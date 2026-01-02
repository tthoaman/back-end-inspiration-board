import pytest
from app.db import db
from app.models.card import Card


class TestDeleteCard:
    def test_delete_card_success(self, client, one_card):
        response = client.delete(f"/cards/{one_card}")

        assert response.status_code == 204

    def test_delete_card_not_found(self, client):
        response = client.delete("/cards/999")
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Card 999 not found"}

    def test_delete_card_invalid_id(self, client):
        response = client.delete("/cards/invalid")
        response_body = response.get_json()

        assert response.status_code == 400
        assert response_body == {"details": "Invalid data"}


class TestLikeCard:
    def test_like_card_success(self, client, one_card):
        response = client.post(f"/cards/{one_card}/like")
        response_body = response.get_json()

        assert response.status_code == 200
        assert response_body["card_id"] == one_card
        assert response_body["likes_count"] == 1

    def test_like_card_multiple_times(self, client, one_card):
        # Like three times
        client.post(f"/cards/{one_card}/like")
        client.post(f"/cards/{one_card}/like")
        response = client.post(f"/cards/{one_card}/like")
        response_body = response.get_json()

        assert response.status_code == 200
        assert response_body["likes_count"] == 3

    def test_like_card_not_found(self, client):
        response = client.post("/cards/999/like")
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Card 999 not found"}

    def test_like_card_invalid_id(self, client):
        response = client.post("/cards/invalid/like")
        response_body = response.get_json()

        assert response.status_code == 400
        assert response_body == {"details": "Invalid data"}

    def test_like_card_preserves_message(self, client, app, one_board):
        # Create a card with specific message
        with app.app_context():
            card = Card(message="Special Message", likes_count=0, board_id=one_board)
            db.session.add(card)
            db.session.commit()
            card_id = card.card_id

        response = client.post(f"/cards/{card_id}/like")
        response_body = response.get_json()

        assert response_body["message"] == "Special Message"