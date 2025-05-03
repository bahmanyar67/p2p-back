# models/user.py
from extensions import db

user_skills = db.Table('user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('module_id', db.Integer, db.ForeignKey('modules.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'users'  # Explicitly set table name to 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(100))
    avatar = db.Column(db.String(255))
    is_tutor = db.Column(db.Boolean, default=False)
    skills = db.relationship('Module', secondary=user_skills, backref='users')
    rate = db.Column(db.Float, default=0)
    bio = db.Column(db.Text)
    availability = db.Column(db.JSON, default={})
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


    def to_dict(self):
        """Helper method to serialize user easily"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "subject": self.subject,
            "avatar": self.avatar if self.avatar else "avatars/user.png",
            "is_tutor": self.is_tutor,
            "skills": [skill.slug for skill in self.skills],  # Serialize skills as a list of slugs
            "rate": self.rate,
            "bio": self.bio,
            "availability": list(self.availability),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }