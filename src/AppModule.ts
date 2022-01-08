import { Module } from '@nestjs/common';
import { AppApiModule } from './apps/api/AppApiModule';
import { AppBackOfficeModule } from './apps/backoffice/AppBackOfficeModule';
import { BackOfficeModule } from './contexts/backoffice/BackOfficeModule';

@Module({
  imports: [AppApiModule, AppBackOfficeModule, BackOfficeModule],
})
export class AppModule {}
