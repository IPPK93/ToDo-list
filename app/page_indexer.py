from typing import List, Optional, Tuple


class PageIndexer:
    def __init__(self, tasks_per_page: int):
        self._tasks_per_page = tasks_per_page

    def true_index(self, page: int, index: int) -> int:
        return (page - 1) * self._tasks_per_page + index

    def end_indices(self, arr_length: int, page: int) -> Tuple[int, Optional[int]]:
        page_begin = (page - 1) * self._tasks_per_page

        if page_begin + self._tasks_per_page <= arr_length:
            page_end = page_begin + self._tasks_per_page
        else:
            page_end = None
        return page_begin, page_end

    @staticmethod
    def get_pages_representation(cur_page: int, pages_num: int) -> List[str]:
        pages_repr = []

        # Getting representation of the left to the cur_page part
        if cur_page - 1 < 4:
            left = [str(i) for i in range(1, cur_page)]
        else:
            left = ['1', '...', str(cur_page - 1)]
        pages_repr.extend(left)

        # Getting representation of cur_page
        pages_repr.append(str(cur_page))

        # Getting representation of the right to the cur_page part
        if pages_num - cur_page < 4:
            right = [str(i) for i in range(cur_page + 1, pages_num + 1)]
        else:
            right = [str(cur_page + 1), '...', str(pages_num)]
        pages_repr.extend(right)

        return pages_repr

    def pages_num(self, arr_len: int) -> int:
        return max(
            1, arr_len // self._tasks_per_page + (arr_len % self._tasks_per_page > 0)
        )
