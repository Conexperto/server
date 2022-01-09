import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AdminEntity } from '../entities/AdminEntity';
import { AssociationUserToMethodEntity } from '../entities/AssociationUserToMethodEntity';
import { AssociationUserToSpecialityEntity } from '../entities/AssociationUserToSpecialityEntity';
import { MethodEntity } from '../entities/MethodEntity';
import { PlanEntity } from '../entities/PlanEntity';
import { SpecialityEntity } from '../entities/SpecialityEntity';
import { UserEntity } from '../entities/UserEntity';
import { UserExpertEntity } from '../entities/UserExpertEntity';
import { UserRatingEntity } from '../entities/UserRatingEntity';

const database = TypeOrmModule.forRoot({
  type: 'sqlite',
  database: 'cxp_db',
  entities: [
    AdminEntity,
    UserEntity,
    UserExpertEntity,
    AssociationUserToSpecialityEntity,
    AssociationUserToMethodEntity,
    UserRatingEntity,
    PlanEntity,
    SpecialityEntity,
    MethodEntity,
  ],
  synchronize: true,
});

const schemas = TypeOrmModule.forFeature([
  AdminEntity,
  UserEntity,
  UserExpertEntity,
  AssociationUserToSpecialityEntity,
  AssociationUserToMethodEntity,
  UserRatingEntity,
  PlanEntity,
  SpecialityEntity,
  MethodEntity,
]);

@Module({
  imports: [database, schemas],
  exports: [database, schemas],
})
export class BackofficeSQLiteModule {}
