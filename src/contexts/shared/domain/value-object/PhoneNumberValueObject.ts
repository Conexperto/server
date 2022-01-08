import { isPhoneNumber } from 'class-validator';
import { InvalidArgumentError } from './InvalidArgumentError';
import { StringValueObject } from './StringValueObject';

export class PhoneNumberValueObject extends StringValueObject {
  constructor(value: string) {
    super(value);
    this.ensureIsValidPhoneNumber(value);
  }

  private ensureIsValidPhoneNumber(value: string): void {
    if (!isPhoneNumber(value)) {
      throw new InvalidArgumentError(
        `<${this.constructor.name}> doest not allow the value <${value}>`,
      );
    }
  }
}
