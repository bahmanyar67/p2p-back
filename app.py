# app.py
from flask import Flask
from config import Config
from extensions import db, jwt
from flask_cors import CORS

# import your routes
from routes.auth_routes import auth_bp
from routes.general_routers import general_bp
from routes.modules_router import modules_bp
from routes.users_routes import users_bp
from routes.bookings_routes import bookings_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # register your blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(general_bp)
    app.register_blueprint(modules_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(messages_bp)

    return app


if __name__ == '__main__':
    app = create_app()

    app.run(debug=True)
