from primitive_db.decorators import handle_db_errors, confirm_action
from primitive_db.constants import VALID_TYPES

@handle_db_errors
def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata
    
    parsed_columns = [{"name": "ID", "type": "int"}]
    for col in columns:
        if ":" not in col:
            raise ValueError(f"Некорректное значение: {col}")
        name, dtype = col.split(":")
        if dtype not in VALID_TYPES:
            raise ValueError(f"Недопустимый тип {dtype}")
        parsed_columns.append({"name": name, "type": dtype})
    
    metadata[table_name] = parsed_columns
    cols_str = ", ".join([f"{c['name']}:{c['type']}" for c in parsed_columns])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {cols_str}')
    return metadata

@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        raise KeyError(table_name)
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata