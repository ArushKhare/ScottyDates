from flask import Blueprint, request, jsonify

api = Blueprint("api", __name__)

@api.get("/hello")
def hello():
    return jsonify({"message": "Hello from Flask!"})

@api.post("/add")
def add_numbers():
    a = int(request.args.get("a", 0))
    b = int(request.args.get("b", 0))
    return jsonify({"result": a + b})