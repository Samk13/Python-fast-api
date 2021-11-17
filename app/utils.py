from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def find_post(id):
    for post in my_posts:
        if int(post["id"]) == int(id):
            return post
    return None
