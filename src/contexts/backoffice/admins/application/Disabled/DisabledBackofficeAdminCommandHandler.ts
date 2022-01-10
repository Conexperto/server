import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { BackofficeAdminDisabler } from './BackofficeAdminDisabler';
import { DisabledBackofficeAdminCommand } from './DisabledBackofficeAdminCommand';

@CommandHandler(DisabledBackofficeAdminCommand)
export class DisabledBackofficeAdminCommandHandler
  implements ICommandHandler<DisabledBackofficeAdminCommand>
{
  constructor(private disabler: BackofficeAdminDisabler) {}

  async execute(command: DisabledBackofficeAdminCommand) {
    let ids = [];

    if (Array.isArray(ids)) {
      ids = [...command.id];
    } else {
      ids = [command.id];
    }

    await this.disabler.run(ids);
  }
}
