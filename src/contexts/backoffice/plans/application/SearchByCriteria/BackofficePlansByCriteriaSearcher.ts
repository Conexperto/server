import { Injectable } from '@nestjs/common';
import { Criteria } from 'src/contexts/shared/domain/criteria/Criteria';
import { Filters } from 'src/contexts/shared/domain/criteria/Filters';
import { Order } from 'src/contexts/shared/domain/criteria/Order';
import { BackofficeSQLitePlanRepository } from '../../infrastructure/persistence/BackofficeSQLitePlanRepository';
import { BackofficePlansResponse } from '../BackofficePlansResponse';

@Injectable()
export class BackofficePlansByCriteriaSearcher {
  constructor(private readonly repository: BackofficeSQLitePlanRepository) {}

  async run(
    filters: Filters,
    order?: Order,
    limit?: number,
    offset?: number,
  ): Promise<BackofficePlansResponse> {
    const criteria = new Criteria(filters, order, limit, offset);

    const plans = await this.repository.find(criteria);

    return new BackofficePlansResponse(plans);
  }
}
