import { BackofficeAdminIdFixture } from '../../../domain/__fixtures__/BackofficeAdminIdFixture';
import { DeleteBackofficeAdminCommand } from '../DeleteBackofficeAdminCommand';

describe('DeleteBackofficeAdminCommand', () => {
  it('should deleter command', async () => {
    const uid = BackofficeAdminIdFixture.random().value;
    const command = new DeleteBackofficeAdminCommand(uid);

    expect(command instanceof DeleteBackofficeAdminCommand).toBeTruthy();
    expect(command).toMatchObject({ id: uid });
  });
});
