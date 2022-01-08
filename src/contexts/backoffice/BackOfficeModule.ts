import { Module } from '@nestjs/common';
import { SharedModule } from '../shared/SharedModule';
import { SQLiteClientFactory } from './shared/infrastructure/persistence/SQLiteClientFactory';

@Module({
  imports: [SQLiteClientFactory, SharedModule],
  controllers: [],
  providers: [],
  exports: [],
})
export class BackOfficeModule {}
