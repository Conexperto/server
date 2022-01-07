import { IsEmail, IsString } from 'class-validator';

export class CreateUserDTO {
  @IsEmail()
  email: string;

  @IsString()
  displayName: string;

  @IsString()
  phoneNumber: string;

  @IsString()
  name: string;

  @IsString()
  lastname: string;
}
