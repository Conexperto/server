import { Body, Controller, Param, Put, ParseUUIDPipe } from '@nestjs/common';
import { CreateUserDTO } from '../dtos/CreateUserDTO';

@Controller({
  path: '/backoffice/users',
})
export class UsersPutController {
  @Put(':id')
  async create(
    @Param('id', ParseUUIDPipe) id: string,
    @Body() dto: CreateUserDTO,
  ) {
    console.log(id, dto);
    return {
      id,
      dto,
    };
  }
}
