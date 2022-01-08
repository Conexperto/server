import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'sqlite',
      database: 'cxp_db',
      entities: [__dirname + '/**/**/entities/*{.ts,.js}'],
      synchronize: true,
    }),
  ],
  controllers: [],
  providers: [],
  exports: [],
})
export class BackOfficeModule {}
