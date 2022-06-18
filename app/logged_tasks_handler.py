import logging
from pathlib import Path

from app.tasks_handler import TasksHandler


class LoggedTasksHandler(TasksHandler):
    def __init__(self, log_file: str, status: str = 'active'):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.init_logger(log_file)

        try:
            super().__init__(status)
        except ValueError as e:
            self.logger.error("%s Setting status to 'active'.", e)
            super().__init__('active')

    def init_logger(self, log_file: str) -> None:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        self.logger.addHandler(fh)

    def add_task(self, description: str) -> None:
        super().add_task(description)
        self.logger.info("Task '%s' added.", description)

    def finish_task(self, task_index: int) -> str:
        task_description = ''
        try:
            task_description = super().finish_task(task_index)
            self.logger.info(
                "Task '%s' finished. It's now moved to finished tasks.",
                task_description,
            )
        except IndexError as e:
            self.logger.warning('%s', e)
        return task_description

    def delete_task(self, task_index: int) -> str:
        task_description = ''
        try:
            task_description = super().delete_task(task_index)
            self.logger.info("Task '%s' deleted.", task_description)
        except IndexError as e:
            self.logger.warning('%s', e)
        return task_description

    @TasksHandler.status.setter  # type: ignore[attr-defined]
    def status(self, new_status: str) -> None:
        try:
            TasksHandler.status.fset(self, new_status)  # type: ignore[attr-defined]
        except ValueError as e:
            self.logger.warning('%s', e)

    @TasksHandler.page.setter  # type: ignore[attr-defined]
    def page(self, new_page: int) -> None:
        try:
            TasksHandler.page.fset(self, new_page)  # type: ignore[attr-defined]
        except IndexError as e:
            self.logger.warning('%s', e)
