import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { LoadsModule } from './loads/loads.module';
import { NegotiationModule } from './negotiation/negotiation.module';
import { FmcsaModule } from './fmcsa/fmcsa.module';
import { MetricsModule } from './metrics/metrics.module';
import { AuthModule } from './auth/auth.module';
import { WebhookModule } from './webhook/webhook.module';

@Module({
  imports: [LoadsModule, NegotiationModule, FmcsaModule, MetricsModule, AuthModule, WebhookModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
