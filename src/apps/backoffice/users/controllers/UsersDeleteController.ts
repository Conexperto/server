import { Controller, Delete, Param, ParseUUIDPipe } from '@nestjs/common';

@Controller({
  path: '/backoffice/users',
})
export class UsersDeleteController {
  @Delete(':id')
  async delete(@Param('id', ParseUUIDPipe) id: string) {
    console.log(id);
    return {
      id,
    };
  }
}
