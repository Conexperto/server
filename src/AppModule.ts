import { Module } from '@nestjs/common';
import { AppApiModule } from './apps/api/AppApiModule';
import { AppBackOfficeModule } from './apps/backoffice/AppBackOfficeModule';
import { BackofficeModule } from './contexts/backoffice/BackofficeModule';

@Module({
  imports: [AppApiModule, AppBackOfficeModule, BackofficeModule],
})
export class AppModule {}
