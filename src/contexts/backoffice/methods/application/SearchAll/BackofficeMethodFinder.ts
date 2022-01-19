import { Injectable } from '@nestjs/common';
import { BackofficeSQLiteMethodRepository } from '../../infrasctructure/persistence/BackofficeSQLiteMethodRepository';
import { BackofficeMethodsResponse } from '../BackofficeMethodsResponse';

@Injectable()
export class BackofficeMethodFinder {
  constructor(private readonly repository: BackofficeSQLiteMethodRepository) {}

  async run(): Promise<BackofficeMethodsResponse> {
    const methods = await this.repository.findAll();

    return new BackofficeMethodsResponse(methods);
  }
}
