from datetime import datetime

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    goal_id = db.Column(Integer, ForeignKey('goal.id'), nullable=True)
    goal = relationship('Goal', back_populates='tasks')

    def to_dict(self):
        result = dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at != None)
        if self.goal is not None:
            result["goal_id"] = self.goal.id
        return result
