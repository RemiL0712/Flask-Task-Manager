from flask import request
from flask_restx import Namespace, fields, Resource
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.task import Task

ns = Namespace("tasks", description="Task CRUD")

task_model = ns.model("Task", {
    "id": fields.Integer(readonly=True),
    "title": fields.String(required=True),
    "description": fields.String,
    "status": fields.String,
})

@ns.route("")
class TaskList(Resource):
    @jwt_required()
    def get(self):
        # Filters
        q = request.args.get("q")
        status = request.args.get("status")
        query = db.session.query(Task)
        if q:
            like = f"%{q}%"
            query = query.filter(Task.title.ilike(like))
        if status:
            query = query.filter(Task.status == status)
        items = query.order_by(Task.created_at.desc()).all()
        return [ {"id": t.id, "title": t.title, "description": t.description, "status": t.status} for t in items ]

    @ns.expect(task_model, validate=True)
    @jwt_required()
    def post(self):
        payload = request.get_json()
        t = Task(title=payload["title"], description=payload.get("description"), status=payload.get("status", "todo"))
        db.session.add(t)
        db.session.commit()
        return {"id": t.id, "title": t.title, "description": t.description, "status": t.status}, 201

@ns.route("/<int:task_id>")
class TaskDetail(Resource):
    @jwt_required()
    def get(self, task_id: int):
        t = db.session.get(Task, task_id)
        if not t:
            return {"message": "Not found"}, 404
        return {"id": t.id, "title": t.title, "description": t.description, "status": t.status}

    @ns.expect(task_model, validate=True)
    @jwt_required()
    def put(self, task_id: int):
        t = db.session.get(Task, task_id)
        if not t:
            return {"message": "Not found"}, 404
        payload = request.get_json()
        t.title = payload["title"]
        t.description = payload.get("description")
        t.status = payload.get("status", t.status)
        db.session.commit()
        return {"id": t.id, "title": t.title, "description": t.description, "status": t.status}

    @jwt_required()
    def delete(self, task_id: int):
        t = db.session.get(Task, task_id)
        if not t:
            return {"message": "Not found"}, 404
        db.session.delete(t)
        db.session.commit()
        return {"message": "Deleted"}, 204
