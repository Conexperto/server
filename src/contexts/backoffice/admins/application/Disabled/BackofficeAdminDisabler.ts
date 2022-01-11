import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { BackofficeAdminId } from '../../domain/BackofficeAdminId';
import { BackofficeSQLiteAdminRepository } from '../../infrastructure/persistence/BackofficeSQLiteAdminRepository';

@Injectable()
export class BackofficeAdminDisabler {
  constructor(
    @InjectRepository(BackofficeSQLiteAdminRepository)
    private readonly repository: BackofficeSQLiteAdminRepository,
  ) {}

  async run(adminId: BackofficeAdminId[]): Promise<void> {
    const ids = adminId.map((obj) => obj.value);
    await this.repository.disabled(ids);
  }
}
