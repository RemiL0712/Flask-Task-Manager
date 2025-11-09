from flask import request
from flask_restx import Namespace, fields, Resource
from flask_jwt_extended import create_access_token
from ..extensions import db
from ..models.user import User

ns = Namespace("auth", description="Authentication")

login_model = ns.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

@ns.route("/register")
class Register(Resource):
    @ns.expect(login_model, validate=True)
    def post(self):
        payload = request.get_json()
        email = payload["email"].strip().lower()
        password = payload["password"]
        if db.session.query(User).filter_by(email=email).first():
            return {"message": "User already exists"}, 400
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return {"message": "Registered"}, 201

@ns.route("/login")
class Login(Resource):
    @ns.expect(login_model, validate=True)
    def post(self):
        payload = request.get_json()
        email = payload["email"].strip().lower()
        password = payload["password"]
        user = db.session.query(User).filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401
        token = create_access_token(identity=str(user.id))
        return {"access_token": token}, 200
