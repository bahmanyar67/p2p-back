from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from validators import Validator
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.module import Module
from extensions import db

users_bp = Blueprint('users', __name__)


@users_bp.route("/users/update", methods=["PUT"])
@jwt_required()
def update_user():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    request_data = request.json

    # Validate required fields
    if not Validator.validate("name", ["required", "string"], request_data):
        return jsonify({"success": False, "message": Validator.get_first_error('name')}), 422

    if not Validator.validate("email", ["required", "email"], request_data):
        return jsonify({"success": False, "message": Validator.get_first_error('email')}), 422

    if not Validator.validate("phone", ["required", "number"], request_data):
        return jsonify({"success": False, "message": Validator.get_first_error('phone')}), 422

    if not Validator.validate("subject", ["required", "string"], request_data):
        return jsonify({"success": False, "message": Validator.get_first_error('subject')}), 422

    if not Validator.validate("is_tutor", ["required", "boolean"], request_data):
        return jsonify({"success": False, "message": Validator.get_first_error('is_tutor')}), 422

    # validate tutor specific fields
    if request_data['is_tutor']:
        if not Validator.validate("rate", ["required", "price"], request_data):
            return jsonify({"success": False, "message": Validator.get_first_error('rate')}), 422

        if not Validator.validate("bio", ["required"], request_data):
            return jsonify({"success": False, "message": Validator.get_first_error('bio')}), 422

        if not Validator.validate("skills", ["required", "array"], request_data):
            return jsonify({"success": False, "message": Validator.get_first_error('skills')}), 422

        if not Validator.validate("availability", ["required", "array"], request_data):
            return jsonify({"success": False, "message": Validator.get_first_error('availability')}), 422

    # Update user details
    user.name = request_data['name']
    user.email = request_data['email']
    user.phone = request_data['phone']
    user.subject = request_data['subject']
    user.is_tutor = request_data['is_tutor']
    if request_data['is_tutor']:
        user.rate = request_data.get('rate', user.rate)
        user.bio = request_data.get('bio', user.bio)
        user.availability = request_data.get('availability', user.availability)

        # Update skills
        if 'skills' in request_data:
            user.skills.clear()  # Clear existing skills
            for skill_name in request_data['skills']:
                skill = Module.query.filter_by(slug=skill_name).first()
                user.skills.append(skill)

    # Save changes to the database
    db.session.commit()

    return jsonify({"success": True, "message": "User updated successfully", "user": user.to_dict()}), 200


@users_bp.route("/tutors", methods=["GET"])
@jwt_required()
def get_tutors():
    # Get all tutors
    tutors = User.query.filter_by(is_tutor=True).all()
    tutors_list = [tutor.to_dict() for tutor in tutors]

    return jsonify({"success": True, "message": "List of tutors", "tutors": tutors_list}), 200


@users_bp.route("/tutors/<int:tutor_id>", methods=["GET"])
@jwt_required()
def get_tutor(tutor_id):
    # Get a specific tutor by ID
    tutor = User.query.filter_by(id=tutor_id, is_tutor=True).first()

    if not tutor:
        return jsonify({"success": False, "message": "Tutor not found"}), 404

    return jsonify({"success": True, "message": "Tutor details", "tutor": tutor.to_dict()}), 200


@users_bp.route("/tutors/skills/<int:skill_id>", methods=["GET"])
@jwt_required()
def get_tutors_by_skill(skill_id):
    # Get all tutors with a specific skill
    tutors = User.query.join(User.skills).filter(Module.id == skill_id, User.is_tutor == True).all()
    tutors_list = [tutor.to_dict() for tutor in tutors]
    if not tutors_list:
        return jsonify({"success": False, "message": "No tutors found with this skill"}), 404
    return jsonify({"success": True, "message": "List of tutors with this skill", "tutors": tutors_list}), 200


@users_bp.route("/users/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": True, "message": "User deleted successfully"}), 200

    return jsonify({"success": False, "message": "User not found"}), 404
