from typing import List, Optional, Tuple

import pytest

from app.page_indexer import PageIndexer


@pytest.mark.parametrize(
    ('page', 'index', 'expected'), [(1, 9, 9), (2, 5, 15), (10, 7, 97), (25, 0, 240)]
)
def test_true_index(
    page_indexer_fixture: PageIndexer, page: int, index: int, expected: int
) -> None:
    result = page_indexer_fixture.true_index(page, index)
    assert result == expected


@pytest.mark.parametrize(
    ('arr_length', 'page', 'expected'),
    [(15, 1, (0, 10)), (27, 3, (20, None)), (1, 1, (0, None)), (100, 5, (40, 50))],
)
def test_end_indices(
    page_indexer_fixture: PageIndexer,
    arr_length: int,
    page: int,
    expected: Tuple[int, Optional[int]],
) -> None:
    result = page_indexer_fixture.end_indices(arr_length, page)
    assert result == expected


@pytest.mark.parametrize(
    ('cur_page', 'pages_num', 'expected'),
    [
        (3, 5, ['1', '2', '3', '4', '5']),
        (2, 6, ['1', '2', '3', '...', '6']),
        (6, 8, ['1', '...', '5', '6', '7', '8']),
        (5, 9, ['1', '...', '4', '5', '6', '...', '9']),
    ],
)
def test_get_pages_representation(
    page_indexer_fixture: PageIndexer,
    cur_page: int,
    pages_num: int,
    expected: List[str],
) -> None:
    result = page_indexer_fixture.get_pages_representation(cur_page, pages_num)
    assert result == expected


@pytest.mark.parametrize(
    ('arr_len', 'expected'),
    [
        (0, 1),
        (12, 2),
        (159, 16),
        (30, 3),
    ],
)
def test_pages_num(
    page_indexer_fixture: PageIndexer, arr_len: int, expected: int
) -> None:
    result = page_indexer_fixture.pages_num(arr_len)
    assert result == expected
