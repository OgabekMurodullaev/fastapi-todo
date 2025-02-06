from sqlalchemy import Column, Integer, String, Boolean

from todo_app.database.config import Base



class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    done: str = Column(Boolean, default=False)