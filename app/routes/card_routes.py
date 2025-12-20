from flask import Blueprint, Response
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