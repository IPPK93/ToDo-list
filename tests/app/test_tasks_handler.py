from typing import List

import pytest

from app.task import Task
from app.tasks_handler import TasksHandler


@pytest.mark.parametrize('status_', ['asd', 'lol', 'ALL', 'ACTIVE'])
def test_wrong_status_init(status_: str) -> None:
    with pytest.raises(ValueError):
        TasksHandler(status=status_)


@pytest.mark.parametrize('desc', ['ToDo1', 'ToDo2', 'ToDo3'])
def test_add_task(tasks_handler_fixture: TasksHandler, desc: str) -> None:
    tasks_handler_fixture.add_task(desc)
    assert tasks_handler_fixture._tasks['active'][-1].description == desc


@pytest.mark.parametrize(
    ('descs', 'indices'), [(['fst', 'snd', 'trd', 'frt'], [1, 1, 1])]
)
def test_finish_task(
    tasks_handler_fixture: TasksHandler, descs: List[str], indices: List[int]
) -> None:
    for desc in descs:
        tasks_handler_fixture.add_task(desc)

    tasks = []

    for idx in indices:
        task_description = tasks_handler_fixture.finish_task(idx)
        task = Task(task_description, is_active=False)
        tasks.append(task)
        assert task not in tasks_handler_fixture._tasks['active']

    assert tasks_handler_fixture._tasks['finished'] == tasks


@pytest.mark.parametrize('task_index', [1, 10, 100])
def test_finish_task_invalid_index(
    tasks_handler_fixture: TasksHandler, task_index: int
) -> None:
    tasks_handler_fixture.add_task('smth')

    with pytest.raises(IndexError):
        tasks_handler_fixture.finish_task(task_index)


@pytest.mark.parametrize(
    ('descs', 'indices', 'status_'),
    [
        (
            ['fst', 'snd', 'trd', 'frt', 'fft', 'sth', 'svn', 'eth'],
            [2, 1, 0],
            'finished',
        ),
        (['fst', 'snd', 'trd', 'frt', 'fft', 'sth', 'svn', 'eth'], [7, 6, 5], 'all'),
    ],
)
def test_delete_task(
    tasks_handler_fixture: TasksHandler,
    descs: List[str],
    indices: List[int],
    status_: str,
) -> None:
    for i, desc in enumerate(descs):
        tasks_handler_fixture.add_task(desc)
        if i % 2 == 0:
            tasks_handler_fixture.finish_task(0)

    tasks_handler_fixture.status = status_
    for idx in indices:
        task = tasks_handler_fixture.delete_task(idx)
        assert task not in tasks_handler_fixture._tasks['finished']


@pytest.mark.parametrize(
    ('descs', 'task_index', 'status_'),
    [(['fst', 'snd', 'trd'], 2, 'finished'), (['fst', 'snd', 'trd', 'frt'], 1, 'all')],
)
def test_delete_task_invalid_index(
    tasks_handler_fixture: TasksHandler, descs: List[str], task_index: int, status_: str
) -> None:
    for i, desc in enumerate(descs):
        tasks_handler_fixture.add_task(desc)
        if i % 2 == 0:
            tasks_handler_fixture.finish_task(0)

    tasks_handler_fixture.status = status_
    with pytest.raises(IndexError):
        tasks_handler_fixture.delete_task(task_index)


@pytest.mark.parametrize(
    ('descs', 'new_filter', 'expected'),
    [
        (['abcd', 'kekw', 'hehekekhehe'], 'kek', ['kekw', 'hehekekhehe']),
        (['not hehehe', 'lulz', '+rep'], 'lol', []),
        (
            ['bugagagaga', 'wahahahahahahaha', '-100 credits'],
            'wahahaha',
            ['wahahahahahahaha'],
        ),
        (['a', 'b', 'c', 'd'], '', ['a', 'b', 'c', 'd']),
    ],
)
def test_filterby_setter(
    tasks_handler_fixture: TasksHandler,
    descs: List[str],
    new_filter: str,
    expected: List[str],
) -> None:
    for desc in descs:
        tasks_handler_fixture.add_task(desc)

    tasks_handler_fixture.filterby = new_filter
    assert len(expected) == len(tasks_handler_fixture.requested_tasks)

    for i in range(len(expected)):
        assert expected[i] == tasks_handler_fixture.requested_tasks[i].description


@pytest.mark.parametrize('status_', ['asd', 'lol', 'ALL', 'ACTIVE'])
def test_status_setter_invalid_value(
    tasks_handler_fixture: TasksHandler, status_: str
) -> None:
    with pytest.raises(ValueError):
        tasks_handler_fixture.status = status_


@pytest.mark.parametrize('page', [2, 10, 100])
def test_page_setter_invalid_index(
    tasks_handler_fixture: TasksHandler, page: int
) -> None:
    with pytest.raises(IndexError):
        tasks_handler_fixture.page = page
