import { Test, TestingModule } from '@nestjs/testing';
import { FmcsaService } from './fmcsa.service';

describe('FmcsaService', () => {
  let service: FmcsaService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [FmcsaService],
    }).compile();

    service = module.get<FmcsaService>(FmcsaService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
