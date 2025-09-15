import { Controller, Get, UseGuards } from '@nestjs/common';
import { MetricsService } from './metrics.service';
import { ApiKeyGuard } from '../auth/api-key.guard';

@Controller('metrics')
@UseGuards(ApiKeyGuard)
export class MetricsController {
	constructor(private readonly metricsService: MetricsService) {}

	@Get()
	getNegotiationCount() {
		return { negotiations: this.metricsService.getNegotiationCount() };
	}
}
