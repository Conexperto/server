import { Test } from '@nestjs/testing';
import { BackofficeSQLiteModule } from 'src/contexts/backoffice/shared/infrastructure/persistence/BackofficeSQLiteModule';
import { Criteria } from 'src/contexts/shared/domain/criteria/Criteria';
import { Filter } from 'src/contexts/shared/domain/criteria/Filter';
import { FilterField } from 'src/contexts/shared/domain/criteria/FilterField';
import {
  FilterOperator,
  Operator,
} from 'src/contexts/shared/domain/criteria/FilterOperator';
import { Filters } from 'src/contexts/shared/domain/criteria/Filters';
import { FilterValue } from 'src/contexts/shared/domain/criteria/FilterValue';
import { AdminEntity } from 'src/contexts/shared/infrastructure/entities/AdminEntity';
import { Connection } from 'typeorm';
import { BackofficeAdmin } from '../../../domain/BackofficeAdmin';
import { BackofficeAdminId } from '../../../domain/BackofficeAdminId';
import { BackofficeAdminDisplayNameFixture } from '../../../domain/__fixtures__/BackofficeAdminDisplayNameFixture';
import { BackofficeAdminEmailFixture } from '../../../domain/__fixtures__/BackofficeAdminEmailFixture';
import { BackofficeAdminIdFixture } from '../../../domain/__fixtures__/BackofficeAdminIdFixture';
import { BackofficeAdminLastnameFixture } from '../../../domain/__fixtures__/BackofficeAdminLastnameFixture';
import { BackofficeAdminNameFixture } from '../../../domain/__fixtures__/BackofficeAdminNameFixture';
import { BackofficeAdminPhoneNumberFixture } from '../../../domain/__fixtures__/BackofficeAdminPhoneNumberFixture';
import { BackofficeAdminPhotoURLFixture } from '../../../domain/__fixtures__/BackofficeAdminPhotoURLFixture';
import { BackofficeAdminRoleFixture } from '../../../domain/__fixtures__/BackofficeAdminRoleFixture';
import { BackofficeSQLiteAdminRepository } from '../BackofficeSQLiteAdminRepository';

jest.mock(
  'src/contexts/backoffice/shared/infrastructure/persistence/BackofficeSQLiteModule',
);

