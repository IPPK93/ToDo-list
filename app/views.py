from typing import Union

from flask import redirect, render_template, request, url_for
from werkzeug import Response

import app


@app.app.route('/')  # type: ignore
@app.app.route('/tasks', methods=['GET', 'POST'])  # type: ignore
def tasks() -> str:
    status = request.args.get('status', None)
    page = request.args.get('page', None, type=int)
    search_filter = request.args.get('filterby', None)
    if status is not None:
        app.tasks_handler.status = status
    if page is not None:
        app.tasks_handler.page = page
    if search_filter is not None:
        app.tasks_handler.filterby = search_filter
    pages = app.tasks_handler.pages_representation()
    return render_template(
        'tasks.html',
        tasks=app.tasks_handler.requested_tasks,
        status=app.tasks_handler.status,
        filterby=app.tasks_handler.filterby,
        cur_page=str(app.tasks_handler.page),
        pages_repr=pages,
    )


@app.app.route('/add_task', methods=['GET', 'POST'])  # type: ignore
def add_task() -> Union[Response, str]:
    if request.method == 'POST':
        description = request.form['task_description']
        app.tasks_handler.add_task(description)
        page = app.tasks_handler.page if app.tasks_handler.page > 1 else None
        return redirect(
            url_for(
                'tasks',
                status=app.tasks_handler.status,
                filterby=app.tasks_handler.filterby,
                page=page,
            )
        )
    return render_template('add_task.html')


@app.app.route('/finish_task', methods=['POST'])  # type: ignore
def finish_task() -> Response:
    task_index = int(request.form['task_index'])
    app.tasks_handler.finish_task(task_index)
    page = app.tasks_handler.page if app.tasks_handler.page > 1 else None
    return redirect(
        url_for(
            'tasks',
            status=app.tasks_handler.status,
            filterby=app.tasks_handler.filterby,
            page=page,
        )
    )


@app.app.route('/delete_task', methods=['POST'])  # type: ignore
def delete_task() -> Response:
    task_index = int(request.form['task_index'])
    app.tasks_handler.delete_task(task_index)
    page = app.tasks_handler.page if app.tasks_handler.page > 1 else None
    return redirect(
        url_for(
            'tasks',
            status=app.tasks_handler.status,
            filterby=app.tasks_handler.filterby,
            page=page,
        )
    )


@app.app.route('/main_page', methods=['GET'])  # type: ignore
def main_page() -> Response:
    app.tasks_handler.set_state_default()
    return redirect(url_for('tasks'))
