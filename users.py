from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(username, password):
    sql = "SELECT id, password FROM Users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (username,password,moderator) VALUES (:username, :password, false)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def get_username():
    return session.get("username", 0)

def get_id_by_username(username):
    sql = "SELECT id FROM Users WHERE username = :username"
    result = db.session.execute(text(sql), {"username":username})
    id_number = result.fetchone()
    if id_number is None:
        return False
    return id_number[0]

def is_user():
    try:
        if session["user_id"] == user_id():
            return True
    except:
        return False

