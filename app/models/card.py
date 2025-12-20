from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    like_count: Mapped[int]
    board_id: Mapped[Optional[int]] = mapped_column(ForeignKey("board.id"))
    board: Mapped[Optional["Board"]] = relationship(back_populates="cards")
    
    def to_dict(self):
        card_as_dict = {
            "card_id": getattr(self, "id", None),
            "message": getattr(self, "message", None),
            "like_count": getattr(self, "like_count", None),
            "board_id": getattr(self, "board_id", None)
        }
        if self.board:
            card_as_dict["board_id"] = self.board_id
        return card_as_dict
    
    @classmethod
    def from_dict(cls, dict):
        return cls(
            message=dict["message"],
            like_count=dict["like_count"],
            board_id=dict.get("board_id")
        )