import shlex

from prettytable import PrettyTable
from prompt import string

from primitive_db import core, parser, utils
from primitive_db.constants import VALID_TYPES


def create_cacher():
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            print("(Из кэша)")
            return cache[key]
        result = value_func()
        cache[key] = result
        return result

    return cache_result


cache_select = create_cacher()


def print_help():
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя> <столбец1:тип> ... - создать таблицу")
    print("<command> list_tables - показать список таблиц")
    print("<command> drop_table <имя> - удалить таблицу")
    print("<command> insert into <имя> values (<значения>) - добавить запись")
    print("<command> select from <имя> [where <столбец> = <значение>] - прочитать")
    print(
        "<command> update <имя> set <столбец> = <значение> where <столбец> = <значение>"
    )
    print("<command> delete from <имя> where <столбец> = <значение>")
    print("<command> info <имя> - информация о таблице")
    print("<command> help - справка")
    print("<command> exit - выход\n")


def run():
    print("DB project is running!")
    metadata = utils.load_metadata()

    while True:
        try:
            user_input = string(">>>Введите команду: ")
            if not user_input.strip():
                continue

            args = shlex.split(user_input)
            cmd = args[0].lower()

            if cmd == "exit":
                break
            elif cmd == "help":
                print_help()
            elif cmd == "create_table":
                if len(args) < 3:
                    print("Некорректное значение: не указаны столбцы.")
                    continue

                table_name = args[1]
                columns = args[2:]

                valid = True
                for col in columns:
                    if ":" not in col:
                        print(f"Некорректное значение: {col}. Попробуйте снова.")
                        valid = False
                        break
                    _, dtype = col.split(":")
                    if dtype not in VALID_TYPES:
                        print(f"Некорректное значение: {col}. Попробуйте снова.")
                        valid = False
                        break

                if not valid:
                    continue

                metadata = core.create_table(metadata, table_name, columns)
                utils.save_metadata(metadata)
            elif cmd == "list_tables":
                if not metadata:
                    print("Таблиц нет.")
                for t in metadata:
                    print(f"- {t}")
            elif cmd == "drop_table":
                table_name = args[1]
                metadata = core.drop_table(metadata, table_name)
                utils.save_metadata(metadata)
            elif cmd == "insert":
                table_name = args[2]
                values_str = " ".join(args[4:])
                values = parser.parse_values(values_str)
                data = utils.load_table_data(table_name)
                data = core.insert(data, metadata, table_name, values)
                utils.save_table_data(table_name, data)
            elif cmd == "select":
                table_name = args[2]
                data = utils.load_table_data(table_name)

                if len(args) > 4 and args[3].lower() == "where":
                    cond_str = " ".join(args[4:])
                    where = parser.parse_condition(cond_str)
                    key = f"{table_name}_{where}"
                    result = cache_select(key, lambda: core.select(data, where))
                else:
                    result = core.select(data)

                if result:
                    table = PrettyTable()
                    table.field_names = [col["name"] for col in metadata[table_name]]
                    for row in result:
                        table.add_row([row[c["name"]] for c in metadata[table_name]])
                    print(table)
                else:
                    print("Записей не найдено.")
            elif cmd == "update":
                table_name = args[1]
                set_str = " ".join(args[3 : args.index("where")])
                where_str = " ".join(args[args.index("where") + 1 :])
                set_clause = parser.parse_condition(set_str)
                where_clause = parser.parse_condition(where_str)
                data = utils.load_table_data(table_name)
                data = core.update(data, set_clause, where_clause)
                utils.save_table_data(table_name, data)
            elif cmd == "delete":
                table_name = args[2]
                where_str = " ".join(args[4:])
                where_clause = parser.parse_condition(where_str)
                data = utils.load_table_data(table_name)
                data = core.delete(data, where_clause)
                utils.save_table_data(table_name, data)
            elif cmd == "info":
                table_name = args[1]
                if table_name in metadata:
                    cols = ", ".join(
                        [f"{c['name']}:{c['type']}" for c in metadata[table_name]]
                    )
                    print(f"Таблица: {table_name}")
                    print(f"Столбцы: {cols}")
                    data = utils.load_table_data(table_name)
                    print(f"Количество записей: {len(data)}")
                else:
                    print("Таблица не найдена.")
            else:
                print(f"Функции {cmd} нет. Попробуйте снова.")
        except IndexError:
            print("Ошибка: не хватает аргументов для команды.")
        except Exception as e:
            print(f"Ошибка: {e}")
