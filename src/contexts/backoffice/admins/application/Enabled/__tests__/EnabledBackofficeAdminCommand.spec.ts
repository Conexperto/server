import { BackofficeAdminIdFixture } from '../../../domain/__fixtures__/BackofficeAdminIdFixture';
import { EnabledBackofficeAdminCommand } from '../EnabledBackofficeAdminCommand';

describe('EnabledBackofficeAdminCommand', () => {
  it('should enabler command', async () => {
    const uid = BackofficeAdminIdFixture.random().value;
    const command = new EnabledBackofficeAdminCommand(uid);

    expect(command instanceof EnabledBackofficeAdminCommand).toBeTruthy();
    expect(command).toMatchObject({ id: uid });
  });
});
