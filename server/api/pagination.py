def pg_offset(limit, page) -> int:
    """Вычисляем offset пагинации для SQL."""
    return (page - 1) * limit
