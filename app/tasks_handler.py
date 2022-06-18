from typing import Dict, List, Optional

from app.page_indexer import PageIndexer
from app.task import Task


class TasksHandler:
    def __init__(self, status: str = 'active'):
        if status not in ['active', 'finished', 'all']:
            raise ValueError("'status' is not one of 'active', 'finished', 'all'.")

        self._tasks: Dict[str, List[Task]] = {'active': [], 'finished': []}
        self._requested_tasks: List[Task] = []
        self._indexer = PageIndexer(tasks_per_page=10)
        self._status = status
        self._page = 0
        self._filter = ''
        self._indices: List[int] = []

    def set_state_default(self) -> None:
        self._status = 'active'
        self._page = 0
        self._filter = ''
        self._update_requested()

    def add_task(self, description: str) -> None:
        new_task = Task(description)
        self._tasks['active'].append(new_task)
        self._update_requested()

    def finish_task(self, task_index: int) -> str:
        true_index = self._indexer.true_index(self.page, task_index)

        if not 0 <= true_index < len(self._tasks['active']):
            raise IndexError('Invalid task index was given for task finishing.')

        task = self._tasks['active'].pop(self._indices[true_index])
        task.finish()

        self._tasks['finished'].append(task)

        self._update_requested()
        self._fix_page()

        return task.description

    def delete_task(self, task_index: int) -> str:
        list_index = self._indexer.true_index(self.page, task_index)
        if not 0 <= list_index < len(self._indices):
            raise IndexError('Invalid task index was given for task deletion.')

        true_index = self._indices[list_index]
        if self._status == 'all':
            true_index -= len(self._tasks['active'])

        if not 0 <= true_index < len(self._tasks['finished']):
            raise IndexError('Invalid task index was given for task deletion.')

        task = self._tasks['finished'].pop(true_index)

        self._update_requested()
        self._fix_page()

        return task.description

    def _update_requested(self) -> None:
        if self._status != 'all':
            self._requested_tasks = self._tasks[self._status]
        else:
            self._requested_tasks = [*self._tasks['active'], *self._tasks['finished']]

        req_tasks = self._requested_tasks
        if self._filter != '':
            self._indices = [
                idx
                for idx in range(len(req_tasks))
                if self._filter in req_tasks[idx].description
            ]
            self._requested_tasks = [
                self._requested_tasks[idx] for idx in self._indices
            ]
        else:
            self._indices = list(range(len(self._requested_tasks)))

    @property
    def requested_tasks(self) -> List[Task]:
        page_begin, page_end = self._indexer.end_indices(
            len(self._requested_tasks), self.page
        )
        return self._requested_tasks[page_begin:page_end]

    @property
    def filterby(self) -> Optional[str]:
        if self._filter == '':
            return None
        return self._filter

    @filterby.setter
    def filterby(self, new_filter: str) -> None:
        if self._filter != new_filter:
            self._filter = new_filter
            self._page = 0
            self._update_requested()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, new_status: str) -> None:
        if new_status not in ['active', 'finished', 'all']:
            raise ValueError("'status' is not one of 'active', 'finished', 'all'.")

        if self._status != new_status:
            self._status = new_status
            self._page = 0
            self._update_requested()

    @property
    def page(self) -> int:
        return self._page + 1

    @page.setter
    def page(self, new_page: int) -> None:
        if not 0 < new_page <= self.pages_num():
            raise IndexError('Invalid page number.')

        if self.page != new_page:
            self._page = new_page - 1

    def _fix_page(self) -> None:
        self.page = min(self.page, self.pages_num())

    def pages_num(self) -> int:
        req_tasks_len = len(self._requested_tasks)
        return self._indexer.pages_num(req_tasks_len)

    def pages_representation(self) -> List[str]:
        return self._indexer.get_pages_representation(self.page, self.pages_num())
