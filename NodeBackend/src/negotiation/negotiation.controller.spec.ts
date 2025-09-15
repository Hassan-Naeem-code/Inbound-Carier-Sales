import { Test, TestingModule } from '@nestjs/testing';
import { NegotiationController } from './negotiation.controller';

describe('NegotiationController', () => {
  let controller: NegotiationController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [NegotiationController],
    }).compile();

    controller = module.get<NegotiationController>(NegotiationController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
