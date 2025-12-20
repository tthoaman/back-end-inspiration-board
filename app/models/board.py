from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Board(db.Model):
    board_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="board")

    def to_dict(self):
        return {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }

    @classmethod
    def from_dict(cls, goal_data):
        return cls(title=goal_data["title"])