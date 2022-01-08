import { Column, Entity, Index, PrimaryGeneratedColumn } from 'typeorm';
import { RoleAdminEnumType } from 'src/contexts/backoffice/admins/domain/RoleAdminTypeEnum';

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

  @Column()
  disabled: boolean;

  @Column('enum', { enum: RoleAdminEnumType })
  role: string;
}
