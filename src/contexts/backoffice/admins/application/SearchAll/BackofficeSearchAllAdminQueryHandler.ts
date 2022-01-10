import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { BackofficeAdminsResponse } from '../BackofficeAdminsResponse';
import { BackofficeAdminFinder } from './BackofficeAdminFinder';
import { BackofficeSearchAllAdminQuery } from './BackofficeSearchAllAdminQuery';

@QueryHandler(BackofficeSearchAllAdminQuery)
export class BackofficeSearchAllAdminQueryHandler
  implements IQueryHandler<BackofficeSearchAllAdminQuery>
{
  constructor(private readonly finder: BackofficeAdminFinder) {}

  async execute(): Promise<BackofficeAdminsResponse> {
    return this.finder.run();
  }
}
