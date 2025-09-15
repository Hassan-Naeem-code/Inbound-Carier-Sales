import { Test, TestingModule } from '@nestjs/testing';
import { LoadsService } from './loads.service';

describe('LoadsService', () => {
  let service: LoadsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [LoadsService],
    }).compile();

    service = module.get<LoadsService>(LoadsService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
