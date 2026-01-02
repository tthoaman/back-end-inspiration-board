from flask import Blueprint, Response,request
from app.models.card import Card
from app.routes.route_utilities import validate_model
from ..db import db

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.post("/<card_id>/like")
def like_card(card_id):
    card = validate_model(Card, card_id)

    card.likes_count += 1
    db.session.commit()

    return {
        "card_id": card.card_id,
        "message": card.message,
        "likes_count": card.likes_count
    }, 200

@bp.patch("<card_id>")
def edit_card(card_id):
    card = validate_model(Card, card_id)
    data = request.get_json()

    if "message" in data:
        card.message = data["message"]
    if "likes_count" in data:
        card.likes_count = data["likes_count"]
    
    db.session.commit()
    
    return card.to_dict(), 200