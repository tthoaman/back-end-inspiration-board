import pytest
from app.db import db
from app.models.board import Board
from app.models.card import Card


class TestGetAllBoards:
    def test_get_all_boards_empty(self, client):
        response = client.get("/boards")

        assert response.status_code == 200
        assert response.get_json() == {"boards": []}

    def test_get_all_boards_with_boards(self, client, two_boards):
        response = client.get("/boards")
        response_body = response.get_json()

        assert response.status_code == 200
        assert len(response_body["boards"]) == 2
        assert response_body["boards"][0]["title"] == "Board One"
        assert response_body["boards"][1]["title"] == "Board Two"


class TestCreateBoard:
    def test_create_board_success(self, client):
        response = client.post("/boards", json={
            "title": "New Board",
            "owner": "New Owner"
        })
        response_body = response.get_json()

        assert response.status_code == 201
        assert response_body["title"] == "New Board"
        assert response_body["owner"] == "New Owner"
        assert "board_id" in response_body

    def test_create_board_missing_title(self, client):
        response = client.post("/boards", json={
            "owner": "New Owner"
        })
        response_body = response.get_json()

        assert response.status_code == 400
        assert response_body == {"details": "Invalid data"}

    def test_create_board_missing_owner(self, client):
        response = client.post("/boards", json={
            "title": "New Board"
        })
        response_body = response.get_json()

        assert response.status_code == 400
        assert response_body == {"details": "Invalid data"}

    def test_create_board_empty_body(self, client):
        response = client.post("/boards", json={})
        response_body = response.get_json()

        assert response.status_code == 400
        assert response_body == {"details": "Invalid data"}


class TestGetBoard:
    def test_get_board_success(self, client, one_board):
        response = client.get(f"/boards/{one_board}")
        response_body = response.get_json()

        assert response.status_code == 200
        assert response_body["board_id"] == one_board
        assert response_body["title"] == "Test Board"
        assert response_body["owner"] == "Test Owner"
        assert response_body["cards"] == []

    def test_get_board_not_found(self, client):
        response = client.get("/boards/999")
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Board 999 not found"}

    def test_get_board_invalid_id(self, client):
        response = client.get("/boards/invalid")
        response_body = response.get_json()

        assert response.status_code == 400
        assert response_body == {"details": "Invalid data"}


class TestDeleteBoard:
    def test_delete_board_success(self, client, one_board):
        response = client.delete(f"/boards/{one_board}")
        response_body = response.get_json()

        assert response.status_code == 200
        assert response_body == {"details": f'Board {one_board} "Test Board" successfully deleted'}

        # Verify board is deleted
        get_response = client.get(f"/boards/{one_board}")
        assert get_response.status_code == 404

    def test_delete_board_not_found(self, client):
        response = client.delete("/boards/999")
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Board 999 not found"}

    def test_delete_board_invalid_id(self, client):
        response = client.delete("/boards/invalid")
        response_body = response.get_json()

        assert response.status_code == 400
        assert response_body == {"details": "Invalid data"}


class TestCreateCardOnBoard:
    def test_create_card_on_board_success(self, client, one_board):
        response = client.post(f"/boards/{one_board}/cards", json={
            "message": "New Card Message"
        })
        response_body = response.get_json()

        assert response.status_code == 201
        assert response_body["message"] == "New Card Message"
        assert response_body["likes_count"] == 0
        assert "card_id" in response_body

    def test_create_card_on_board_with_likes(self, client, one_board):
        response = client.post(f"/boards/{one_board}/cards", json={
            "message": "Card with likes",
            "likes_count": 5
        })
        response_body = response.get_json()

        assert response.status_code == 201
        assert response_body["likes_count"] == 5

    def test_create_card_board_not_found(self, client):
        response = client.post("/boards/999/cards", json={
            "message": "New Card"
        })
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Board 999 not found"}

    def test_create_card_missing_message(self, client, one_board):
        response = client.post(f"/boards/{one_board}/cards", json={})
        response_body = response.get_json()

        assert response.status_code == 400
        assert response_body == {"details": "Invalid data"}


