import { Controller, Post, Body, UseGuards, BadRequestException, Logger } from '@nestjs/common';
import * as Joi from 'joi';
import { NegotiationService } from './negotiation.service';
import { ApiKeyGuard } from '../auth/api-key.guard';


@Controller('negotiation')
@UseGuards(ApiKeyGuard)
export class NegotiationController {
	private readonly logger = new Logger(NegotiationController.name);
	constructor(private readonly negotiationService: NegotiationService) {}

	@Post()
	negotiate(@Body() body: any) {
		const schema = Joi.object({
			load: Joi.object().required(),
			initial_offer: Joi.number().required(),
		});
		const { error, value } = schema.validate(body);
		if (error) {
			this.logger.error(`Validation error: ${error.message}`);
			throw new BadRequestException(`Missing or invalid fields: ${error.message}`);
		}
		return this.negotiationService.negotiate(value.load, value.initial_offer);
	}
}
