import { EnumValueObject } from 'src/contexts/shared/domain/value-object/EnumValueObject';
import { InvalidArgumentError } from 'src/contexts/shared/domain/value-object/InvalidArgumentError';

export enum AdminRoles {
  SuperRoot = 0,
  Root = 1,
  Admin = 2,
  User = 3,
}

export class AdminRole extends EnumValueObject<AdminRoles> {
  constructor(value: AdminRoles) {
    super(value, Object.values(AdminRoles) as AdminRoles[]);
  }

  static fromValue(value: number): AdminRole {
    switch (value) {
      case AdminRoles.SuperRoot:
        return new AdminRole(AdminRoles.SuperRoot);
      case AdminRoles.Root:
        return new AdminRole(AdminRoles.Root);
      case AdminRoles.Admin:
        return new AdminRole(AdminRoles.Admin);
      case AdminRoles.User:
        return new AdminRole(AdminRoles.User);
      default:
        throw new InvalidArgumentError(`The role type ${value} is invalid`);
    }
  }

  public isSuperRoot(): boolean {
    return this.value === AdminRoles.SuperRoot;
  }

  public isRoot(): boolean {
    return this.value === AdminRoles.Root;
  }

  public isAdmin(): boolean {
    return this.value === AdminRoles.Admin;
  }

  public isUser(): boolean {
    return this.value === AdminRoles.User;
  }

  protected throwErrorForInvalidValue(value: AdminRoles): void {
    throw new InvalidArgumentError(`The role type ${value} is invalid`);
  }
}
