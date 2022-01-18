import { BackofficeMethod } from '../domain/BackofficeMethod';

export class BackofficeMethodsResponse {
  readonly methods: Array<BackofficeMethod>;

  constructor(methods: Array<BackofficeMethod>) {
    this.methods = methods;
  }
}
