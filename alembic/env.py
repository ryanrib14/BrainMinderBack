from alembic_utils.replaceable_entity import register_entities
from sqlalchemy import engine_from_config, MetaData
from sqlalchemy import pool, text
from alembic import context
from app.config.constants import POSTGRES_URL
from app.models.operations.divide import (
    Base,
    update_updated_at_column,
    uuid_ossp,
    update_divide_operations_modtime,
)

MY_SCHEMA = "iag"


## change this according to your models
target_metadata = Base.metadata
## change this according to what functions, extensions, triggers you want to use in autogenerate
register_entities([update_updated_at_column, uuid_ossp])

cmd_kwargs = context.get_x_argument(as_dictionary=True)


config = {"sqlalchemy.url": POSTGRES_URL}


# control the operation to be performed
if "op" in cmd_kwargs:
    if cmd_kwargs["op"] == "create_schema":
        target_metadata = MetaData(schema=MY_SCHEMA)
        register_entities([])
    elif cmd_kwargs["op"] == "create_extension":
        register_entities([update_updated_at_column, uuid_ossp])
        target_metadata = MetaData(schema=MY_SCHEMA)
    elif cmd_kwargs["op"] == "create_trigger":
        target_metadata = target_metadata
        register_entities(
            [update_updated_at_column, uuid_ossp, update_divide_operations_modtime]
        )
    elif cmd_kwargs["op"] == "default":
        target_metadata = Base.metadata
        register_entities(
            [update_updated_at_column, uuid_ossp, update_divide_operations_modtime]
        )
    else:
        raise Exception(f'Unsupported operation: {cmd_kwargs["op"]}')


def include_object(object, name, type_, reflected, compare_to) -> bool:
    if type_ == "table" and object.schema != MY_SCHEMA:
        return False
    return True


def include_name(name, type_, parent_names):
    if type_ == "schema":
        # note this will not include the default schema
        return name in ["iag"]
    else:
        return True


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = engine_from_config(
        config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            include_name=include_name,
            version_table_schema=target_metadata.schema,
        )
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS iag"))
        with context.begin_transaction():
            context.run_migrations()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
