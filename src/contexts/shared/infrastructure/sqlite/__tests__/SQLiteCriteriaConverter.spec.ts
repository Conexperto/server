import { Criteria } from 'src/contexts/shared/domain/criteria/Criteria';
import { Filter } from 'src/contexts/shared/domain/criteria/Filter';
import { FilterField } from 'src/contexts/shared/domain/criteria/FilterField';
import {
  FilterOperator,
  Operator,
} from 'src/contexts/shared/domain/criteria/FilterOperator';
import { Filters } from 'src/contexts/shared/domain/criteria/Filters';
import { FilterValue } from 'src/contexts/shared/domain/criteria/FilterValue';
import { Order } from 'src/contexts/shared/domain/criteria/Order';
import { OrderBy } from 'src/contexts/shared/domain/criteria/OrderBy';
import {
  OrderType,
  OrderTypes,
} from 'src/contexts/shared/domain/criteria/OrderType';
import { SQLiteCriteriaConverter } from '../SQLiteCriteraConverter';

describe('SQLiteCriteriaConverter', () => {
  it('should generate a query filter', () => {
    const filter = new Filter(
      new FilterField('email'),
      FilterOperator.fromValue('='),
      new FilterValue('jhondeo@mail.com'),
    );
    const order = new Order(new OrderBy('uid'), new OrderType(OrderTypes.ASC));
    const filters = new Filters([filter]);
    const criteria = new Criteria(filters, order);

    const converter = new SQLiteCriteriaConverter();

    const result = converter.convert(criteria);

    console.log(result);
  });
});
