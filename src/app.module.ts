import { Module } from '@nestjs/common';
import { AppApiModule } from './apps/api/AppApiModule';
import { AppBackOfficeModule } from './apps/backoffice/AppBackOfficeModule';

@Module({
  imports: [AppApiModule, AppBackOfficeModule],
})
export class AppModule {}

//import { TypeOrmModule } from '@nestjs/typeorm';
//TypeOrmModule.forRoot({
//	type: 'sqlite',
//	database: 'db',
//	entities: [__dirname + '/**/**/entities/*{.ts,.js}'],
//	synchronize: true,
//}),
