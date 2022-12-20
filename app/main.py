from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# validation schema for post
class Post(BaseModel):
    title: str
    content: str
    # optional property can be set with a default value
    published: bool = False
    # or with the Optional object
    #rating: Optional[int] = None

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status" : "success"}

# decorator @app + url
@app.get("/")
def getHelloWorld():
    return {"message": "Hello world"}

# first post call, payload define a dict and import Body from fastapi
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING * """,
                   (post.title, post.content))
    new_post = cursor.fetchone()
    # to save data in the db we have to reference the connection and do a commit
    conn.commit()
    return {"data": new_post}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
# inside the function parameter I state that id must be an int
def get_post(id: int, response: Response):
    # apparently the comma after str(id) is SUPER important for SOME reason
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post_with_id = cursor.fetchone()
    if not post_with_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    return {"data": post_with_id}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(
        """ DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):

    cursor.execute(""" UPDATE posts SET title =%s, content=%s WHERE id = %s RETURNING * """,
                   (post.title, post.content, str(id),))
    updated_post = cursor.fetchone()
    # to save data in the db we have to reference the connection and do a commit
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    post_dict = post.dict()

    return Response(status_code=status.HTTP_202_ACCEPTED)
