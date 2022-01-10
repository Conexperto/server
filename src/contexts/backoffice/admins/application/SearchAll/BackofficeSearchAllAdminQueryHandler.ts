import { IQueryHandler, QueryHandler } from '@nestjs/cqrs';
import { BackofficeAdminFinder } from './BackofficeAdminFinder';
import { BackofficeSearchAllAdminQuery } from './BackofficeSearchAllAdminQuery';

@QueryHandler(BackofficeSearchAllAdminQuery)
export class BackofficeSearchAllAdminQueryHandler
  implements IQueryHandler<BackofficeSearchAllAdminQuery>
{
  constructor(private readonly adminFinder: BackofficeAdminFinder) {}

  async execute() {
    return this.adminFinder.run();
  }
}
