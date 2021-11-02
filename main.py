from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World is it working?"}


@app.get("/posts")
def get_posts():
    return [
        {"id": 1, "title": "Hello World"},
        {"id": 2, "title": "Hello Galaxy"},
    ]
