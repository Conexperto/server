import { BackofficeAdminIdFixture } from '../../../domain/__fixtures__/BackofficeAdminIdFixture';
import { DisabledBackofficeAdminCommand } from '../DisabledBackofficeAdminCommand';

describe('DisabledBackofficeAdminCommand', () => {
  it('should disabler command', async () => {
    const uid = BackofficeAdminIdFixture.random().value;
    const command = new DisabledBackofficeAdminCommand(uid);

    expect(command instanceof DisabledBackofficeAdminCommand).toBeTruthy();
    expect(command).toMatchObject({ id: uid });
  });
});
