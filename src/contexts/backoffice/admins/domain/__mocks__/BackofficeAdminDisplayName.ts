import * as faker from 'faker';
import { BackofficeAdminDisplayName } from '../BackofficeAdminDisplayName';

class BackofficeAdminDisplayNameMock {
  static create(value: string): BackofficeAdminDisplayName {
    return new BackofficeAdminDisplayName(value);
  }

  static random(): BackofficeAdminDisplayName {
    return this.create(faker.internet.userName());
  }
}

export { BackofficeAdminDisplayNameMock as BackofficeAdminDisplayName };
