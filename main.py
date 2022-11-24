from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel 

app = FastAPI()

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
@app.post("/createPosts")
def createPosts(new_post: Post):
    print(new_post.title)
    return {"data" : "A new post has been created"}