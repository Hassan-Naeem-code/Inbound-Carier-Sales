import { Controller, Get, Query, Param, UseGuards } from '@nestjs/common';
import { LoadsService } from './loads.service';
import { ApiKeyGuard } from '../auth/api-key.guard';

@Controller('loads')
@UseGuards(ApiKeyGuard)
export class LoadsController {
	constructor(private readonly loadsService: LoadsService) {}

	@Get()
	findAll(@Query() query: any) {
		return this.loadsService.findAll(query);
	}

	@Get(':load_id')
	findOne(@Param('load_id') load_id: string) {
		const load = this.loadsService.findOne(load_id);
		if (!load) {
			return { detail: 'Load not found' };
		}
		return load;
	}
}
