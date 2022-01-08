import { Module } from '@nestjs/common';
import { BackOfficeSQLiteModule } from './shared/infrastructure/persistence/BackOfficeSQLiteModule';

@Module({
  imports: [BackOfficeSQLiteModule],
  exports: [],
})
export class BackOfficeModule {}
