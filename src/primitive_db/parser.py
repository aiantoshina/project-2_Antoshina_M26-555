def parse_values(values_str):
    """Парсит строку вида ('Ivan', 25, true) в список."""
    values_str = values_str.strip("()")
    # Простой парсер, разделяет по запятым, игнорируя кавычки
    values = [v.strip().strip("'\"") for v in values_str.split(",")]
    return values


def parse_condition(cond_str):
    """Парсит 'age = 28' в ('age', '28')."""
    parts = [p.strip() for p in cond_str.split("=")]
    if len(parts) != 2:
        raise ValueError("Некорректное условие")
    return parts[0], parts[1].strip("'\"")
