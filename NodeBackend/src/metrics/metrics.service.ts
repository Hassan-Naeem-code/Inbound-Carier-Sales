import { Injectable } from '@nestjs/common';
import * as fs from 'fs';
import * as path from 'path';

@Injectable()
export class MetricsService {
	getNegotiationCount(): number {
		const logPath = path.join(__dirname, '../../../negotiations.log');
		try {
			const lines = fs.readFileSync(logPath, 'utf-8').split('\n').filter(Boolean);
			return lines.length;
		} catch (e) {
			return 0;
		}
	}
}