class TestGetCardsOnBoard:
    def test_get_cards_on_board_empty(self, client, one_board):
        response = client.get(f"/boards/{one_board}/cards")
        response_body = response.get_json()

        assert response.status_code == 200
        assert response_body == {"cards": []}

    def test_get_cards_on_board_with_cards(self, client, board_with_cards):
        board_id = board_with_cards["board_id"]
        response = client.get(f"/boards/{board_id}/cards")
        response_body = response.get_json()

        assert response.status_code == 200
        assert len(response_body["cards"]) == 2
        assert response_body["cards"][0]["message"] == "Card One"
        assert response_body["cards"][1]["message"] == "Card Two"

    def test_get_cards_board_not_found(self, client):
        response = client.get("/boards/999/cards")
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Board 999 not found"}


class TestDeleteCardOnBoard:
    def test_delete_card_on_board_success(self, client, board_with_cards):
        board_id = board_with_cards["board_id"]
        card_id = board_with_cards["card_ids"][0]

        response = client.delete(f"/boards/{board_id}/{card_id}")
        response_body = response.get_json()

        assert response.status_code == 200
        assert response_body == {"details": f"Card {card_id} successfully deleted from Board {board_id}"}

    def test_delete_card_board_not_found(self, client, one_card):
        response = client.delete(f"/boards/999/{one_card}")
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Board 999 not found"}

    def test_delete_card_not_found(self, client, one_board):
        response = client.delete(f"/boards/{one_board}/999")
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Card 999 not found"}

    def test_delete_card_wrong_board(self, client, app, board_with_cards):
        # Create another board
        with app.app_context():
            other_board = Board(title="Other Board", owner="Other Owner")
            db.session.add(other_board)
            db.session.commit()
            other_board_id = other_board.board_id

        card_id = board_with_cards["card_ids"][0]
        response = client.delete(f"/boards/{other_board_id}/{card_id}")
        response_body = response.get_json()

        assert response.status_code == 400
        assert response_body == {"details": f"Card {card_id} does not belong to Board {other_board_id}"}


class TestLikeCardOnBoard:
    def test_like_card_on_board_success(self, client, board_with_cards):
        board_id = board_with_cards["board_id"]
        card_id = board_with_cards["card_ids"][0]

        response = client.patch(f"/boards/{board_id}/cards/{card_id}/like")
        response_body = response.get_json()

        assert response.status_code == 200
        assert response_body["card_id"] == card_id
        assert response_body["likes_count"] == 6  # Was 5, now 6
        assert response_body["board_id"] == board_id

    def test_like_card_multiple_times(self, client, board_with_cards):
        board_id = board_with_cards["board_id"]
        card_id = board_with_cards["card_ids"][0]

        # Like twice
        client.patch(f"/boards/{board_id}/cards/{card_id}/like")
        response = client.patch(f"/boards/{board_id}/cards/{card_id}/like")
        response_body = response.get_json()

        assert response.status_code == 200
        assert response_body["likes_count"] == 7  # Was 5, now 7

    def test_like_card_board_not_found(self, client, one_card):
        response = client.patch(f"/boards/999/cards/{one_card}/like")
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Board 999 not found"}

    def test_like_card_not_found(self, client, one_board):
        response = client.patch(f"/boards/{one_board}/cards/999/like")
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Card 999 not found"}

    def test_like_card_wrong_board(self, client, app, board_with_cards):
        # Create another board
        with app.app_context():
            other_board = Board(title="Other Board", owner="Other Owner")
            db.session.add(other_board)
            db.session.commit()
            other_board_id = other_board.board_id

        card_id = board_with_cards["card_ids"][0]
        response = client.patch(f"/boards/{other_board_id}/cards/{card_id}/like")
        response_body = response.get_json()

        assert response.status_code == 404
        assert response_body == {"details": "Card does not belong to this board"}