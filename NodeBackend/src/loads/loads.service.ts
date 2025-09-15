import { Injectable } from '@nestjs/common';
import * as fs from 'fs';
import * as path from 'path';

@Injectable()
export class LoadsService {
	private loads: any[];

	constructor() {
		// const dataPath = path.join(__dirname, '../../../loads.json');
        const dataPath = path.join(process.cwd(), 'loads.json');
		this.loads = JSON.parse(fs.readFileSync(dataPath, 'utf-8'));
	}

	findAll(query: any) {
		let results = this.loads;
		if (query.equipment_type) {
			results = results.filter(
				l => l.equipment_type.toLowerCase() === query.equipment_type.toLowerCase(),
			);
		}
		if (query.origin) {
			results = results.filter(l =>
				l.origin.toLowerCase().includes(query.origin.toLowerCase()),
			);
		}
		if (query.destination) {
			results = results.filter(l =>
				l.destination.toLowerCase().includes(query.destination.toLowerCase()),
			);
		}
		return results;
	}

	findOne(load_id: string) {
		return this.loads.find(l => l.load_id === load_id);
	}
}
