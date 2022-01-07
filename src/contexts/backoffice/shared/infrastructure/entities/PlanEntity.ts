import { Column, Entity, Index, PrimaryGeneratedColumn } from "typeorm";


@Entity({
	name: 'cxp_plan',
	orderBy: { id: 'DESC'},
	synchronize: true
})
export class PlanEntity {
	@PrimaryGeneratedColumn()
	id: number;

	@Column('uuid')
	@Index({ unique: true})
	uid: string;

	@Column()
	duration: number;

	@Column()
	price: number;

	@Column()
	coin: string;

	@Column()
	disabled: boolean;
}
