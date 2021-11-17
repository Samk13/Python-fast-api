import time
from fastapi import FastAPI
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine
from .routers import post, user

# init app
app = FastAPI()

# connect to database
while True:
    try:
        # TODO: move to config
        conn = connect(
            database="postgres",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432",
            cursor_factory=RealDictCursor,
        )
        cur = conn.cursor()
        print("✨🎉Connected to database successfully ✨🎉")

        # create all tables if they don't exist
        models.Base.metadata.create_all(bind=engine)
        # cur.execute("SELECT * FROM posts")
        # my_posts = cur.fetchall()
        break
    except Exception as e:
        print("😐 Error:", e)
        print("Trying to connect to database again in 5 seconds...")
        time.sleep(5)

# add routers
app.include_router(post.router)
app.include_router(user.router)


# test endpoint
@app.get("/")
def root():
    return {"message": "Hello World is it working?"}
