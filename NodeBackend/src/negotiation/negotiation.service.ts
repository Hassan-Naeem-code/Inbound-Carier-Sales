import { Injectable } from '@nestjs/common';

@Injectable()
export class NegotiationService {
	negotiate(load: any, initial_offer: number, max_rounds = 3) {
		let counter = load.loadboard_rate;
		let rounds = 0;
		let accepted = false;
		const negotiation_history: any[] = [];
		while (rounds < max_rounds) {
			negotiation_history.push({
				round: rounds + 1,
				carrier_offer: initial_offer,
				broker_offer: counter,
			});
			if (Math.abs(initial_offer - counter) <= 100) {
				accepted = true;
				break;
			}
			counter = Math.floor((counter + initial_offer) / 2);
			rounds += 1;
		}
		return {
			accepted,
			final_rate: accepted ? counter : null,
			history: negotiation_history,
		};
	}
}
