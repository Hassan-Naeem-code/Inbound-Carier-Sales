import { Controller, Post, Body, Logger, BadRequestException } from '@nestjs/common';
import { LoadsService } from '../loads/loads.service';
import { FmcsaService } from '../fmcsa/fmcsa.service';
import { NegotiationService } from '../negotiation/negotiation.service';
import * as fs from 'fs';
import * as path from 'path';
import * as Joi from 'joi';
import OpenAI from 'openai';


@Controller('webhook/happyrobot')
export class WebhookController {
	private readonly logger = new Logger(WebhookController.name);
	constructor(
		private readonly loadsService: LoadsService,
		private readonly fmcsaService: FmcsaService,
		private readonly negotiationService: NegotiationService,
	) {}

			@Post()
				async handleWebhook(@Body() payload: any) {
				// Joi schema for validation
				const schema = Joi.object({
					mc_number: Joi.string().required(),
					equipment_type: Joi.string().required(),
					origin: Joi.string().required(),
					destination: Joi.string().required(),
					initial_offer: Joi.number().required(),
					call_transcript: Joi.string().required(),
				});
				const { error, value } = schema.validate(payload);
				if (error || !value) {
					this.logger.error(`Validation error: ${error?.message || 'Payload is empty or invalid'}`);
					throw new BadRequestException(`Missing or invalid fields: ${error?.message || 'Payload is empty or invalid'}`);
				}
				const { mc_number, equipment_type, origin, destination, initial_offer, call_transcript } = value;

				// Real sentiment analysis using OpenAI GPT
				let sentiment = 'Neutral';
				try {
					const openaiApiKey = process.env.OPENAI_API_KEY;
					if (!openaiApiKey) {
						throw new Error('OPENAI_API_KEY is not set in environment variables');
					}
					const openai = new OpenAI({ apiKey: openaiApiKey });
					const prompt = `Classify the sentiment of the following transcript as Positive, Negative, or Neutral. Only respond with one word (Positive, Negative, or Neutral).\nTranscript: ${call_transcript}`;
					const completion = await openai.chat.completions.create({
						model: 'gpt-3.5-turbo',
						messages: [
							{ role: 'system', content: 'You are a sentiment analysis agent.' },
							{ role: 'user', content: prompt }
						],
						max_tokens: 1,
						temperature: 0,
					});
					const aiResponse = completion.choices[0].message?.content?.trim();
					if (aiResponse && ['Positive', 'Negative', 'Neutral'].includes(aiResponse)) {
						sentiment = aiResponse;
					}
				} catch (err) {
					this.logger.error(`OpenAI sentiment analysis failed: ${err.message}`);
					// fallback: Neutral
				}

				const mc_status = this.fmcsaService.verifyMcNumber(mc_number);
				if (!mc_status) {
					this.logger.error(`MC not eligible: ${mc_number}`);
					return { status: 'rejected', reason: 'MC not eligible' };
				}
				const loads = this.loadsService.findAll({ equipment_type, origin, destination });
				if (!loads.length) {
					this.logger.error(`No loads found for equipment_type=${equipment_type}, origin=${origin}, destination=${destination}`);
					return { status: 'no_loads_found' };
				}
				const chosen_load = loads[0];
				const negotiation = this.negotiationService.negotiate(chosen_load, initial_offer);
				const outcome = negotiation.accepted ? 'Deal Closed' : 'No Deal';
				// Log negotiation
				const logPath = path.join(__dirname, '../../../negotiations.log');
				const logData = {
					mc_number,
					load_id: chosen_load.load_id,
					...negotiation,
					outcome,
					sentiment,
				};
				fs.appendFileSync(logPath, JSON.stringify(logData) + '\n');
				return {
					status: 'processed',
					load: chosen_load,
					negotiation,
					outcome,
					sentiment,
				};
			}
}
