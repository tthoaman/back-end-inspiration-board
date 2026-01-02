import pytest
from app import create_app
from app.db import db
from app.models.board import Board
from app.models.card import Card

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.rollback()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_board(app):
    with app.app_context():
        board = Board(title="Test Board", owner="Test Owner")
        db.session.add(board)
        db.session.commit()
        return board.board_id

@pytest.fixture
def two_boards(app):
    with app.app_context():
        board1 = Board(title="Board One", owner="Owner One")
        board2 = Board(title="Board Two", owner="Owner Two")
        db.session.add_all([board1, board2])
        db.session.commit()
        return [board1.board_id, board2.board_id]

@pytest.fixture
def one_card(app, one_board):
    with app.app_context():
        card = Card(message="Test Message", likes_count=0, board_id=one_board)
        db.session.add(card)
        db.session.commit()
        return card.card_id

@pytest.fixture
def board_with_cards(app):
    with app.app_context():
        board = Board(title="Board with Cards", owner="Owner")
        db.session.add(board)
        db.session.commit()

        card1 = Card(message="Card One", likes_count=5, board_id=board.board_id)
        card2 = Card(message="Card Two", likes_count=10, board_id=board.board_id)
        db.session.add_all([card1, card2])
        db.session.commit()

        return {
            "board_id": board.board_id,
            "card_ids": [card1.card_id, card2.card_id]
        }