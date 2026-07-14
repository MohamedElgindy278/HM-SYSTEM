from typing import Any, List, Optional, Tuple


def build_where_clause(conditions: List[Tuple[str, Optional[Any]]]) -> Tuple[str, list]:

    parts = []
    params = []

    for fragment, value in conditions:
        if value is not None:
            parts.append(fragment)
            params.append(value)

    where_clause = f"WHERE {' AND '.join(parts)}" if parts else ""

    return where_clause, params


def paginate(start_num: int, page_size: int) -> Tuple[int, int]:

    offset = max(start_num - 1, 0)

    return offset, page_size
