from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db

class Board(db.Model):
    board_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    owner: Mapped[str] = mapped_column(nullable=False)
    cards: Mapped[list["Card"]] = relationship("Card", back_populates="board")

    def to_dict(self):
        board_dict = {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,
            "cards": [card.to_dict() for card in self.cards]
        }

        return board_dict

    @classmethod
    def from_dict(cls, board_data):
        title = board_data["title"]
        owner = board_data["owner"]

        return cls(title=title, owner=owner)