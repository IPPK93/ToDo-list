from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient
from pytest import LogCaptureFixture

import app
from app.logged_tasks_handler import LoggedTasksHandler
from app.page_indexer import PageIndexer
from app.tasks_handler import TasksHandler


@pytest.fixture()
def tasks_handler_fixture() -> TasksHandler:
    return TasksHandler()


@pytest.fixture()
def page_indexer_fixture() -> PageIndexer:
    return PageIndexer(10)


@pytest.fixture()
def logged_handler_fixture() -> LoggedTasksHandler:
    return LoggedTasksHandler('logs/tests.log')


@pytest.fixture()
def clear_tasks_handler() -> None:
    app.tasks_handler._tasks = {'active': [], 'finished': []}
    app.tasks_handler.set_state_default()


@pytest.fixture()
def app_fixture(
    monkeypatch: pytest.MonkeyPatch,
    logged_handler_fixture: LogCaptureFixture,
    clear_tasks_handler: None,
) -> Generator[Flask, None, None]:
    monkeypatch.setattr(app, 'tasks_handler', logged_handler_fixture)
    app.app.config.update(
        {
            'TESTING': True,
        }
    )
    app.app.jinja_env.trim_blocks = True
    app.app.jinja_env.lstrip_blocks = True

    yield app.app

    app.app.jinja_env.trim_blocks = False
    app.app.jinja_env.lstrip_blocks = False

    app.app.config.update(
        {
            'TESTING': False,
        }
    )


@pytest.fixture()
def client(app_fixture: Flask) -> FlaskClient:
    return app_fixture.test_client()
