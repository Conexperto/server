import { Column, Entity, Index, PrimaryGeneratedColumn } from 'typeorm';

@Entity({
  name: 'cxp_users',
  orderBy: { id: 'DESC' },
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

  @Column()
  disabled: boolean;

  @Column()
  ratingAverage: number;

  @Column('array')
  ratingStars: [number];

  @Column()
  ratingVotes: number;

  @Column()
  headline: string;

  @Column()
  aboutMe: string;

  @Column()
  sessionTaken: number;

  @Column()
  completeRegister: boolean;

  @Column()
  timezone: string;

  @Column()
  linkVideo: string;

  @Column()
  location: string;

  plans: [];

  specialities: [];

  methods: [];
}
