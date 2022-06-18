from flask import Flask

from app.logged_tasks_handler import LoggedTasksHandler

app = Flask(__name__)
tasks_handler = LoggedTasksHandler(log_file='logs/app.log')


# pylint: disable=wrong-import-position

from app.views import tasks  # noqa: E402 F401

# pylint: enable=wrong-import-position

if __name__ == '__main__':
    app.run()
