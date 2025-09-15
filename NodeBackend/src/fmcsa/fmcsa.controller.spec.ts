import { Test, TestingModule } from '@nestjs/testing';
import { FmcsaController } from './fmcsa.controller';

describe('FmcsaController', () => {
  let controller: FmcsaController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [FmcsaController],
    }).compile();

    controller = module.get<FmcsaController>(FmcsaController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
