import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { Filters } from 'src/contexts/shared/domain/criteria/Filters';
import { Order } from 'src/contexts/shared/domain/criteria/Order';
import { BackofficeSpecialitiesResponse } from '../BackofficeSpecialitiesResponse';
import { BackofficeSearchSpecialitiesByCriteriaQuery } from './BackofficeSearchSpecialitiesByCriteriaQuery';
import { BackofficeSpecialitiesByCriteriaSearcher } from './BackofficeSpecialitiesByCriteriaSeacher';

@QueryHandler(BackofficeSearchSpecialitiesByCriteriaQuery)
export class BackofficeSearchSpecialitiesByCriteriaQueryHandler
  implements IQueryHandler<BackofficeSearchSpecialitiesByCriteriaQuery>
{
  constructor(
    private readonly searcher: BackofficeSpecialitiesByCriteriaSearcher,
  ) {}

  async execute(
    query: BackofficeSearchSpecialitiesByCriteriaQuery,
  ): Promise<BackofficeSpecialitiesResponse> {
    const filters = Filters.fromValues(query.filters);
    const order = Order.fromValues(query.orderBy, query.orderType);

    return this.searcher.run(filters, order, query.offset, query.limit);
  }
}
