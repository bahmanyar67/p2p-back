from extensions import db
from datetime import datetime


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # e.g., pending, confirmed, canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('User', foreign_keys=[student_id], backref='bookings_as_student')
    tutor = db.relationship('User', foreign_keys=[tutor_id], backref='bookings_as_tutor')

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "tutor_id": self.tutor_id,
            "student": self.student.to_dict() if self.student else None,
            # need full tutor object
            "tutor": self.tutor.to_dict() if self.tutor else None,
            "date": self.date.isoformat(),
            "time": self.time,
            "total_price": self.total_price,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
