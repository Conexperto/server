import * as faker from 'faker';
import { BackofficeAdminPhoneNumber } from '../BackofficeAdminPhoneNumber';

class BackofficeAdminPhoneNumberMock {
  static create(value: string): BackofficeAdminPhoneNumber {
    return new BackofficeAdminPhoneNumber(value);
  }

  static random(): BackofficeAdminPhoneNumber {
    return this.create(faker.phone.phoneNumber());
  }
}

export { BackofficeAdminPhoneNumberMock as BackofficeAdminPhoneNumber }
