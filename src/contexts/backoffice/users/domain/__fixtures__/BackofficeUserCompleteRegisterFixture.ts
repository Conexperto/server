import * as faker from 'faker';
import { BackofficeUserCompleteRegister } from '../BackofficeUserCompleteRegister';

export class BackofficeUserCompleRegisterFixture {
  static create(value: boolean): BackofficeUserCompleteRegister {
    return new BackofficeUserCompleteRegister(value);
  }

  static random(): BackofficeUserCompleteRegister {
    return this.create(faker.random.boolean());
  }
}
