import { Module } from '@nestjs/common';
import { AppApiModule } from './apps/api/AppApiModule';
import { AppBackOfficeModule } from './apps/backoffice/AppBackOfficeModule';
import { WinstonLogger } from './shared/infrastructure/WinstonLogger';

@Module({
  imports: [AppApiModule, AppBackOfficeModule, WinstonLogger],
})
export class AppModule {}
