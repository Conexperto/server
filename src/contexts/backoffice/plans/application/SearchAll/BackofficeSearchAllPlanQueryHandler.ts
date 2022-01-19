import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { BackofficePlansResponse } from '../BackofficePlansResponse';
import { BackofficePlanFinder } from './BackofficePlanFinder';
import { BackofficeSearchAllPlanQuery } from './BackofficeSearchAllPlanQuery';

@QueryHandler(BackofficeSearchAllPlanQuery)
export class BackofficeSearchAllPlanQueryHandler
  implements IQueryHandler<BackofficeSearchAllPlanQuery>
{
  constructor(private readonly finder: BackofficePlanFinder) {}

  async execute(
    command: BackofficeSearchAllPlanQuery,
  ): Promise<BackofficePlansResponse> {
    return this.finder.run();
  }
}
