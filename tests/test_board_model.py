from app.models.board import Board
from app.db import db
import pytest

# @pytest.mark.skip(reason="Test skipped")
def test_board_to_dict():
    #Arrange
    new_board = Board(board_id = 1, title="Holiday Plans", 
                    owner="Alice")
    
    #Act
    board_dict = new_board.to_dict()

    #Assert
    assert len(board_dict) == 4
    assert board_dict["board_id"] == 1
    assert board_dict["title"] == "Holiday Plans"
    assert board_dict["owner"] == "Alice"
    assert board_dict["cards"] == []

# @pytest.mark.skip(reason="Test skipped")
def test_board_to_dict_missing_id():
    #Arrange
    new_board = Board(title="Holiday Plans", 
                    owner="Alice")
    
    #Act
    board_dict = new_board.to_dict()

    #Assert
    assert len(board_dict) == 4
    assert board_dict["board_id"] is None
    assert board_dict["title"] == "Holiday Plans"
    assert board_dict["owner"] == "Alice"
    assert board_dict["cards"] == []

# @pytest.mark.skip(reason="Test skipped")
def test_board_to_dict_missing_title():
    #Arrange
    new_board = Board(board_id = 1,
                    owner="Alice")
    
    #Act
    board_dict = new_board.to_dict()

    #Assert
    assert len(board_dict) == 4
    assert board_dict["board_id"] == 1
    assert board_dict["title"] is None
    assert board_dict["owner"] == "Alice"
    assert board_dict["cards"] == []

# @pytest.mark.skip(reason="Test skipped")
def test_board_to_dict_missing_owner():
    #Arrange
    new_board = Board(board_id = 1, title="Holiday Plans")
    
    #Act
    board_dict = new_board.to_dict()

    #Assert
    assert len(board_dict) == 4
    assert board_dict["board_id"] == 1
    assert board_dict["title"] == "Holiday Plans"
    assert board_dict["owner"] is None
    assert board_dict["cards"] == []

# @pytest.mark.skip(reason="Test skipped")
def test_board_from_dict():
    #Arrange
    board_dict =  {
        "title": "Holiday Plans",
        "owner": "Alice"
    }

    #Act
    board_obj =  Board.from_dict(board_dict)

    #Assert
    assert board_obj.title == "Holiday Plans"
    assert board_obj.owner == "Alice"

# @pytest.mark.skip(reason="Test skipped")
def test_board_from_dict_no_title():
    #Arrange
    board_dict =  {
        "owner": "Alice",
    }

    #Act & Assert
    with pytest.raises(KeyError, match = 'title'):
        Board.from_dict(board_dict)

# @pytest.mark.skip(reason="Test skipped")
def test_board_from_dict_no_owner():
    #Arrange
    task_dict =  {
        "title": "Holiday Plans"
    }

    #Act & Assert
    with pytest.raises(KeyError, match = 'owner'):
        Board.from_dict(task_dict)