from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import db


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks = relationship('Task', back_populates='goal', cascade='all, delete-orphan')

    def to_dict(self, noTasks=True):
        result = {"id": self.id, "title": self.title, }
        if noTasks:
            return result
        tasks = []
        for task in self.tasks:
            tasks.append({"id": task.id,
                          "goal_id": task.goal_id,
                          "title": task.title,
                          "description": task.description,
                          "is_complete": task.completed_at is not None})
        result["tasks"] = tasks
        return result
