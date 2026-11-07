import shlex
from prompt import string
from prettytable import PrettyTable
from primitive_db import core, parser, utils

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
    print("<command> update <имя> set <столбец> = <значение> where <столбец> = <значение>")
    print("<command> delete from <имя> where <столбец> = <значение>")
    print("<command> info <имя> - информация о таблице")
    print("<command> help - справка")
    print("<command> exit - выход\n")