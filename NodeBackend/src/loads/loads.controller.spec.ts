import { Test, TestingModule } from '@nestjs/testing';
import { LoadsController } from './loads.controller';

describe('LoadsController', () => {
  let controller: LoadsController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [LoadsController],
    }).compile();

    controller = module.get<LoadsController>(LoadsController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
