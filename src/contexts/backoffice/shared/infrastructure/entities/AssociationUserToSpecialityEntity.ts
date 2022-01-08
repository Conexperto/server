import { Entity, ManyToOne } from 'typeorm';
import { SpecialityEntity } from './SpecialityEntity';
import { UserEntity } from './UserEntity';

@Entity({
  name: 'cxp_association_user_to_speciality',
  synchronize: true,
})
export class AssociationUserToSpecialityEntity {
  @ManyToOne(() => UserEntity, (user) => user.id)
  user: UserEntity;

  @ManyToOne(() => SpecialityEntity, (speciality) => speciality.id)
  speciality: SpecialityEntity;
}
