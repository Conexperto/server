import * as faker from 'faker';
import { BackofficeAdminId } from '../BackofficeAdminId';

class BackofficeAdminIdMock {
  static create(value: string): BackofficeAdminId {
    return new BackofficeAdminId(value);
  }

  static random(): BackofficeAdminId {
    return this.create(faker.datatype.uuid());
  }
}

export { BackofficeAdminIdMock as BackofficeAdminId };
