from fastapi import Body, FastAPI

app = FastAPI()

# decorator @app + url
@app.get("/")
def getHelloWorld():
    return {"message" : "Hello world"}

@app.get("/welcomeMessage")
def getHelloWorld():
    return {"message" : "Welcome to this FAST API tutorial"}

# first post call, payload define a dict and import Body from fastapi
@app.post("/createPosts")
def createPosts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"new_post" : f"title {payLoad['title']} content: {payLoad['content']}"}