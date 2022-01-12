import { BackofficeAdminRoles } from 'src/contexts/backoffice/admins/domain/BackofficeAdminRole';
import { Column, Entity, Index, PrimaryGeneratedColumn } from 'typeorm';

@Entity({
  name: 'cxp_admins',
  synchronize: true,
})
export class AdminEntity {
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

  @Column({ default: false })
  disabled: boolean;

  @Column({ type: 'simple-enum' })
  role: BackofficeAdminRoles;
}
