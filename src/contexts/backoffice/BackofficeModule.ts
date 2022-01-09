import { Module } from '@nestjs/common';
import { BackofficeSQLiteModule } from './shared/infrastructure/persistence/BackofficeSQLiteModule';

@Module({
  imports: [BackofficeSQLiteModule],
  exports: [],
})
export class BackofficeModule {}
