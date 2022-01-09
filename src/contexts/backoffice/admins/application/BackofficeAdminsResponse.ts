import { BackofficeAdmin } from '../domain/BackofficeAdmin';

export class BackofficeAdminsResponse {
  readonly admins: Array<BackofficeAdmin>;

  constructor(admins: Array<BackofficeAdmin>) {
    this.admins = admins;
  }
}
