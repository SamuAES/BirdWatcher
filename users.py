from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from os import getenv

def login(username, password):
    sql = "SELECT id, password, moderator FROM Users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            if user.moderator is True:
                session["moderator"] = True

            if username == getenv("admin"):
                session["admin"] = True

            return True
        
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]
    try:
        del session["moderator"]
    except:
        pass
    try:
        del session["admin"]
    except:
        pass

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO Users (username,password,moderator) VALUES (:username, :password, false)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def add_bio(name, age, bio):
    try:
        id = user_id()
        sql = "INSERT INTO Bios (user_id, name, age, bio) VALUES (:id, :name, :age, :bio)"
        db.session.execute(text(sql), {"id":id, "name":name, "age":age, "bio":bio})
        db.session.commit()
        return True
    except:
        return False

def edit_bio(name, age, bio):
    try:
        id = user_id()
        sql = "UPDATE Bios SET name = :name, age = :age, bio = :bio WHERE user_id = :id"
        db.session.execute(text(sql), {"id":id, "name":name, "age":age, "bio":bio})
        db.session.commit()
        return True
    except:
        return False


def get_bio(id):
    sql = "SELECT name, age, bio FROM Bios WHERE user_id = :id"
    result = db.session.execute(text(sql), {"id": id})
    return result.fetchone()


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

def get_moderators():
    sql = "SELECT id, username FROM Users WHERE moderator = true"
    result = db.session.execute(text(sql))
    return result.fetchall()

def promote_moderator(username):
    sql = "SELECT id, moderator FROM Users WHERE username = :username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()

    if user is None:
        return "No user with that name."
    if user[1] == True:
        return "That user is already a moderator."

    try:
        sql = "UPDATE Users SET moderator = true WHERE id = :user_id"
        db.session.execute(text(sql), {"user_id": user[0]})
        db.session.commit()
        return True
    except:
        return "Something went wrong..."

def demote_moderator(user_id):
    try:
        sql = "UPDATE Users SET moderator = false WHERE id = :user_id"
        db.session.execute(text(sql), {"user_id": user_id})
        db.session.commit()
        return True
    except:
        return "Something went wrong..."
