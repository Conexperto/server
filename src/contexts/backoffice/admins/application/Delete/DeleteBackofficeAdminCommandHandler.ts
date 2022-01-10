import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { BackofficeAdminDeleter } from './BackofficeAdminDeleter';
import { DeleteBackofficeAdminCommand } from './DeleteBackofficeAdminCommand';

@CommandHandler(DeleteBackofficeAdminCommand)
export class DeleteBackofficeAdminCommandHandler
  implements ICommandHandler<DeleteBackofficeAdminCommand>
{
  constructor(private deleter: BackofficeAdminDeleter) {}

  async execute(command: DeleteBackofficeAdminCommand) {
    let ids = [];

    if (Array.isArray(ids)) {
      ids = [...command.id];
    } else {
      ids = [command.id];
    }

    await this.deleter.run(ids);
  }
}
