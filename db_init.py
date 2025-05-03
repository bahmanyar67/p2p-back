# db_init.py
from app import create_app
from extensions import db
from models.user import User
from models.module import Module
from werkzeug.security import generate_password_hash

app = create_app()

'''
availability format
[{"day": "Monday", "slots": [{"time": "08:00 - 09:30", "isAvailable": false}, {"time": "10:00 - 11:30", "isAvailable": true}, {"time": "12:00 - 13:30", "isAvailable": false}, {"time": "14:00 - 15:30", "isAvailable": false}, {"time": "16:00 - 17:30", "isAvailable": false}, {"time": "18:00 - 19:30", "isAvailable": false}]}, {"day": "Tuesday", "slots": [{"time": "08:00 - 09:30", "isAvailable": false}, {"time": "10:00 - 11:30", "isAvailable": false}, {"time": "12:00 - 13:30", "isAvailable": false}, {"time": "14:00 - 15:30", "isAvailable": false}, {"time": "16:00 - 17:30", "isAvailable": false}, {"time": "18:00 - 19:30", "isAvailable": true}]}, {"day": "Wednesday", "slots": [{"time": "08:00 - 09:30", "isAvailable": false}, {"time": "10:00 - 11:30", "isAvailable": false}, {"time": "12:00 - 13:30", "isAvailable": false}, {"time": "14:00 - 15:30", "isAvailable": true}, {"time": "16:00 - 17:30", "isAvailable": false}, {"time": "18:00 - 19:30", "isAvailable": false}]}, {"day": "Thursday", "slots": [{"time": "08:00 - 09:30", "isAvailable": false}, {"time": "10:00 - 11:30", "isAvailable": false}, {"time": "12:00 - 13:30", "isAvailable": false}, {"time": "14:00 - 15:30", "isAvailable": false}, {"time": "16:00 - 17:30", "isAvailable": false}, {"time": "18:00 - 19:30", "isAvailable": true}]}, {"day": "Friday", "slots": [{"time": "08:00 - 09:30", "isAvailable": false}, {"time": "10:00 - 11:30", "isAvailable": false}, {"time": "12:00 - 13:30", "isAvailable": false}, {"time": "14:00 - 15:30", "isAvailable": true}, {"time": "16:00 - 17:30", "isAvailable": false}, {"time": "18:00 - 19:30", "isAvailable": false}]}, {"day": "Saturday", "slots": [{"time": "08:00 - 09:30", "isAvailable": false}, {"time": "10:00 - 11:30", "isAvailable": false}, {"time": "12:00 - 13:30", "isAvailable": false}, {"time": "14:00 - 15:30", "isAvailable": false}, {"time": "16:00 - 17:30", "isAvailable": false}, {"time": "18:00 - 19:30", "isAvailable": true}]}, {"day": "Sunday", "slots": [{"time": "08:00 - 09:30", "isAvailable": false}, {"time": "10:00 - 11:30", "isAvailable": false}, {"time": "12:00 - 13:30", "isAvailable": false}, {"time": "14:00 - 15:30", "isAvailable": true}, {"time": "16:00 - 17:30", "isAvailable": false}, {"time": "18:00 - 19:30", "isAvailable": false}]}]
'''


def generate_random_availability():
    import random
    import json

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    availability = []

    # each session is 1:30 hours
    time_slots = [
        {"time": "08:00 - 09:30", "isAvailable": random.choice([True, False])},
        {"time": "10:00 - 11:30", "isAvailable": random.choice([True, False])},
        {"time": "12:00 - 13:30", "isAvailable": random.choice([True, False])},
        {"time": "14:00 - 15:30", "isAvailable": random.choice([True, False])},
        {"time": "16:00 - 17:30", "isAvailable": random.choice([True, False])},
        {"time": "18:00 - 19:30", "isAvailable": random.choice([True, False])},
    ]
    for day in days:
        slots = random.sample(time_slots, k=random.randint(1, len(time_slots)))
        availability.append({"day": day, "slots": slots})

    return availability


