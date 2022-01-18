import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { Filters } from 'src/contexts/shared/domain/criteria/Filters';
import { Order } from 'src/contexts/shared/domain/criteria/Order';
import { BackofficeAdminsResponse } from '../BackofficeAdminsResponse';
import { BackofficeAdminsByCriteriaSearcher } from './BackofficeAdminsByCriteriaSearcher';
import { BackofficeSearchAdminsByCriteriaQuery } from './BackofficeSearchAdminsByCriteriaQuery';

@QueryHandler(BackofficeSearchAdminsByCriteriaQuery)
export class BackofficeSearchAdminsByCriteriaQueryHandler
  implements IQueryHandler<BackofficeSearchAdminsByCriteriaQuery>
{
  constructor(private readonly searcher: BackofficeAdminsByCriteriaSearcher) {}

  async execute(
    query: BackofficeSearchAdminsByCriteriaQuery,
  ): Promise<BackofficeAdminsResponse> {
    const filters = Filters.fromValues(query.filters);
    const order = Order.fromValues(query.orderBy, query.orderType);

    return this.searcher.run(filters, order, query.offset, query.limit);
  }
}
