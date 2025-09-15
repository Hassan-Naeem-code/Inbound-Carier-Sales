import { Controller, Post, Body, UseGuards, BadRequestException, Logger } from '@nestjs/common';
import * as Joi from 'joi';
import { FmcsaService } from './fmcsa.service';
import { ApiKeyGuard } from '../auth/api-key.guard';


@Controller('verify_mc')
@UseGuards(ApiKeyGuard)
export class FmcsaController {
	private readonly logger = new Logger(FmcsaController.name);
	constructor(private readonly fmcsaService: FmcsaService) {}

	@Post()
	verify(@Body() body: any) {
		const schema = Joi.object({
			mc_number: Joi.string().required(),
		});
		const { error, value } = schema.validate(body);
		if (error) {
			this.logger.error(`Validation error: ${error.message}`);
			throw new BadRequestException(`Missing or invalid fields: ${error.message}`);
		}
		const eligible = this.fmcsaService.verifyMcNumber(value.mc_number);
		return { mc_number: value.mc_number, eligible };
	}
}
