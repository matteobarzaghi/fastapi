from random import randrange
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel 

app = FastAPI()
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}, ]

# validation schema for post
class Post(BaseModel):
    title: str
    content: str
    # optional property can be set with a default value
    published: bool = False
    #or with the Optional object
    rating: Optional[int] = None

def find_post_by_id(id):
    for p in my_posts:
        if p["id"] == id:
            return p 

# decorator @app + url
@app.get("/")
def getHelloWorld():
    return {"message" : "Hello world"}

@app.get("/welcomeMessage")
def getHelloWorld():
    return {"message" : "Welcome to this FAST API tutorial"}

# first post call, payload define a dict and import Body from fastapi
@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

# first post call, payload define a dict and import Body from fastapi
@app.get("/posts")
def get_posts():
    return {"data" : my_posts}


@app.get("/posts/{id}")
# inside the function parameter I state that id must be an int
def get_post(id : int):
    # instead of manually convert it id to int
    post = find_post_by_id(id)
    return {"data" : post}