import { TypeOrmModule, TypeOrmModuleOptions } from '@nestjs/typeorm';
import BackOfficeConfigFactory from '../config';

export const SQLiteClientFactory = TypeOrmModule.forRoot(
  BackOfficeConfigFactory.get('slite') as TypeOrmModuleOptions,
);