describe('BackofficeSQLiteAdminRepository', () => {
  let database: Connection;
  let repository: BackofficeSQLiteAdminRepository;

  beforeEach(async () => {
    let moduleRef = await Test.createTestingModule({
      imports: [BackofficeSQLiteModule],
      providers: [BackofficeSQLiteAdminRepository],
    }).compile();

    database = moduleRef.get<Connection>(Connection);
    repository = moduleRef.get<BackofficeSQLiteAdminRepository>(
      BackofficeSQLiteAdminRepository,
    );
  });

  afterEach(async () => {
    await database.close();
  });

  describe('#save', () => {
    it('should create a new admin', async () => {
      const admin = new BackofficeAdmin(
        BackofficeAdminIdFixture.random(),
        BackofficeAdminEmailFixture.random(),
        BackofficeAdminDisplayNameFixture.random(),
        BackofficeAdminPhoneNumberFixture.random(),
        BackofficeAdminPhotoURLFixture.random(),
        BackofficeAdminNameFixture.random(),
        BackofficeAdminLastnameFixture.random(),
        BackofficeAdminRoleFixture.random(),
      );
      const raw = admin.toPrimitives();

      await repository.save(admin);

      const entity = await database.manager.findOne(AdminEntity, {
        uid: raw.id,
      });

      expect(entity).not.toBeUndefined();
      expect(raw).toMatchObject({
        id: entity.uid,
        email: entity.email,
        displayName: entity.displayName,
        phoneNumber: entity.phoneNumber,
        photoURL: entity.photoURL,
        name: entity.name,
        lastname: entity.lastname,
        role: +entity.role,
      });
    });
  });

  describe('#findById', () => {
    let admin: AdminEntity;
    let entity: AdminEntity;

    beforeEach(async () => {
      admin = new AdminEntity();

      admin.uid = BackofficeAdminIdFixture.random().value;
      admin.email = BackofficeAdminEmailFixture.random().value;
      admin.displayName = BackofficeAdminDisplayNameFixture.random().value;
      admin.phoneNumber = BackofficeAdminPhoneNumberFixture.random().value;
      admin.photoURL = BackofficeAdminPhotoURLFixture.random().value;
      admin.name = BackofficeAdminNameFixture.random().value;
      admin.lastname = BackofficeAdminLastnameFixture.random().value;
      admin.role = BackofficeAdminRoleFixture.random().value;

      entity = await database.manager.save(AdminEntity, admin);
    });

    it('should find a admin by id', async () => {
      const result = await repository.findById(
        new BackofficeAdminId(entity.uid),
      );
      const raw = result.toPrimitives();

      expect(entity).not.toBeUndefined();
      expect(raw).toMatchObject({
        id: entity.uid,
        email: entity.email,
        displayName: entity.displayName,
        phoneNumber: entity.phoneNumber,
        photoURL: entity.photoURL,
        name: entity.name,
        lastname: entity.lastname,
        role: +entity.role,
      });
    });
  });

  describe('#findOne', () => {
    let admin: AdminEntity;
    let entity: AdminEntity;

    beforeEach(async () => {
      admin = new AdminEntity();

      admin.uid = BackofficeAdminIdFixture.random().value;
      admin.email = BackofficeAdminEmailFixture.random().value;
      admin.displayName = BackofficeAdminDisplayNameFixture.random().value;
      admin.phoneNumber = BackofficeAdminPhoneNumberFixture.random().value;
      admin.photoURL = BackofficeAdminPhotoURLFixture.random().value;
      admin.name = BackofficeAdminNameFixture.random().value;
      admin.lastname = BackofficeAdminLastnameFixture.random().value;
      admin.role = BackofficeAdminRoleFixture.random().value;

      entity = await database.manager.save(AdminEntity, admin);
    });

    it('should find a admin by criteria', async () => {
      const filter = new Filter(
        new FilterField('email'),
        FilterOperator.fromValue(Operator.EQUAL),
        new FilterValue(admin.email),
      );
      const filters = new Filters([filter]);
      const criteria = new Criteria(filters);
      const result = await repository.findOne(criteria);
      const raw = result.toPrimitives();

      expect(result).not.toBeUndefined();
      expect(raw).toMatchObject({
        id: entity.uid,
        email: entity.email,
        displayName: entity.displayName,
        phoneNumber: entity.phoneNumber,
        photoURL: entity.photoURL,
        name: entity.name,
        lastname: entity.lastname,
        role: +entity.role,
      });
    });
  });

  describe('#findAll', () => {
    let admins: AdminEntity[] = [];
    let entities: AdminEntity[] = [];

    beforeEach(async () => {
      for (let i = 0; i < 3; i++) {
        const item = (admins[i] = new AdminEntity());

        item.uid = BackofficeAdminIdFixture.random().value;
        item.email = BackofficeAdminEmailFixture.random().value;
        item.displayName = BackofficeAdminDisplayNameFixture.random().value;
        item.phoneNumber = BackofficeAdminPhoneNumberFixture.random().value;
        item.photoURL = BackofficeAdminPhotoURLFixture.random().value;
        item.name = BackofficeAdminNameFixture.random().value;
        item.lastname = BackofficeAdminLastnameFixture.random().value;
        item.role = BackofficeAdminRoleFixture.random().value;

        entities[i] = await database.manager.save(AdminEntity, item);
      }
    });

    it('should find all admin', async () => {
      expect(admins).toHaveLength(3);
      admins.map((item) => expect(entities).toContain(item));
    });
  });

  describe('#delete', () => {
    let admin: AdminEntity;
    let entity: AdminEntity;

    beforeEach(async () => {
      admin = new AdminEntity();

      admin.uid = BackofficeAdminIdFixture.random().value;
      admin.email = BackofficeAdminEmailFixture.random().value;
      admin.displayName = BackofficeAdminDisplayNameFixture.random().value;
      admin.phoneNumber = BackofficeAdminPhoneNumberFixture.random().value;
      admin.photoURL = BackofficeAdminPhotoURLFixture.random().value;
      admin.name = BackofficeAdminNameFixture.random().value;
      admin.lastname = BackofficeAdminLastnameFixture.random().value;
      admin.role = BackofficeAdminRoleFixture.random().value;

      entity = await database.manager.save(AdminEntity, admin);
    });

    it('should delete a admin', async () => {
      await repository.delete(entity.uid);

      const result = await database.manager.findOne(AdminEntity, {
        uid: entity.uid,
      });

      expect(result).toBeUndefined();
    });
  });

  describe('#remove', () => {
    let admins: AdminEntity[] = [];
    let entities: AdminEntity[] = [];

    beforeEach(async () => {
      for (let i = 0; i < 3; i++) {
        const item = (admins[i] = new AdminEntity());

        item.uid = BackofficeAdminIdFixture.random().value;
        item.email = BackofficeAdminEmailFixture.random().value;
        item.displayName = BackofficeAdminDisplayNameFixture.random().value;
        item.phoneNumber = BackofficeAdminPhoneNumberFixture.random().value;
        item.photoURL = BackofficeAdminPhotoURLFixture.random().value;
        item.name = BackofficeAdminNameFixture.random().value;
        item.lastname = BackofficeAdminLastnameFixture.random().value;
        item.role = BackofficeAdminRoleFixture.random().value;

        entities[i] = await database.manager.save(AdminEntity, item);
      }
    });

    it('should remove admins', async () => {
      const ids = entities.map((item) => item.uid);
      await repository.remove(ids);

      const results = await database.manager.findByIds(
        AdminEntity,
        entities.map((item) => item.id),
      );

      expect(results).toHaveLength(0);
      results.map((item) => expect(entities).not.toContain(item));
    });
  });

  describe('#disabled', () => {
    let admins: AdminEntity[] = [];
    let entities: AdminEntity[] = [];

    beforeEach(async () => {
      for (let i = 0; i < 3; i++) {
        const item = (admins[i] = new AdminEntity());

        item.uid = BackofficeAdminIdFixture.random().value;
        item.email = BackofficeAdminEmailFixture.random().value;
        item.displayName = BackofficeAdminDisplayNameFixture.random().value;
        item.phoneNumber = BackofficeAdminPhoneNumberFixture.random().value;
        item.photoURL = BackofficeAdminPhotoURLFixture.random().value;
        item.name = BackofficeAdminNameFixture.random().value;
        item.lastname = BackofficeAdminLastnameFixture.random().value;
        item.role = BackofficeAdminRoleFixture.random().value;

        entities[i] = await database.manager.save(AdminEntity, item);
      }
    });

    it('should disabled admin', async () => {
      const ids = entities.map((item) => item.uid);

      await repository.disabled(ids);

      const result = await database.manager.findByIds(
        AdminEntity,
        entities.map((item) => item.id),
      );

      expect(result).toHaveLength(entities.length);
      result.map((item) => expect(item.disabled).toBeTruthy());
    });
  });
});
