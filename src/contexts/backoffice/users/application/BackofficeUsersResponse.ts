import { BackofficeUser } from '../domain/BackofficeUser';

export class BackofficeUsersResponse {
  readonly users: Array<BackofficeUser>;

  constructor(users: Array<BackofficeUser>) {
    this.users = users;
  }
}
