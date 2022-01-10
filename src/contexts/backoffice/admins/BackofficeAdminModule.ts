import { Module } from '@nestjs/common';
import { CqrsModule } from '@nestjs/cqrs';
import { CreateBackofficeAdminCommandHandler } from './application/Create/CreateBackofficeAdminCommandHandler';
import { BackofficeSearchAllAdminQueryHandler } from './application/SearchAll/BackofficeSearchAllAdminQueryHandler';
import { BackofficeSearchAdminsByCriteriaQueryHandler } from './application/SearchByCriteria/BackofficeSearchAdminsByCriteriaQueryHandler';
import { BackofficeSQLiteAdminRepository } from './infrastructure/persistence/BackofficeSQLiteAdminRepository';

@Module({
  imports: [CqrsModule],
  providers: [
    BackofficeSQLiteAdminRepository,
    CreateBackofficeAdminCommandHandler,
    BackofficeSearchAllAdminQueryHandler,
    BackofficeSearchAdminsByCriteriaQueryHandler,
  ],
})
export class BackofficeAdminModule {}
