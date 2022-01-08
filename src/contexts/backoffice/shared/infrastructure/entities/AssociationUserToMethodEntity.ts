import { Entity, ManyToOne } from 'typeorm';
import { MethodEntity } from './MethodEntity';
import { UserEntity } from './UserEntity';

@Entity({
  name: 'cxp_association_user_to_method',
  synchronize: true,
})
export class AssociationUserToMethodEntity {
  @ManyToOne(() => UserEntity, (user) => user.id)
  user: UserEntity;

  @ManyToOne(() => MethodEntity, (method) => method.id)
  method: MethodEntity;
}
