from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "title of post 2", "content": "content of post 2", "id": 2}, ]

# validation schema for post


class Post(BaseModel):
    title: str
    content: str
    # optional property can be set with a default value
    published: bool = False
    # or with the Optional object
    rating: Optional[int] = None


def find_post_by_id(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


# decorator @app + url
@app.get("/")
def getHelloWorld():
    return {"message": "Hello world"}

# first post call, payload define a dict and import Body from fastapi


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# first post call, payload define a dict and import Body from fastapi


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/{id}")
# inside the function parameter I state that id must be an int
def get_post(id: int, response: Response):
    # instead of manually convert it id to int
    post = find_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message' : f"id: {id} was not found!"}
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return Response(status_code=status.HTTP_202_ACCEPTED)