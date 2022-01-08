import convict from 'convict';

const BackOfficeConfigFactory = convict({
  env: {
    doc: 'The application environment.',
    format: ['production', 'development', 'staging', 'test'],
    default: 'default',
    env: 'NODE_ENV',
  },
  slite: {
    type: {
      doc: 'Database driver',
      format: String,
      env: 'DATABASE_DRIVER',
      default: 'sqlite',
    },
    database: {
      doc: 'Database name',
      format: String,
      env: 'DATABASE_NAME',
      default: 'cxp_db',
    },
    entities: {
      doc: 'Entites',
      format: Array,
      default: ['../entities/*{.ts,.js}'],
    },
    synchronize: {
      doc: 'Synchronize',
      format: Boolean,
      default: true,
      env: 'DATABASE_SYNCHRONIZE',
    },
  },
});

BackOfficeConfigFactory.loadFile([
  __dirname + '/default.json',
  __dirname + '/' + BackOfficeConfigFactory.get('env') + '.json',
]);

export default BackOfficeConfigFactory;
