from flask import Blueprint, send_from_directory, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
import os

general_bp = Blueprint('general', __name__)


@general_bp.route('/')
def index():
    return "Welcome to the API!"

@general_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    return jsonify({"message": f"Welcome to the protected area, {user.name}!"})

@general_bp.route('/avatars/<filename>')
def get_avatar(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'static/avatars'), filename)

@general_bp.route('/static/modules/<path:filename>')
def get_static_modules(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'static/modules'), filename)