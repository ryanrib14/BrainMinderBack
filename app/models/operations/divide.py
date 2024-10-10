from sqlalchemy import Column, Float, MetaData, TIMESTAMP
from alembic_utils.pg_trigger import PGTrigger
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_extension import PGExtension
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

Base = declarative_base(metadata=MetaData(schema="iag"))


class DivideOperation(Base):  # type: ignore
    __tablename__ = "divide_operations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.iag.uuid_generate_v4(),
        index=True,
    )
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    result = Column(Float, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=None)
    deleted_at = Column(TIMESTAMP(timezone=True), server_default=None)


update_divide_operations_modtime = PGTrigger(
    schema="iag",
    signature="update_divide_operations_modtime",
    on_entity="iag.divide_operations",
    is_constraint=False,
    definition="""
    BEFORE UPDATE ON divide_operations
    FOR EACH ROW EXECUTE FUNCTION iag.update_updated_at_column();
    """,
)


# general use
update_updated_at_column = PGFunction(
    schema="iag",
    signature="update_updated_at_column()",
    definition="""
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    """,
)
uuid_ossp = PGExtension(
    schema="iag",
    signature="uuid-ossp",
)
