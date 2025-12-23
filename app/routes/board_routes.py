from flask import Blueprint, request, abort, make_response
from app.models.board import Board
from app.models.card import Card
from ..db import db
from ..routes.routes_utilities import create_model, validate_model

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model(Board, request_body)


@bp.post("/<board_id>/cards")
def create_card_on_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()
    return create_model(Card, {**request_body, "board_id": board.board_id})

@bp.get("/<board_id>")
def get_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict(), 200