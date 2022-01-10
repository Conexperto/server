export class CreateBackofficeAdminCommand {
  public readonly id: string;
  public readonly email: string;
  public readonly displayName: string;
  public readonly phoneNumber: string;
  public readonly photoURL: string;
  public readonly name: string;
  public readonly lastname: string;
  public readonly role: number;

  constructor({
    id,
    email,
    displayName,
    phoneNumber,
    photoURL,
    name,
    lastname,
    role,
  }: {
    id: string;
    email: string;
    displayName: string;
    phoneNumber: string;
    photoURL: string;
    name: string;
    lastname: string;
    role: number;
  }) {
    this.id = id;
    this.email = email;
    this.displayName = displayName;
    this.phoneNumber = phoneNumber;
    this.photoURL = photoURL;
    this.name = name;
    this.lastname = lastname;
    this.role = role;
  }
}
