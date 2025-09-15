import { Injectable } from '@nestjs/common';

@Injectable()
export class FmcsaService {
	verifyMcNumber(mc_number: string): boolean {
		// Mock logic, replace with real API call if needed
		const validMc = ['123456', '654321'];
		return validMc.includes(mc_number);
	}
}
