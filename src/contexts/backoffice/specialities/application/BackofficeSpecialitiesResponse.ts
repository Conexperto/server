import { BackofficeSpeciality } from '../domain/BackofficeSpeciality';

export class BackofficeSpecialitiesResponse {
  readonly specialities: Array<BackofficeSpeciality>;

  constructor(specialities: Array<BackofficeSpeciality>) {
    this.specialities = specialities;
  }
}
