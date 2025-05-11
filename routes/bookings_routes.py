from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.booking import Booking
from extensions import db
from datetime import datetime
import stripe

stripe.api_key = "sk_test_51KxzhtKeIAw0kBJOO3XjfDEE8MXiLvC51NlEBZuBobJwqSuIqShtD5c3yj6DCPyr6PvRfYk2xhdTAlMzdrzDXJli003hccOBb8"

bookings_bp = Blueprint('bookings', __name__)


@bookings_bp.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    current_user_email = get_jwt_identity()
    student = User.query.filter_by(email=current_user_email).first()

    if not student:
        return jsonify({"success": False, "message": "Student not found"}), 404

    data = request.json
    tutor = User.query.filter_by(id=data.get('tutor_id'), is_tutor=True).first()

    if not tutor:
        return jsonify({"success": False, "message": "Tutor not found"}), 404

    try:
        # date will be passed like : 2025-05-03T21:30:26.274Z
        date = datetime.strptime(data.get('date'), '%Y-%m-%dT%H:%M:%S.%fZ').date()
        time = data.get('time')
        total_price = tutor.rate
    except ValueError:
        return jsonify({"success": False, "message": "Invalid date or time format"}), 400

    booking = Booking(
        student_id=student.id,
        tutor_id=tutor.id,
        date=date,
        time=time,
        total_price=total_price,
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({"success": True, "message": "Booking created successfully", "booking": booking.to_dict()}), 201


@bookings_bp.route('/bookings/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking(booking_id):
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"success": False, "message": "Booking not found"}), 404

    return jsonify({"success": True, "booking": booking.to_dict()}), 200


@bookings_bp.route('/bookings/<int:booking_id>/create-payment-intent', methods=['POST'])
@jwt_required()
def create_payment_intent(booking_id):
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"success": False, "message": "Booking not found"}), 404

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(booking.total_price * 100),  # in cents
            currency='gbp',
            automatic_payment_methods={'enabled': True},
            metadata={'booking_id': booking.id}
        )

        return jsonify({
            'success': True,
            'client_secret': intent.client_secret
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@bookings_bp.route('/bookings/<int:booking_id>/confirm', methods=['PUT'])
@jwt_required()
def confirm_booking_status(booking_id):
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"success": False, "message": "Booking not found"}), 404

    booking.status = 'confirmed'
    db.session.commit()

    return jsonify({"success": True, "message": "Booking confirmed successfully", "booking": booking.to_dict()}), 200



@bookings_bp.route('/bookings/<int:booking_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_booking_status(booking_id):
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({"success": False, "message": "Booking not found"}), 404

    booking.status = 'canceled'
    db.session.commit()

    return jsonify({"success": True, "message": "Booking canceled successfully", "booking": booking.to_dict()}), 200


@bookings_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_user_bookings():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    bookings = Booking.query.filter((Booking.student_id == user.id) | (Booking.tutor_id == user.id)).all()
    bookings_list = [booking.to_dict() for booking in bookings]

    return jsonify({"success": True, "bookings": bookings_list}), 200
