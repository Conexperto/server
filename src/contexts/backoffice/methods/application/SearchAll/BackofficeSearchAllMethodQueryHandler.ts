import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { BackofficeMethodsResponse } from '../BackofficeMethodsResponse';
import { BackofficeMethodFinder } from './BackofficeMethodFinder';
import { BackofficeSearchAllMethodQuery } from './BackofficeSearchAllMethodQuery';

@QueryHandler(BackofficeSearchAllMethodQuery)
export class BackofficeSearchAllMethodQueryHandler
  implements IQueryHandler<BackofficeSearchAllMethodQuery>
{
  constructor(private readonly finder: BackofficeMethodFinder) {}

  async execute(
    command: BackofficeSearchAllMethodQuery,
  ): Promise<BackofficeMethodsResponse> {
    return this.finder.run();
  }
}
