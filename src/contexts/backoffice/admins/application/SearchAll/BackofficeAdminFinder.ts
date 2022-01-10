import { Injectable } from '@nestjs/common';
import { BackofficeSQLiteAdminRepository } from '../../infrastructure/persistence/BackofficeSQLiteAdminRepository';
import { BackofficeAdminsResponse } from '../BackofficeAdminsResponse';

@Injectable()
export class BackofficeAdminFinder {
  constructor(private readonly repository: BackofficeSQLiteAdminRepository) {}

  async run() {
    const admins = await this.repository.findAll();

    return new BackofficeAdminsResponse(admins);
  }
}
