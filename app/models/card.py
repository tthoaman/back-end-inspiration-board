from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db

class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(nullable=False)
    likes_count: Mapped[int] = mapped_column(nullable=False)      
    board_id: Mapped[int] = mapped_column(ForeignKey("board.board_id"), nullable=False)
    board: Mapped["Board"] = relationship(back_populates="cards")
    
    def to_dict(self):
        card_as_dict = {
            "card_id": getattr(self, "card_id", None),
            "message": getattr(self, "message", None),
            "likes_count": getattr(self, "likes_count", None),
            "board_id": getattr(self, "board_id", None)
        }
        if self.board:
            card_as_dict["board_id"] = self.board_id
        return card_as_dict
    
    @classmethod
    def from_dict(cls, dict):
        return cls(
            message=dict["message"],
            likes_count=dict["likes_count"],
            board_id=dict.get("board_id")
        )