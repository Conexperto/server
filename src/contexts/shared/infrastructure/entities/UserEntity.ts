import {
  Column,
  Entity,
  Index,
  JoinColumn,
  OneToMany,
  OneToOne,
  PrimaryGeneratedColumn,
} from 'typeorm';
import { AssociationUserToMethodEntity } from './AssociationUserToMethodEntity';
import { AssociationUserToSpecialityEntity } from './AssociationUserToSpecialityEntity';
import { MethodEntity } from './MethodEntity';
import { PlanEntity } from './PlanEntity';
import { SpecialityEntity } from './SpecialityEntity';
import { UserExpertEntity } from './UserExpertEntity';
import { UserRatingEntity } from './UserRatingEntity';

@Entity({
  name: 'cxp_users',
  synchronize: true,
})
export class UserEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @Column('uuid')
  @Index({ unique: true })
  uid: string;

  @Column()
  displayName: string;

  @Column()
  email: string;

  @Column()
  phoneNumber: string;

  @Column()
  photoURL: string;

  @Column()
  name: string;

  @Column()
  lastname: string;

  @Column({ default: true })
  disabled: boolean;

  @Column()
  sessionTaken: number;

  @Column()
  completeRegister: boolean;

  @Column()
  timezone: string;

  @Column()
  location: string;

  @OneToOne(() => UserRatingEntity, { onDelete: 'CASCADE' })
  @JoinColumn()
  rating: UserRatingEntity;

  @OneToOne(() => UserExpertEntity, { onDelete: 'CASCADE' })
  @JoinColumn()
  expert: UserExpertEntity;

  @OneToMany(
    () => AssociationUserToSpecialityEntity,
    (assocSpeciality) => assocSpeciality.speciality,
    { onDelete: 'CASCADE' },
  )
  specialities: SpecialityEntity[];

  @OneToMany(
    () => AssociationUserToMethodEntity,
    (assocMethod) => assocMethod,
    { onDelete: 'CASCADE' },
  )
  methods: AssociationUserToMethodEntity[];

  @OneToMany(() => PlanEntity, (plan) => plan.id, { onDelete: 'CASCADE' })
  plans: PlanEntity[];
}
