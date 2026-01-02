from flask import Blueprint, request, abort, make_response
from app.models.board import Board
from app.models.card import Card
from ..db import db
from app.routes.route_utilities import validate_model, create_model

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.get("")
def get_all_boards():
    query = db.select(Board)
    boards = db.session.scalars(query)
    boards_list = [board.to_dict() for board in boards]
    return {"boards": boards_list}, 200

@bp.post("")
def create_board():
    request_body = request.get_json()
    return create_model(Board, request_body)

@bp.get("/<board_id>")
def get_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict(), 200

@bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_model(Board, board_id)
    db.session.delete(board)
    db.session.commit()
    return {"details": f'Board {board_id} "{board.title}" successfully deleted'}, 200

@bp.post("/<board_id>/cards")
def create_card_on_board(board_id):
    board = validate_model(Board, board_id)
    data = request.get_json()
    return create_model(Card, {**data, "board_id": board.board_id})

@bp.get("/<board_id>/cards")
def get_cards_on_board(board_id):
    board = validate_model(Board, board_id)
    cards = board.cards
    cards_list = [card.to_dict() for card in cards]
    return {"cards": cards_list}, 200

@bp.delete("/<board_id>/<card_id>")
def delete_card_on_board(board_id, card_id):
    board = validate_model(Board, board_id)
    card = validate_model(Card, card_id)
    if card.board_id != board.board_id:
        response = {"details": f"Card {card_id} does not belong to Board {board_id}"}
        abort(make_response(response, 400))
    db.session.delete(card)
    db.session.commit()
    return {"details": f'Card {card_id} successfully deleted from Board {board_id}'}, 200

@bp.patch("/<board_id>/cards/<card_id>/like")
def like_card(board_id, card_id):
    board = validate_model(Board, board_id)
    card = validate_model(Card, card_id)

    if card.board_id != board.board_id:
        abort(make_response(
        {"details": "Card does not belong to this board"},404
    ))

    card.likes_count += 1
    db.session.commit()

    return {
        "card_id": card.card_id,
        "message": card.message,
        "likes_count": card.likes_count,
        "board_id": card.board_id
    }, 200
