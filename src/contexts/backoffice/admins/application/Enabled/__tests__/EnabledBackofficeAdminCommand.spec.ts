import { BackofficeAdminIdFixture } from '../../../domain/__fixtures__/BackofficeAdminIdFixture';
import { EnabledBackofficeAdminCommand } from '../EnabledBackofficeAdminCommand';

describe('EnabledBackofficeAdminCommand', () => {
  it('should enabler command', () => {
    const uid = BackofficeAdminIdFixture.random().value;
    const command = new EnabledBackofficeAdminCommand(uid);
		
		expect(command).toBeInstanceOf(EnabledBackofficeAdminCommand)
    expect(command).toMatchObject({ id: uid });
  });
});
