import { BackofficePlan } from '../domain/BackofficePlan';

export class BackofficeMethodsResponse {
  readonly plans: Array<BackofficePlan>;

  constructor(plans: Array<BackofficePlan>) {
    this.plans = plans;
  }
i
