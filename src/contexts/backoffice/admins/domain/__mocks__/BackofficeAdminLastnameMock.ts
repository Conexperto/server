import * as faker from 'faker';
import { BackofficeAdminLastname } from '../BackofficeAdminLastname';

export class BackofficeAdminLastnameMock {
  static create(value: string): BackofficeAdminLastname {
    return new BackofficeAdminLastname(value);
  }

  static random(): BackofficeAdminLastname {
    return this.create(faker.name.lastName());
  }
}
