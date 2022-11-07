from fastapi import FastAPI

app = FastAPI()

# decorator @app + url
@app.get("/welcomeMessage")
def getHelloWorld():
    return {"message" : "Hello world"}