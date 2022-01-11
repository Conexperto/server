import * as faker from 'faker';
import { BackofficeAdminId } from '../BackofficeAdminId';

export class BackofficeAdminIdMock {
  static create(value: string): BackofficeAdminId {
    return new BackofficeAdminId(value);
  }

  static random(): BackofficeAdminId {
    return this.create(faker.random.uuid());
  }
}
