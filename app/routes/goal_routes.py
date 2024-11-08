from flask import Blueprint, make_response, abort, request

from app import db
from app.models.goal import Goal

goal_bp = Blueprint("goal_bp",__name__, url_prefix="/goals")


@goal_bp.post("")
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body.keys():
        abort(make_response({"details": "Invalid data"}, 400))
    title = request_body["title"]
    new_goal = Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()
    response = {
        "goal": new_goal.to_dict()
    }
    return response, 201

@goal_bp.post("/<goal_id>")
def create_goal_with_id(goal_id):
    request_body = request.get_json()
    if "title" not in request_body.keys():
        abort(make_response({"details": "Invalid data"}, 400))
    title = request_body["title"]
    new_goal = Goal(id= goal_id, title=title)
    db.session.add(new_goal)
    db.session.commit()
    response = {
        "goal": new_goal.to_dict()
    }
    return response, 201
@goal_bp.get("")
def get_all_tasks():
    title_param = request.args.get("title")

    query = db.select(Goal)
    if title_param:
        query = query.where(Goal.title.like(f"%{title_param}"))

    goals = db.session.scalars(query).all()
    goals_response = [goal.to_dict() for goal in goals]
    return goals_response

def goal_id_validation(id):
    if not id.isnumeric():
        abort(make_response({"details": f" {id} Invalid data"}, 400))

@goal_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal_id_validation(goal_id)
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        response = {"message": f"{goal_id} not found"}
        abort(make_response(response,404))
    return {"goal": goal.to_dict()}

@goal_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal_id_validation(goal_id)
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if goal is None:
        abort(make_response({"details": f"Goal {goal_id} not found"}, 404))

    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return {
        "task": goal.to_dict()
    }

@goal_bp.delete("/<goal_id>")
def delete_task(goal_id):
    goal_id_validation(goal_id)
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)
    if not goal:
        response = {"details": f"{goal_id}Build a habit of going outside daily\" successfully deleted"}
        abort(make_response(response,404))

    db.session.delete(goal)
    db.session.commit()