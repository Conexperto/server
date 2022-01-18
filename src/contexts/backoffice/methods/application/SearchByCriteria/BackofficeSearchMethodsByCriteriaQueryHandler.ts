import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { Filters } from 'src/contexts/shared/domain/criteria/Filters';
import { Order } from 'src/contexts/shared/domain/criteria/Order';
import { BackofficeMethodsResponse } from '../BackofficeMethodsResponse';
import { BackofficeMethodsByCriteriaSearcher } from './BackofficeMethodsByCriteriaSearcher';
import { BackofficeSearchMethodsByCriteriaQuery } from './BackofficeSearchMethodsByCriteriaQuery';

@QueryHandler(BackofficeSearchMethodsByCriteriaQuery)
export class BackofficeSearchMethodsByCriteriaQueryHandler
  implements IQueryHandler<BackofficeSearchMethodsByCriteriaQuery>
{
  constructor(private readonly searcher: BackofficeMethodsByCriteriaSearcher) {}

  async execute(
    query: BackofficeSearchMethodsByCriteriaQuery,
  ): Promise<BackofficeMethodsResponse> {
    const filters = Filters.fromValues(query.filters);
    const order = Order.fromValues(query.orderBy, query.orderType);

    return this.searcher.run(filters, order, query.offset, query.limit);
  }
}
