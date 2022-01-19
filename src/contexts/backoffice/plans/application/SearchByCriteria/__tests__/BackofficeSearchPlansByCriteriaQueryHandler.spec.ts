import { Test } from '@nestjs/testing';
import { BackofficeSQLiteModule } from 'src/contexts/backoffice/shared/infrastructure/persistence/__mocks__/BackofficeSQLiteModule';
import { MethodEntity } from 'src/contexts/shared/infrastructure/entities/MethodEntity';
import { PlanEntity } from 'src/contexts/shared/infrastructure/entities/PlanEntity';
import { Connection } from 'typeorm';
import { BackofficePlan } from '../../../domain/BackofficePlan';
import { BackofficePlanCoinFixture } from '../../../domain/__fixtures__/BackofficePlanCoinFixture';
import { BackofficePlanDurationFixture } from '../../../domain/__fixtures__/BackofficePlanDurationFixture';
import { BackofficePlanIdFixture } from '../../../domain/__fixtures__/BackofficePlanIdFixture';
import { BackofficePlanPriceFixture } from '../../../domain/__fixtures__/BackofficePlanPriceFixture';
import { BackofficeSQLitePlanRepository } from '../../../infrastructure/persistence/BackofficeSQLitePlanRepository';
import { BackofficePlansByCriteriaSearcher } from '../BackofficePlansByCriteriaSearcher';
import { BackofficeSearchPlansByCriteriaQuery } from '../BackofficeSearchPlansByCriteriaQuery';
import { BackofficeSearchPlansByCriteriaQueryHandler } from '../BackofficeSearchPlansByCriteriaQueryHandler';

jest.mock(
  'src/contexts/backoffice/shared/infrastructure/persistence/BackofficeSQLiteModule',
);

const backofficePlanMock = () =>
  new BackofficePlan(
    BackofficePlanIdFixture.random(),
    BackofficePlanPriceFixture.random(),
    BackofficePlanDurationFixture.random(),
    BackofficePlanCoinFixture.random(),
  );

describe('BackofficeSearchAllMethodQueryHandler', () => {
  let database: Connection;
  let handler: BackofficeSearchPlansByCriteriaQueryHandler;

  beforeEach(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [BackofficeSQLiteModule],
      providers: [
        BackofficeSQLitePlanRepository,
        BackofficePlansByCriteriaSearcher,
        BackofficeSearchPlansByCriteriaQueryHandler,
      ],
    }).compile();

    database = moduleRef.get<Connection>(Connection);
    handler = moduleRef.get<BackofficeSearchPlansByCriteriaQueryHandler>(
      BackofficeSearchPlansByCriteriaQueryHandler,
    );
  });

  describe('#execute', () => {
    let plans: PlanEntity[] = [];

    beforeEach(async () => {
      for (let i = 0; i < 3; i++) {
        const item = (plans[i] = new PlanEntity());
        const { id, price, duration, coin } =
          backofficePlanMock().toPrimitives();

        item.id = id;
        item.price = price;
        item.duration = duration;
        item.coin = coin;

        await database.manager.save(PlanEntity, item);
      }
    });

    it('should search by criteria plans', async () => {
      const filter = new Map();
      filter.set('field', 'price');
      filter.set('operator', '=');
      filter.set('value', `${plans[0].price}`);

      const orderBy = 'id';
      const orderType = 'asc';
      const limit = 10;
      const offset = 0;
      const query = new BackofficeSearchPlansByCriteriaQuery(
        [filter],
        orderBy,
        orderType,
        limit,
        offset,
      );
      const result = await handler.execute(query);

      expect(result.plans).not.toBeUndefined();
      result.plans.map((item) => {
        const raw = item.toPrimitives();

        expect(plans).toContain({
          id: raw.id,
          price: raw.price,
          duration: raw.duration,
          coin: raw.coin,
        });
      });
    });
  });
});
