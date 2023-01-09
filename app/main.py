from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# validation schema for post


class Post(BaseModel):
    title: str
    content: str
    # optional property can be set with a default value
    published: bool = False
    # or with the Optional object
    #rating: Optional[int] = None


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}
