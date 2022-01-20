import { Injectable } from '@nestjs/common';
import { Criteria } from 'src/contexts/shared/domain/criteria/Criteria';
import { Filters } from 'src/contexts/shared/domain/criteria/Filters';
import { Order } from 'src/contexts/shared/domain/criteria/Order';
import { BackofficeSQLiteSpecialityRepository } from '../../infrastructure/persistence/BackofficeSQLiteSpecialityRepository';
import { BackofficeSpecialitiesResponse } from '../BackofficeSpecialitiesResponse';

@Injectable()
export class BackofficeSpecialitiesByCriteriaSearcher {
  constructor(
    private readonly repository: BackofficeSQLiteSpecialityRepository,
  ) {}

  async run(
    filters: Filters,
    order?: Order,
    limit?: number,
    offset?: number,
  ): Promise<BackofficeSpecialitiesResponse> {
    const criteria = new Criteria(filters, order, limit, offset);

    const speciliaties = await this.repository.find(criteria);

    return new BackofficeSpecialitiesResponse(speciliaties);
  }
}
