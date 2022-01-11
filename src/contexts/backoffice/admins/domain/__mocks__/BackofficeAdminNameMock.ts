import * as faker from 'faker';
import { BackofficeAdminName } from '../BackofficeAdminName';

export class BackofficeAdminNameMock {
  static create(value: string): BackofficeAdminName {
    return new BackofficeAdminName(value);
  }

  static random(): BackofficeAdminName {
    return this.create(faker.name.firstName());
  }
}
