import { Module } from '@nestjs/common';
import { AppApiModule } from './apps/api/AppApiModule';
import { AppBackOfficeModule } from './apps/backoffice/AppBackOfficeModule';
import { SharedModule } from './contexts/shared/SharedModule';

@Module({
  imports: [AppApiModule, AppBackOfficeModule, SharedModule],
})
export class AppModule {}
