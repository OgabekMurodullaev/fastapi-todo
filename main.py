import uvicorn
from fastapi import FastAPI

from todo_app.database.config import Base, engine
from todo_app.routes import todo_router, index_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todo_router)
app.include_router(index_router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)