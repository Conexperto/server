import { Injectable } from '@nestjs/common';
import { BackofficeSQLitePlanRepository } from '../../infrastructure/persistence/BackofficeSQLitePlanRepository';
import { BackofficePlansResponse } from '../BackofficePlansResponse';

@Injectable()
export class BackofficePlanFinder {
  constructor(private readonly repository: BackofficeSQLitePlanRepository) {}

  async run(): Promise<BackofficePlansResponse> {
    const plans = await this.repository.findAll();

    return new BackofficePlansResponse(plans);
  }
}
