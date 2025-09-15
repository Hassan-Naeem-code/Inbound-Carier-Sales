import { Test, TestingModule } from '@nestjs/testing';
import { NegotiationService } from './negotiation.service';

describe('NegotiationService', () => {
  let service: NegotiationService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [NegotiationService],
    }).compile();

    service = module.get<NegotiationService>(NegotiationService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
