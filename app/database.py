from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# from . import models
# import time
# from psycopg2 import connect
# from psycopg2.extras import RealDictCursor
# TODO move this line to the secrets
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    },
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
print("✨🎉Connected to database successfully ✨🎉")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# for reference if you wanna use sql directly:
# while True:
#     try:
#         # TODO: move to config
#         conn = connect(
#             database="postgres",
#             user="postgres",
#             password="admin",
#             host="localhost",
#             port="5432",
#             cursor_factory=RealDictCursor,
#         )
#         cur = conn.cursor()
#         print("✨🎉Connected to database successfully ✨🎉")

#         # create all tables if they don't exist
#         # cur.execute("SELECT * FROM posts")
#         # my_posts = cur.fetchall()
#         break
#     except Exception as e:
#         print("😐 Error:", e)
#         print("Trying to connect to database again in 5 seconds...")
#         time.sleep(5)
