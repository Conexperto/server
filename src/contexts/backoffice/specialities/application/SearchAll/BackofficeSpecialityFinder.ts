import { Injectable } from '@nestjs/common';
import { BackofficeSQLiteSpecialityRepository } from '../../infrastructure/persistence/BackofficeSQLiteSpecialityRepository';
import { BackofficeSpecialitiesResponse } from '../BackofficeSpecialitiesResponse';

@Injectable()
export class BackofficeSpecialityFinder {
  constructor(
    private readonly repository: BackofficeSQLiteSpecialityRepository,
  ) {}

  async run(): Promise<BackofficeSpecialitiesResponse> {
    const methods = await this.repository.findAll();

    return new BackofficeSpecialitiesResponse(methods);
  }
}
