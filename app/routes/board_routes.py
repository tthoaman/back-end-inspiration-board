from flask import Blueprint, request, Response
from app.models.board import Board
from app.models.card import Card
from ..db import db
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("board_bp", __name__, url_prefix="/boards")

@bp.get("")
def get_all_boards():

    return get_models_with_filters(Board, request.args)

@bp.post("")
def create_goal():
    request_body = request.get_json()

    return create_model(Board, request_body)

@bp.post("/<goal_id>/tasks")
def create_card_with_board(board_id):
    
    board = validate_model(Board, board_id)
    
    request_body = request.get_json() 
    card_ids = request_body["card_ids"] 

    card_list = [] 
    for id in card_ids: 
        card = validate_model(Card, id)
        card_list.append(card)

    board.cards = card_list
    db.session.commit()

    return { 
            "id": board.id,
            "card_ids": card_ids
        }, 200

@bp.get("/<board_id>/cards")
def get_cards_by_board(board_id):

    board = validate_model(Board, board_id)
    cards = [card.to_dict() for card in board.cards]

    return {
        "id": board.id,
        "title": board.title,
        "owner": board.owner,
        "cards": cards
    }, 200