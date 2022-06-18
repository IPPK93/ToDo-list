import pytest
from pytest import LogCaptureFixture

from app.logged_tasks_handler import LoggedTasksHandler


@pytest.mark.parametrize('status_', ['not hehehe', 'howdy', 'some status'])
def test_incorrect_status(caplog: LogCaptureFixture, status_: str) -> None:
    LoggedTasksHandler('logs/tests.log', status_)
    assert (
        "'status' is not one of 'active', 'finished', 'all'."
        " Setting status to 'active'." in caplog.text
    )


@pytest.mark.parametrize('desc', ['uwuwuwuwu', 'not hehehe', 'howdy'])
def test_add_task(
    caplog: LogCaptureFixture, logged_handler_fixture: LoggedTasksHandler, desc: str
) -> None:
    logged_handler_fixture.add_task(desc)
    assert f"Task '{desc}' added" in caplog.text


@pytest.mark.parametrize('index_', [19, 29, 384])
def test_finish_task_invalid_index(
    caplog: LogCaptureFixture, logged_handler_fixture: LoggedTasksHandler, index_: int
) -> None:
    logged_handler_fixture.finish_task(index_)
    assert 'Invalid task index was given for task finishing.' in caplog.text


@pytest.mark.parametrize('index_', [19, 29, 384])
def test_delete_task_invalid_index(
    caplog: LogCaptureFixture, logged_handler_fixture: LoggedTasksHandler, index_: int
) -> None:
    logged_handler_fixture.status = 'all'
    logged_handler_fixture.delete_task(index_)
    assert 'Invalid task index was given for task deletion.' in caplog.text


@pytest.mark.parametrize('status_', ['not hehehe', 'howdy', 'some status'])
def test_status_setter_invalid_value(
    caplog: LogCaptureFixture, logged_handler_fixture: LoggedTasksHandler, status_: str
) -> None:
    logged_handler_fixture.status = status_
    assert "'status' is not one of 'active', 'finished', 'all'." in caplog.text


@pytest.mark.parametrize('page', [2, 5, 10])
def test_page_setter_invalid_index(
    caplog: LogCaptureFixture, logged_handler_fixture: LoggedTasksHandler, page: int
) -> None:
    logged_handler_fixture.page = page
    assert 'Invalid page number.' in caplog.text
