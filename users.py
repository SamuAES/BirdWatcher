from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from os import getenv
from secrets import token_hex

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
            session["csrf_token"] = token_hex(16)
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
    del session["csrf_token"]
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

def add_bio(favourite_bird, age, bio):
    try:
        id = user_id()
        sql = "INSERT INTO Bios (user_id, favourite_bird, age, bio) VALUES (:id, :favourite_bird, :age, :bio)"
        db.session.execute(text(sql), {"id":id, "favourite_bird":favourite_bird, "age":age, "bio":bio})
        db.session.commit()
        return True
    except:
        return False

def edit_bio(favourite_bird, age, bio):
    try:
        id = user_id()
        sql = "UPDATE Bios SET favourite_bird = :favourite_bird, age = :age, bio = :bio WHERE user_id = :id"
        db.session.execute(text(sql), {"id":id, "favourite_bird":favourite_bird, "age":age, "bio":bio})
        db.session.commit()
        return True
    except:
        return False


def get_bio(id):
    sql = "SELECT favourite_bird, age, bio FROM Bios WHERE user_id = :id"
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



    
def get_blacklist():
    sql = "SELECT U.username, B.reason, B.date FROM Users U, Blacklist B WHERE B.user_id = U.id"
    result = db.session.execute(text(sql))
    return result.fetchall()

def check_blacklist(username):
    id = get_id_by_username(username)
    if id is False:
        return False
    sql = "SELECT user_id FROM Blacklist WHERE user_id = :id"
    result = db.session.execute(text(sql), {"id": id})
    result = result.fetchone()
    if result:
        return True
    else:
        return False
    
def ban_user(user_id, reason):
    try:
        sql = "INSERT INTO Blacklist (user_id, reason, date) VALUES (:user_id, :reason, NOW())"
        db.session.execute(text(sql), {"user_id": user_id, "reason": reason})
        db.session.commit()
        return True
    except:
        return "No user with that name or user is already banned."

def unban_user(user_id):
    try:
        sql = "DELETE FROM Blacklist WHERE user_id = :user_id"
        db.session.execute(text(sql), {"user_id": user_id})
        db.session.commit()
        return True
    except:
        return "Something went wrong..."
