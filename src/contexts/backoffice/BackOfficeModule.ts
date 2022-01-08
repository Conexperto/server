import { Module } from '@nestjs/common';
import { SQLiteModule } from './shared/infrastructure/persistence/SQLiteModule';

@Module({
  imports: [SQLiteModule],
  exports: [],
})
export class BackOfficeModule {}
