from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel 

app = FastAPI()
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": "2"}, 
{"title": "title of post 1", "content": "content of post 1", "id": "2"}]

# validation schema for post
class Post(BaseModel):
    title: str
    content: str
    # optional property can be set with a default value
    published: bool = False
    #or with the Optional object
    rating: Optional[int] = None

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
    print(post.dict())
    return {"data" : "A new post has been created"}

# first post call, payload define a dict and import Body from fastapi
@app.get("/posts")
def get_posts():
    return {"data" : my_posts}