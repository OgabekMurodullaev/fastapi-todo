import logging
from typing import Any
import traceback
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from todo_app.database.models import Todo

object_type_hint = Todo
objects_type_hints = list[Todo] | list


class ORMBase:

    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, **object_data: dict):
        try:
            object_data = self.model(**object_data)
            db.add(object_data)
            db.commit()
            db.refresh(object_data)
            return object_data
        except IntegrityError:
            logging.info("Already added to the database.")
            db.rollback()
            raise HTTPException(status_code=400, detail="Object already exists.")
        except Exception as e:
            logging.info(f"An error occurred: {e}\n{traceback.format_exc()}")
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, db: Session, id: int, **updated_data) -> object_type_hint:
        try:
            obj = db.query(self.model).get(id)

            if not obj:
                raise ValueError(f"Object with ID {id} not found")

            for key, value in updated_data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)

            db.commit()
            return obj
        except Exception as e:
            logging.error(f"An error occurring update while updating object: {e}")
            raise

    def delete(self, db: Session, id: int) -> Any:
        try:
            obj = db.query(self.model).get(id)

            if obj is not None:
                db.delete(obj)
                db.commit()
                return True

        except Exception as e:
            logging.error(f"An error occurring: {e}")
            return False

    def all(self, db: Session) -> objects_type_hints:
        return db.query(self.model).all()

    def filter(self, db: Session, **filters) -> objects_type_hints:
        try:
            query = db.query(self.model)

            conditions = []
            for key, value in filters.items():
                if hasattr(self.model, key):
                    conditions.append(getattr(self.model, key) == value)  # Basic comparison

                    if "logic" in filters and filters["logic"].lower() == "or":
                        query = query.filter(or_(*conditions))  # Combine filters with OR (default)
                    else:
                        query = query.filter(and_(*conditions))  # Combine filters with AND

                    return query.all()  # Fetch all filtered objects
        except Exception as e:
            logging.error(f"An error occurred while filtering users: {e}")
            raise  # Re-raise the exception for handling outside the function

    def count(self, db: Session) -> int:
        return db.query(self.model).count()

    def get_or_create(self, db: Session, **data) -> object_type_hint:
        get = self.get(db, data["id"])
        if get is None:
            return self.create(db, **data)
        else:
            return get

TodoDB = ORMBase(model=Todo)