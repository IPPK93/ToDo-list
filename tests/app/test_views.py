from typing import List

import pytest
from flask.testing import FlaskClient

import app

testdata_descs = [
    ['ToDo1', 'ToDo2', 'ToDo3', 'ToDo4', 'ToDo5'],
    ['azxcvbdf', 'bgadczxc', 'cfasf', 'dasf'],
    ['HelpMe', 'ToD0', 'cfasf', 'dasf'],
]

testdata_longdescs = [
    testdata_descs[0] * 12,
    [
        'ToDo1',
        'ToDo5',
        'ToDo2',
        'ToDo3',
        'ToDo4',
        'HelpMe',
        'ToD0',
        'cfasf',
        'dasf',
        'asda',
        'azxcvbdf',
        'bgadczxc',
        'cfasf',
        'dasf',
        'kekw',
    ]
    * 5,
    testdata_descs[2] * 15,
]

testdata_indices = [[3, 2, 0], [2, 0, 1], [1, 1, 1]]

testdata_page = [1, 3, 5]

testdata_status = ['active', 'finished', 'all']

testdata_filterby = ['ToD', 'ktop', 'asf']


@pytest.mark.parametrize('task_descs', testdata_descs)
def test_tasks(client: FlaskClient, task_descs: List[str]) -> None:
    for i, task_desc in enumerate(task_descs):
        app.tasks_handler.add_task(task_desc)

    response = client.get('/tasks')
    for task_desc in task_descs:
        assert task_desc in str(response.data)

    assert response.status_code == 200


@pytest.mark.parametrize(
    ('task_descs', 'status_'), list(zip(testdata_descs, testdata_status))
)
def test_tasks_status(client: FlaskClient, task_descs: List[str], status_: str) -> None:
    for desc in task_descs:
        app.tasks_handler.add_task(desc)

    data = {'status': status_}
    response = client.get('/tasks', query_string=data)
    for desc in task_descs:
        if data['status'] == 'finished':
            assert desc not in str(response.data)
        else:
            assert desc in str(response.data)

    assert response.status_code == 200


@pytest.mark.parametrize(
    ('task_descs', 'filterby'), [*zip(testdata_descs, testdata_filterby)]
)
def test_tasks_filterby(
    client: FlaskClient, task_descs: List[str], filterby: str
) -> None:
    filterby_count = 1  # filterby 'value' in html would be filled by its value
    for desc in task_descs:
        app.tasks_handler.add_task(desc)
        if filterby in desc:
            filterby_count += 1

    data = {'filterby': filterby}
    response = client.get('/tasks', query_string=data)
    assert filterby_count == str(response.data).count(filterby)
    assert response.status_code == 200


@pytest.mark.parametrize(
    ('task_descs', 'page'), [*zip(testdata_longdescs, testdata_page)]
)
def test_tasks_page(client: FlaskClient, task_descs: List[str], page: int) -> None:
    for desc in task_descs:
        app.tasks_handler.add_task(desc)

    data = {'page': page}
    response = client.get('/tasks', query_string=data)

    assert app.tasks_handler.page == page
    assert response.status_code == 200


@pytest.mark.parametrize(('task_descs'), [*testdata_descs])
def test_add_tasks(client: FlaskClient, task_descs: List[str]) -> None:
    for desc in task_descs:
        data = {'task_description': desc}
        response = client.post('/add_task', data=data, follow_redirects=True)
        assert len(response.history) == 1
        assert response.request.path == '/tasks'
        assert response.status_code == 200

        assert desc in str(response.data)

    response = client.get('/tasks')
    for desc in task_descs:
        assert desc in str(response.data)

    response = client.get('/add_task')
    assert response.status_code == 200


@pytest.mark.parametrize(
    ('task_descs', 'indices'), [*zip(testdata_descs, testdata_indices)]
)
def test_finish_task(
    client: FlaskClient, task_descs: List[str], indices: List[int]
) -> None:
    for desc in task_descs:
        app.tasks_handler.add_task(desc)

    for idx in indices:
        app.tasks_handler.status = 'active'
        data = {'task_index': str(idx)}
        cur_desc = app.tasks_handler.requested_tasks[idx].description
        response = client.post('/finish_task', data=data, follow_redirects=True)

        assert len(response.history) == 1
        assert response.request.path == '/tasks'
        assert response.status_code == 200
        assert cur_desc not in str(response.data)

        app.tasks_handler.status = 'finished'
        response = client.get('/tasks')
        assert cur_desc in str(response.data)


@pytest.mark.parametrize(
    ('task_descs', 'indices'), [*zip(testdata_descs, testdata_indices)]
)
def test_delete_task(
    client: FlaskClient, task_descs: List[str], indices: List[int]
) -> None:
    for desc in task_descs:
        app.tasks_handler.add_task(desc)

    for _ in range(len(task_descs)):
        data = {'task_index': '0'}
        response = client.post('/finish_task', data=data)
        assert response.status_code == 302

    for idx in indices:
        app.tasks_handler.status = 'finished'
        data = {'task_index': str(idx)}
        cur_desc = app.tasks_handler.requested_tasks[idx].description
        response = client.post('/delete_task', data=data, follow_redirects=True)

        assert len(response.history) == 1
        assert response.request.path == '/tasks'
        assert response.status_code == 200
        assert cur_desc not in str(response.data)

        app.tasks_handler.status = 'all'
        response = client.get('/tasks')
        assert cur_desc not in str(response.data)


def test_main_page(client: FlaskClient) -> None:
    response = client.get('/main_page', follow_redirects=True)

    assert len(response.history) == 1
    assert response.request.path == '/tasks'
    assert response.status_code == 200
