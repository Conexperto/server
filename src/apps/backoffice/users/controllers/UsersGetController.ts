import { Controller, Get, Param, ParseUUIDPipe } from '@nestjs/common';

@Controller({
  path: '/backoffice/users',
})
export class UsersGetController {
  @Get(':id')
  async findById(@Param('id', ParseUUIDPipe) id: string) {
    console.log(id);
    return { id };
  }

  @Get(':search')
  async findAll(@Param('search') search: string) {
    console.log(search);
    return [];
  }
}
