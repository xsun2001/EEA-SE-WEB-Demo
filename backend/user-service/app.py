from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, jwt_optional, get_jwt_identity, \
    get_raw_jwt

from .model import db, User

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "test"
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

CORS(app)
jwt = JWTManager(app)
db.init_app(app)
jwt_blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in jwt_blacklist


@app.before_first_request
def init_db():
    db.create_all()


@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Incorrect request format"}), 400

    password = request.json.get("password", None)
    email = request.json.get("email", None)

    if not password:
        return jsonify({"msg": "Missing password"}), 400
    import validators
    if not email or not validators.email(email):
        return jsonify({"msg": "Invalid email"}), 400

    user = User.query.filter_by(email=email).first()
    if not user.check_password(password):
        return jsonify({"msg": "Incorrect username or password"}), 400

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


@app.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"msg": "Incorrect request format"}), 400
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    if not username:
        return jsonify({"msg": "Missing username"}), 400
    if not password or len(password) <= 5:
        return jsonify({"msg": "No password or too weak"}), 400
    import validators
    if not email or not validators.email(email):
        return jsonify({"msg": "Invalid email"}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(user_id=user.id), 200


@app.route("/users/<int:user_id>", methods=["GET"])
@jwt_optional
def get_user_info(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    if get_jwt_identity() == user_id:
        return jsonify(user.as_dict()), 200
    return jsonify({"id": user.id, "username": user.username}), 200


@app.route("/users/<int:user_id>", methods=["POST"])
@jwt_required
def update_user_info(user_id):
    if not request.is_json:
        return jsonify({"msg": "Incorrect request format"}), 400
    if get_jwt_identity() != user_id:
        return jsonify({"msg": "Cannot modify other's info"}), 400
    user = User.query.filter_by(id=user_id).first()
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    if username:
        user.username = username
    import validators
    if email:
        if validators.email(email):
            user.email = email
        else:
            return jsonify({"msg": "Invalid email"}), 400
    if password:
        user.set_password(password)
    db.session.commit()
    return jsonify(user_id=user.id), 200


@app.route("/logout", methods=["DELETE"])
@jwt_required
def logout():
    jti = get_raw_jwt()["jti"]
    jwt_blacklist.add(jti)
    return jsonify({"msg": "Logged out"}), 200
