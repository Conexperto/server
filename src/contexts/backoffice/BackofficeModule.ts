import { Module } from '@nestjs/common';
import { BackofficeAdminModule } from './admins/BackofficeAdminModule';
import { BackofficeSQLiteModule } from './shared/infrastructure/persistence/BackofficeSQLiteModule';

@Module({
  imports: [BackofficeSQLiteModule],
  providers: [BackofficeAdminModule],
  exports: [BackofficeAdminModule],
})
export class BackofficeModule {}
