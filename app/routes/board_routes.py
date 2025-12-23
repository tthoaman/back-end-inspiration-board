from flask import Blueprint, request, abort, make_response
from app.models.board import Board
from app.models.card import Card
from ..db import db

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model(Board, request_body)


@bp.post("/<board_id>/cards")
def get_board_cards(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()
    return create_model(Card, {**request_body, "board_id": board.board_id})

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)

    except KeyError:
        response = {'details': f'Invalid data'}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)

    except:
        response = {'message': f'{cls.__name__} {model_id} invalid'}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {'message': f'{cls.__name__} {model_id} not found'}
        abort(make_response(response, 404))

    return model