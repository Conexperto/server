import * as faker from 'faker';
import { BackofficeAdminPhotoURL } from '../BackofficeAdminPhotoURL';

class BackofficeAdminPhotoURLMock {
  static create(value: string): BackofficeAdminPhotoURL {
    return new BackofficeAdminPhotoURL(value);
  }

  static random(): BackofficeAdminPhotoURL {
    return this.create(faker.image.avatar());
  }
}

export { BackofficeAdminPhotoURLMock as BackofficeAdminPhotoURL }
