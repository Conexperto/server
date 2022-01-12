import { Test } from '@nestjs/testing';
import { on } from 'events';
import { BackofficeSQLiteModule } from 'src/contexts/backoffice/shared/infrastructure/persistence/__mocks__/BackofficeSQLiteModule';
import { AdminEntity } from 'src/contexts/shared/infrastructure/entities/AdminEntity';
import { Connection } from 'typeorm';
import { BackofficeAdminIdFixture } from '../../../domain/__fixtures__/BackofficeAdminIdFixture';
import { BackofficeSQLiteAdminRepository } from '../../../infrastructure/persistence/BackofficeSQLiteAdminRepository';
import { BackofficeAdminDeleter } from '../BackofficeAdminDeleter';
import { DeleteBackofficeAdminCommand } from '../DeleteBackofficeAdminCommand';
import { DeleteBackofficeAdminCommandHandler } from '../DeleteBackofficeAdminCommandHandler';

describe('DeleteBackofficeAdminCommandHandler', () => {
  let database: Connection;
  let handler: DeleteBackofficeAdminCommandHandler;

  beforeEach(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [BackofficeSQLiteModule],
      providers: [
        BackofficeSQLiteAdminRepository,
        BackofficeAdminDeleter,
        DeleteBackofficeAdminCommandHandler,
      ],
    }).compile();

    database = moduleRef.get<Connection>(Connection);
    handler = moduleRef.get<DeleteBackofficeAdminCommandHandler>(
      DeleteBackofficeAdminCommandHandler,
    );
  });

  it('should deleter a admin', async () => {
    const uid = BackofficeAdminIdFixture.random().value;
    await handler.execute(new DeleteBackofficeAdminCommand(uid));

    const result = await database.manager.findOne(AdminEntity, { uid });

    expect(result).toBeUndefined();
  });
});
