from flask import Blueprint, request, Response
from app.models.board import Board
from app.models.card import Card
from ..db import db
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("board_bp", __name__, url_prefix="/boards")

@bp.get("")
def get_all_boards():
    query = db.select(Board)
    boards = db.session.scalars(query)
    boards_list = [board.to_dict() for board in boards]
    return {"boards": boards_list}, 200

    # return get_models_with_filters(Board, request.args)

@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model(Board, request_body)

@bp.post("/<goal_id>/cards")
def create_card_with_board(board_id):
    
    board = validate_model(Board, board_id)
    request_body = request.get_json()
    
    return create_model(Card, {**request_body, "board_id": board.board_id})



@bp.get("/<board_id>/cards")
def get_cards_by_board(board_id):

    board = validate_model(Board, board_id)
    cards = [card.to_dict() for card in board.cards]

    return { cards }, 200