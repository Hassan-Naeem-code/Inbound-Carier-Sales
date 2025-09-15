import { Module } from '@nestjs/common';
import { WebhookController } from './webhook.controller';
import { LoadsModule } from '../loads/loads.module';
import { FmcsaModule } from '../fmcsa/fmcsa.module';
import { NegotiationModule } from '../negotiation/negotiation.module';

@Module({
  imports: [LoadsModule, FmcsaModule, NegotiationModule],
  controllers: [WebhookController],
})
export class WebhookModule {}
