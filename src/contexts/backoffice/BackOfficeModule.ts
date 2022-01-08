import { Module } from '@nestjs/common';
import { BackOfficeSharedModule } from './shared/BackOfficeSharedModule';

@Module({
  imports: [BackOfficeSharedModule],
  controllers: [],
  providers: [],
  exports: [],
})
export class BackOfficeModule {}
