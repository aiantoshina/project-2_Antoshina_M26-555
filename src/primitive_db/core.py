from primitive_db.constants import VALID_TYPES
from primitive_db.decorators import confirm_action, handle_db_errors


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


@handle_db_errors
def insert(table_data, metadata, table_name, values):
    if table_name not in metadata:
        raise KeyError(table_name)
    if table_data is None:
        table_data = []
    columns = metadata[table_name][1:]
    if len(values) != len(columns):
        raise ValueError(f"Ожидалось {len(columns)} значений, получено {len(values)}")

    new_id = 1
    if table_data:
        new_id = max(row["ID"] for row in table_data) + 1

    row = {"ID": new_id}
    for i, col in enumerate(columns):
        val = values[i]
        if col["type"] == "int":
            val = int(val)
        elif col["type"] == "bool":
            val = val.lower() in ["true", "1", "да"]
        row[col["name"]] = val

    table_data.append(row)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data


@handle_db_errors
def select(table_data, where_clause=None):
    if not where_clause:
        return table_data
    col, val = where_clause
    filtered = [row for row in table_data if str(row.get(col)) == str(val)]
    return filtered


@handle_db_errors
def update(table_data, set_clause, where_clause):
    col_w, val_w = where_clause
    col_s, val_s = set_clause
    updated = False
    for row in table_data:
        if str(row.get(col_w)) == str(val_w):
            row[col_s] = val_s
            updated = True
    if updated:
        print("Записи успешно обновлены.")
    else:
        print("Записи для обновления не найдены.")
    return table_data


@handle_db_errors
@confirm_action("удаление записей")
def delete(table_data, where_clause):
    col, val = where_clause
    initial_len = len(table_data)
    table_data[:] = [row for row in table_data if str(row.get(col)) != str(val)]
    deleted_count = initial_len - len(table_data)
    print(f"Удалено записей: {deleted_count}")
    return table_data