def create_demo_modules():
    demo_modules = [
        {"id": 1, "icon": "static/modules/maths.png", "name": "Math", "slug": "mathematics"},
        {"id": 2, "icon": "static/modules/ai.png", "name": "AI", "slug": "artificial-intelligence"},
        {"id": 3, "icon": "static/modules/python.png", "name": "Python", "slug": "python"},
        {"id": 4, "icon": "static/modules/c-plus-plus.png", "name": "C++", "slug": "c-plus-plus"},
        {"id": 5, "icon": "static/modules/android.png", "name": "Android", "slug": "android"},
        {"id": 6, "icon": "static/modules/html.png", "name": "HTML", "slug": "html"},
    ]

    for module_data in demo_modules:
        module = Module(**module_data)
        db.session.add(module)

    db.session.commit()


def create_demo_tutors():
    demo_tutors = [
        {
            "name": "John Doe",
            "email": "john@domain.test",
            "password": "Password123!",
            "phone": "+44 1234 567890",
            "subject": "Math",
            "is_tutor": True,
            "skills": ["mathematics"],
            "rate": 9.00,
            "bio": "Experienced math tutor.",
            "availability": generate_random_availability()
        },
        {
            "name": "Jane Smith",
            "email": "jane@domain.test",
            "password": "Password123!",
            "phone": "+44 9876 543210",
            "subject": "AI",
            "is_tutor": True,
            "skills": ["artificial-intelligence"],
            "rate": 10.00,
            "bio": "Expert in AI and machine learning.",
            "availability": generate_random_availability()
        },
        {
            "name": "Alice Johnson",
            "email": "alice@domain.test",
            "password": "Password123!",
            "phone": "+44 1122 334455",
            "subject": "Python",
            "is_tutor": True,
            "skills": ["python"],
            "rate": 8.00,
            "bio": "Python programming tutor.",
            "availability": generate_random_availability()
        },
        {
            "name": "Bob Brown",
            "email": "bob@domain.test",
            "password": "Password123!",
            "phone": "+44 5566 778899",
            "subject": "C++",
            "is_tutor": True,
            "skills": ["c-plus-plus"],
            "rate": 11.00,
            "bio": "C++ programming tutor.",
            "availability": generate_random_availability()
        },
        {
            "name": "Charlie Green",
            "email": "charlie@domain.test",
            "password": "Password123!",
            "phone": "+44 2233 445566",
            "subject": "Android",
            "is_tutor": True,
            "skills": ["android"],
            "rate": 12.00,
            "bio": "Android development tutor.",
            "availability": generate_random_availability()
        },
        {
            "name": "Diana White",
            "email": "diana@domain.test",
            "password": "Password123!",
            "phone": "+44 3344 556677",
            "subject": "HTML",
            "is_tutor": True,
            "skills": ["html"],
            "rate": 7.00,
            "bio": "HTML and web development tutor.",
            "availability": generate_random_availability()
        },
    ]

    for tutor_data in demo_tutors:
        # Hash the password before saving
        tutor_data["password"] = generate_password_hash(tutor_data['password'])

        # Create a User instance
        tutor = User(
            name=tutor_data["name"],
            email=tutor_data["email"],
            password=tutor_data["password"],
            phone=tutor_data["phone"],
            subject=tutor_data["subject"],
            is_tutor=tutor_data["is_tutor"],
            rate=tutor_data["rate"],
            bio=tutor_data["bio"],
            availability=tutor_data["availability"]
        )

        # save the user to the database
        db.session.add(tutor)
        db.session.commit()

        # add skills to the tutor
        for skill in tutor_data["skills"]:
            module = Module.query.filter_by(slug=skill).first()
            if module:
                tutor.skills.append(module)

    db.session.commit()


with app.app_context():
    try:
        # purge the database
        db.drop_all()
        print("Tables dropped successfully!")

        db.create_all()
        print("Tables created successfully!")

        create_demo_modules()
        print("Demo modules inserted successfully!")

        create_demo_tutors()
        print("Demo tutors inserted successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
