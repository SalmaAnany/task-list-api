from datetime import datetime
from http.client import responses

from flask import request, Blueprint, make_response, abort, Response
from sqlalchemy import asc, desc

from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp",__name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    if "title" not in request_body.keys():
        abort(make_response({"details": "Invalid data"}, 400))
    title = request_body["title"]
    if "description" not in request_body.keys():
        abort(make_response({"details": "Invalid data"}, 400))
    description = request_body["description"]
    new_task = Task(title=title, description=description,completed_at= None)
    db.session.add(new_task)
    db.session.commit()
    response = {
        "task": new_task.to_dict()
    }
    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    description_param = request.args.get("description")
    title_param = request.args.get("title")
    sort_param = request.args.get("sort")

    query = db.select(Task)
    if description_param:
        query = query.where(Task.description.like(f"%{description_param}%"))

    if title_param:
        query = query.where(Task.title.like(f"%{title_param}"))
    if sort_param == "asc":
        query = query.order_by(asc(Task.title))
    elif sort_param == "desc":
        query = query.order_by(desc(Task.title))

    tasks = db.session.scalars(query).all()
    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response


def validate_id(id):
    if not id.isnumeric():
        abort(make_response({"message": f"Tasks id {id} invalid"}, 400))

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    validate_id(task_id)
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response ={"message": f"{task_id} not found"}
        abort(make_response(response, 404))

    return { "task": task.to_dict()}

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    validate_id(task_id)
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if task is None:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    if "is_complete" in request_body.keys() and request_body["is_complete"]:
        task.completed_at = datetime.now()
    else:
        task.completed_at = None
    db.session.commit()
    return {
        "task": task.to_dict()
    }

@tasks_bp.delete("/<task_id>")
def delete_planet(task_id):
    validate_id(task_id)
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    if not task:
        response = {"message": f"{task_id} not found"}
        abort(make_response(response,404))

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete_on_an_incompleted_task(task_id):
    validate_id(task_id)
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    if task is None:
        response = {"message": f"Task {task_id} not found"}
        abort(make_response(response, 404))
    task.completed_at = datetime.now()
    db.session.commit()
    updated_task = db.session.scalar(query)
    return {"task": updated_task.to_dict()}

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_in_complete_task(task_id):
    validate_id(task_id)
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    if task is None:
        response = {"message": f"{task_id} not found"}
        abort(make_response(response, 404))
    task.completed_at = None
    db.session.commit()
    updated_task = db.session.scalar(query)
    return {"task": updated_task.to_dict()}
