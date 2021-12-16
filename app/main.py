# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote
from .database import engine
from . import models

# init app
app = FastAPI()

# No need for this anymore since we are using Alembic that will build tables for us
# models.Base.metadata.create_all(bind=engine)

# add CORS
# add accepted origins
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# test endpoint
@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic! 🎉"}
