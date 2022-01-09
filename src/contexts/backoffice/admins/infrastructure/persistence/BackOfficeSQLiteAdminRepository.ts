import { Injectable } from '@nestjs/common';
import { AdminEntity } from 'src/contexts/backoffice/shared/infrastructure/entities/AdminEntity';
import { Repository } from 'typeorm';
import { Admin } from '../../domain/Admin';
import { AdminId } from '../../domain/AdminId';

@Injectable()
export class BackOfficeSQLiteAdminRepository {
  constructor(private readonly repository: Repository<AdminEntity>) {}

  async save(admin: Admin): Promise<void> {
    const {
      id,
      email,
      displayName,
      phoneNumber,
      photoURL,
      name,
      lastname,
      role,
    } = admin.toPrimitives();
    const entity = new AdminEntity();

    entity.uid = id;
    entity.email = email;
    entity.displayName = displayName;
    entity.phoneNumber = phoneNumber;
    entity.photoURL = photoURL;
    entity.name = name;
    entity.lastname = lastname;
    entity.role = role;

    await this.repository.save(entity);
  }

  async findById(id: AdminId): Promise<Admin> {
    const entity = await this.repository.findOne({ uid: id.value });
    return Admin.fromPrimitives({
      id: entity.uid,
      email: entity.email,
      displayName: entity.displayName,
      phoneNumber: entity.phoneNumber,
      photoURL: entity.photoURL,
      name: entity.name,
      lastname: entity.lastname,
      role: entity.role,
    });
  }

  async findOne(): Promise<Admin> {
    const entity = await this.repository.findOne();

    return Admin.fromPrimitives({
      id: entity.uid,
      email: entity.email,
      displayName: entity.displayName,
      phoneNumber: entity.phoneNumber,
      photoURL: entity.photoURL,
      name: entity.name,
      lastname: entity.lastname,
      role: entity.role,
    });
  }

  async find() {
    const entities = await this.repository.find({});

    return entities.map((entity) =>
      Admin.fromPrimitives({
        id: entity.uid,
        email: entity.email,
        displayName: entity.displayName,
        phoneNumber: entity.phoneNumber,
        photoURL: entity.photoURL,
        name: entity.name,
        lastname: entity.lastname,
        role: entity.role,
      }),
    );
  }
}
