from flask import Flask
from flask_cors import CORS
from .db import db, migrate
from .models import board, card
from .routes.board_routes import bp as board_bp
# from .routes.card_routes import bp as card_bp
import os

def create_app(config=None):
    app = Flask(__name__)

    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(board_bp)
    # app.register_blueprint(cards_bp)

    CORS(app)
    return app
