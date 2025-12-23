from app.models.card import Card
from app.db import db
import pytest

# @pytest.mark.skip(reason="Test skipped")
def test_card_to_dict():
    #Arrange
    new_card = Card(card_id = 1, message="Buy gifts", 
                    likes_count=1)
    
    #Act
    card_dict = new_card.to_dict()
    #Assert
    assert len(card_dict) == 3
    assert card_dict["card_id"] == 1
    assert card_dict["message"] == "Buy gifts"
    assert card_dict["likes_count"] == 1

# @pytest.mark.skip(reason="Test skipped")
def test_card_to_dict_missing_id():
    #Arrange
    new_card = Card(message="Buy gifts", 
                    likes_count=1)
    
    #Act
    card_dict = new_card.to_dict()
    #Assert
    assert len(card_dict) == 3
    assert card_dict["card_id"] is None
    assert card_dict["message"] == "Buy gifts"
    assert card_dict["likes_count"] == 1

# @pytest.mark.skip(reason="Test skipped")
def test_card_to_dict_missing_message():
    #Arrange
    new_card = Card(card_id = 1, 
                    likes_count=1)
    
    #Act
    card_dict = new_card.to_dict()
    #Assert
    assert len(card_dict) == 3
    assert card_dict["card_id"] == 1
    assert card_dict["message"] is None
    assert card_dict["likes_count"] == 1

# @pytest.mark.skip(reason="Test skipped")
def test_card_to_dict_missing_likes_count():
    #Arrange
    new_card = Card(card_id = 1, message="Buy gifts", 
                    likes_count=None)
    
    #Act
    card_dict = new_card.to_dict()
    #Assert
    assert len(card_dict) == 3
    assert card_dict["card_id"] == 1
    assert card_dict["message"] == "Buy gifts"
    assert card_dict["likes_count"] is None

# @pytest.mark.skip(reason="Test skipped")
def test_card_from_dict():
    #Arrange
    card_dict =  {
        "message": "Buy gifts",
        "likes_count": 1,
        "board_id": 1
    }

    #Act
    card_obj =  Card.from_dict(card_dict)

    #Assert
    assert card_obj.message == "Buy gifts"
    assert card_obj.likes_count == 1
    assert card_obj.board_id == 1

# @pytest.mark.skip(reason="Test skipped")
def test_card_from_dict_missing_likes_count_set_default():
    #Arrange
    card_dict =  {
        "message": "Buy gifts",
        "board_id": 1
    }

    #Act
    card_obj =  Card.from_dict(card_dict)

    #Assert
    assert card_obj.message == "Buy gifts"
    assert card_obj.likes_count == 0
    assert card_obj.board_id == 1

# @pytest.mark.skip(reason="Test skipped")
def test_card_from_dict_missing_message():
    #Arrange
    card_dict =  {
        "likes_count": 1,
        "board_id": 1
    }

    #Act & Assert
    with pytest.raises(KeyError, match = 'message'):
        Card.from_dict(card_dict)

# @pytest.mark.skip(reason="Test skipped")
def test_card_from_dict_missing_board_id():
    #Arrange
    card_dict =  {
        "likes_count": 1,
        "message": "Buy gifts"
    }

    #Act & Assert
    with pytest.raises(KeyError, match = 'board_id'):
        Card.from_dict(card_dict)