import { BackofficeSpeciality } from '../domain/BackofficeSpeciality';

export class BackofficeSpeciakitiesResponse {
  readonly specialities: Array<BackofficeSpeciality>;

  constructor(specialities: Array<BackofficeSpeciality>) {
    this.specialities = specialities;
  }
}
