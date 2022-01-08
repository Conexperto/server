import { Module } from '@nestjs/common';
import { SQLiteClientFactory } from '../backoffice/shared/infrastructure/persistence/SQLiteClientFactory';
import WinstonLogger from './infrastructure/WinstonLogger';

@Module({
  imports: [],
  controllers: [],
  providers: [],
  exports: [WinstonLogger, SQLiteClientFactory],
})
export class SharedModule {}
