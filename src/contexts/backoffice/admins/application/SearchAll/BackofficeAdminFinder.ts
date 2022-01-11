import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { BackofficeSQLiteAdminRepository } from '../../infrastructure/persistence/BackofficeSQLiteAdminRepository';
import { BackofficeAdminsResponse } from '../BackofficeAdminsResponse';

@Injectable()
export class BackofficeAdminFinder {
  constructor(
    @InjectRepository(BackofficeSQLiteAdminRepository)
    private readonly repository: BackofficeSQLiteAdminRepository,
  ) {}

  async run() {
    const admins = await this.repository.findAll();

    return new BackofficeAdminsResponse(admins);
  }
}
