import { Test } from '@nestjs/testing';
import { BackofficeSQLiteModule } from 'src/contexts/backoffice/shared/infrastructure/persistence/__mocks__/BackofficeSQLiteModule';
import { AdminEntity } from 'src/contexts/shared/infrastructure/entities/AdminEntity';
import { Connection } from 'typeorm';
import { BackofficeAdminId } from '../../../domain/BackofficeAdminId';
import { BackofficeAdminDisplayNameFixture } from '../../../domain/__fixtures__/BackofficeAdminDisplayNameFixture';
import { BackofficeAdminEmailFixture } from '../../../domain/__fixtures__/BackofficeAdminEmailFixture';
import { BackofficeAdminIdFixture } from '../../../domain/__fixtures__/BackofficeAdminIdFixture';
import { BackofficeAdminLastnameFixture } from '../../../domain/__fixtures__/BackofficeAdminLastnameFixture';
import { BackofficeAdminNameFixture } from '../../../domain/__fixtures__/BackofficeAdminNameFixture';
import { BackofficeAdminPhoneNumberFixture } from '../../../domain/__fixtures__/BackofficeAdminPhoneNumberFixture';
import { BackofficeAdminPhotoURLFixture } from '../../../domain/__fixtures__/BackofficeAdminPhotoURLFixture';
import { BackofficeAdminRoleFixture } from '../../../domain/__fixtures__/BackofficeAdminRoleFixture';
import { BackofficeSQLiteAdminRepository } from '../../../infrastructure/persistence/BackofficeSQLiteAdminRepository';
import { BackofficeAdminDeleter } from '../BackofficeAdminDeleter';

describe('BackofficeAdminDeleter', () => {
  let database: Connection;
  let deleter: BackofficeAdminDeleter;

  beforeEach(async () => {
    let moduleRef = await Test.createTestingModule({
      imports: [BackofficeSQLiteModule],
      providers: [BackofficeSQLiteAdminRepository, BackofficeAdminDeleter],
    }).compile();

    database = moduleRef.get<Connection>(Connection);
    deleter = moduleRef.get<BackofficeAdminDeleter>(BackofficeAdminDeleter);
  });

  afterEach(async () => {
    await database.close();
  });

  describe('#run', () => {
    let admin: AdminEntity;

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

      await database.manager.save(admin);
    });

    it('should delete a admin', async () => {
      await deleter.run([new BackofficeAdminId(admin.uid)]);

      const result = await database.manager.findOne(AdminEntity, {
        uid: admin.uid,
      });

      expect(result).toBeUndefined();
    });
  });
});
