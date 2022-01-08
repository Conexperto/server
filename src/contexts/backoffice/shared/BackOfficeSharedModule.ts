import { Module } from '@nestjs/common';
import { SQLiteClientFactory } from './infrastructure/persistence/SQLiteClientFactory';

@Module({
  imports: [],
  controllers: [],
  providers: [],
  exports: [SQLiteClientFactory],
})
export class BackOfficeSharedModule {}
