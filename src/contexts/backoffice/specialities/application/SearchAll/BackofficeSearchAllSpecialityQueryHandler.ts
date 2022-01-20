import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { BackofficeSpecialitiesResponse } from '../BackofficeSpecialitiesResponse';
import { BackofficeSearchAllSpecialityQuery } from './BackofficeSearchAllSpecialityQuery';
import { BackofficeSpecialityFinder } from './BackofficeSpecialityFinder';

@QueryHandler(BackofficeSearchAllSpecialityQuery)
export class BackofficeSearchAllSpecialityQueryHandler
  implements IQueryHandler<BackofficeSearchAllSpecialityQuery>
{
  constructor(private readonly finder: BackofficeSpecialityFinder) {}

  async execute(
    command: BackofficeSearchAllSpecialityQuery,
  ): Promise<BackofficeSpecialitiesResponse> {
    return this.finder.run();
  }
}
