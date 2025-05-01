from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from validators import Validator
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from extensions import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    request_data = request.json

    if not Validator.validate("username", ["required", "email"], request_data):
        return jsonify({"success": False, "message": Validator.get_first_error('username')}), 422

    if not Validator.validate("password", ["required", ["min", 8], ["max", 20], "password"], request_data):
        return jsonify({"success": False, "message": Validator.get_first_error('password')}), 422

    # Query user from database
    user = User.query.filter_by(email=request_data['username']).first()

    if user and check_password_hash(user.password, request_data['password']):
        access_token = create_access_token(identity=user.email)
        return jsonify({"success": True, "token": access_token, "user": user.to_dict()}), 200

    return jsonify({"success": False, "message": "Invalid credentials"}), 401


@auth_bp.route("/auth/register", methods=["POST"])
def register():
    request_data = request.json

    # Validate required fields
    if not Validator.validate("name", ["required"], request_data):
        return jsonify({"success": False, "message": Validator.get_first_error('name')}), 422

    if not Validator.validate("email", ["required", "email"], request_data):
        return jsonify({"success": False, "message": Validator.get_first_error('email')}), 422

    if not Validator.validate("password", ["required", ["min", 8], ["max", 20], "password"], request_data):
        return jsonify({"success": False, "message": Validator.get_first_error('password')}), 422

    # Check if user already exists
    if User.query.filter_by(email=request_data['email']).first():
        return jsonify({"success": False, "message": "Email already registered"}), 422

    # Hash the password before storing it
    hashed_password = generate_password_hash(request_data['password'])

    # Create new user
    new_user = User(
        name=request_data['name'],
        email=request_data['email'],
        password=hashed_password
    )

    # Save user to the database
    db.session.add(new_user)
    db.session.commit()

    # Create JWT token for the new user
    access_token = create_access_token(identity=new_user.email)

    # Return success response with user data and token
    return jsonify({"success": True, "message": "User registered successfully", "token": access_token,
                    "user": new_user.to_dict()}), 201


@auth_bp.route("/auth/logout", methods=["POST"])
@jwt_required()
def logout():
    # Invalidate the JWT token by adding it to a blacklist or simply returning a success message
    return jsonify({"success": True, "message": "Logged out successfully"}), 200


@auth_bp.route("/users/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": True, "message": "User deleted successfully"}), 200

    return jsonify({"success": False, "message": "User not found"}), 404
