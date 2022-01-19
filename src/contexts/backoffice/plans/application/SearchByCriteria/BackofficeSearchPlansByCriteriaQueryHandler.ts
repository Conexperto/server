import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { Filters } from 'src/contexts/shared/domain/criteria/Filters';
import { Order } from 'src/contexts/shared/domain/criteria/Order';
import { BackofficePlansResponse } from '../BackofficePlansResponse';
import { BackofficePlansByCriteriaSearcher } from './BackofficePlansByCriteriaSearcher';
import { BackofficeSearchPlansByCriteriaQuery } from './BackofficeSearchPlansByCriteriaQuery';

@QueryHandler(BackofficeSearchPlansByCriteriaQuery)
export class BackofficeSearchPlansByCriteriaQueryHandler
  implements IQueryHandler<BackofficeSearchPlansByCriteriaQuery>
{
  constructor(private readonly searcher: BackofficePlansByCriteriaSearcher) {}

  async execute(
    query: BackofficeSearchPlansByCriteriaQuery,
  ): Promise<BackofficePlansResponse> {
    const filters = Filters.fromValues(query.filters);
    const order = Order.fromValues(query.orderBy, query.orderType);

    return this.searcher.run(filters, order, query.offset, query.limit);
  }
}
