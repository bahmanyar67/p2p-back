from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.message import Message
from models.booking import Booking
from extensions import db

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    current_user_email = get_jwt_identity()
    sender = User.query.filter_by(email=current_user_email).first()

    if not sender:
        return jsonify({"success": False, "message": "Sender not found"}), 404

    data = request.json
    receiver = User.query.filter_by(id=data.get('receiver_id')).first()

    if not receiver:
        return jsonify({"success": False, "message": "Receiver not found"}), 404

    if not data.get('content'):
        return jsonify({"success": False, "message": "Message content is required"}), 400

    message = Message(sender_id=sender.id, receiver_id=receiver.id, content=data['content'])
    db.session.add(message)
    db.session.commit()

    return jsonify({"success": True, "message": "Message sent successfully", "message_item": message.to_dict()}), 201


@messages_bp.route('/messages', methods=['GET'])
@jwt_required()
def get_all_messages():
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()

    if not current_user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Get all bookings where the current user is either a student or a tutor
    student_bookings = Booking.query.filter_by(student_id=current_user.id).all()
    tutor_bookings = Booking.query.filter_by(tutor_id=current_user.id).all()

    # Combine tutor and student IDs
    user_ids = {booking.tutor_id for booking in student_bookings}
    user_ids.update(booking.student_id for booking in tutor_bookings)

    # Get the last message for each tutor
    tutors_with_last_message = []
    for tutor_id in user_ids:
        tutor = User.query.get(tutor_id)
        last_message = Message.query.filter(
            ((Message.sender_id == current_user.id) & (Message.receiver_id == tutor_id)) |
            ((Message.sender_id == tutor_id) & (Message.receiver_id == current_user.id))
        ).order_by(Message.created_at.desc()).first()

        tutors_with_last_message.append({
            **tutor.to_dict(),
            "last_message": last_message.to_dict() if last_message else None,
            "has_unread_messages": Message.query.filter(
                (Message.sender_id == tutor_id) & (Message.receiver_id == current_user.id) & (Message.is_read == False)
            ).count() > 0
        })

    return jsonify({"success": True, "users": tutors_with_last_message}), 200


@messages_bp.route('/messages/<int:user_id>', methods=['GET'])
@jwt_required()
def get_messages(user_id):
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()

    user = User.query.get(user_id)

    if not current_user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Mark all messages as read where the current user is the receiver
    Message.query.filter(
        (Message.sender_id == user_id) & (Message.receiver_id == current_user.id) & (Message.is_read == False)
    ).update({"is_read": True})
    db.session.commit()

    messages = Message.query.filter(
        (Message.sender_id == current_user.id) & (Message.receiver_id == user_id) |
        (Message.sender_id == user_id) & (Message.receiver_id == current_user.id)
    ).order_by(Message.created_at).all()

    messages_list = [message.to_dict() for message in messages]

    return jsonify({"success": True, "messages": messages_list, "user": user.to_dict()}), 200
