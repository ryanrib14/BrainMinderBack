from sqlalchemy import inspect
from sqlalchemy.engine import Row
from typing import Any


def tuple_to_model(model: Any, tuple_result: Any) -> Any:
    if tuple_result is None:
        return None

    model_instance = model()
    mapper = inspect(model_instance.__class__)

    # Ensure that tuple_result can be accessed like a dictionary
    if isinstance(tuple_result, Row):
        tuple_result = tuple_result._mapping

    for column in mapper.attrs:
        if column.key in tuple_result:
            setattr(model_instance, column.key, tuple_result[column.key])

    return model_instance


def generate_sql_update_set_args(update_info: dict) -> tuple[str, dict]:
    keys = []
    args = {}

    for key, value in update_info.items():
        keys.append(f"{key} = :{key}")
        args[key] = value

    set_string = ", ".join(keys)

    return set_string, args
