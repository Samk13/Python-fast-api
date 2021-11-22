from fastapi import FastAPI
from .routers import post, user, auth, vote
from .database import engine
from . import models

# init app
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# add routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# test endpoint
@app.get("/")
def root():
    return {"message": "THis Python API using fast API"}
