import { BackofficeSearchAdminsByCriteriaQuery } from '../BackofficeSearchAdminsByCriteriaQuery';

describe('BackofficeSearchAdminsByCriteriaQuery', () => {
  it('should search by criteria query', () => {
    const filter = new Map();
    filter.set('field', 'uid');
    filter.set('operator', '=');
    filter.set('value', 'uid');

    const orderBy = 'id';
    const orderType = 'ASC';
    const limit = 10;
    const offset = 0;
    const query = new BackofficeSearchAdminsByCriteriaQuery(
      [filter],
      orderBy,
      orderType,
      limit,
      offset,
    );

    expect(query).toBeInstanceOf(BackofficeSearchAdminsByCriteriaQuery);
    expect(query.filters).toEqual([filter]);
    expect(query.orderBy).toBe(orderBy);
    expect(query.orderType).toBe(orderType);
    expect(query.limit).toBe(limit);
    expect(query.offset).toBe(offset);
  });
});
