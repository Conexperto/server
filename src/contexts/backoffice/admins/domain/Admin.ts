import { AggregateRoot } from '@nestjs/cqrs';
import { AdminDisplayName } from './AdminDisplayName';
import { AdminEmail } from './AdminEmail';
import { AdminId } from './AdminId';
import { AdminLastname } from './AdminLastname';
import { AdminName } from './AdminName';
import { AdminPhoneNumber } from './AdminPhoneNumber';
import { AdminPhotoURL } from './AdminPhotoURL';
import { AdminRole } from './AdminRole';

export class Admin extends AggregateRoot {
  constructor(
    private readonly id: AdminId,
    private readonly email: AdminEmail,
    private readonly displayName: AdminDisplayName,
    private readonly phoneNumber: AdminPhoneNumber,
    private readonly photoURL: AdminPhotoURL,
    private readonly name: AdminName,
    private readonly lastname: AdminLastname,
    private readonly role: AdminRole,
  ) {
    super();
  }

  static fromPrimitives(plainData: {
    id: string;
    email: string;
    displayName: string;
    phoneNumber: string;
    photoURL: string;
    name: string;
    lastname: string;
    role: number;
  }): Admin {
    return new Admin(
      new AdminId(plainData.id),
      new AdminEmail(plainData.email),
      new AdminDisplayName(plainData.displayName),
      new AdminPhoneNumber(plainData.phoneNumber),
      new AdminPhotoURL(plainData.photoURL),
      new AdminName(plainData.name),
      new AdminLastname(plainData.lastname),
      new AdminRole(plainData.role),
    );
  }

  toPrimitives() {
    return {
      id: this.id.value,
      email: this.email.value,
      displayName: this.displayName.value,
      phoneNumber: this.phoneNumber.value,
      photoURL: this.photoURL.value,
      name: this.name.value,
      lastname: this.lastname.value,
      role: this.role.value,
    };
  }
}
