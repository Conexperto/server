import { Module } from '@nestjs/common';
import WinstonLogger from './infrastructure/WinstonLogger';

@Module({
  imports: [],
  controllers: [],
  providers: [],
  exports: [WinstonLogger],
})
export class SharedModule {}
