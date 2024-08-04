from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
        db.session.execute(text(sql), {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def add_friend(username):
    user = user_id()
    sql = "SELECT id FROM users WHERE username = :username"
    result = db.session.execute(text(sql), {"username":username})
    friend_id = result.fetchone()
    
    if friend_id is None:
        return "No user with that name."
    friend_id = friend_id[0]
    if friend_id == user:
        return "You can't add yourself to your friendlist."
        
    
    try:
        match_id = int(f"{user}{friend_id}")
        sql = "INSERT INTO friendlist (match_id, user_id, friend_id) VALUES (:match_id, :user_id, :friend_id)"
        db.session.execute(text(sql), {"match_id":match_id, "user_id":user, "friend_id":friend_id})
        db.session.commit()
        return True
    except:
        return "That user is already your friend."
    

def get_friendlist():
    user = user_id()
    sql = "SELECT U.username FROM users U, friendlist F WHERE F.user_id = :user_id AND F.friend_id = U.id"
    result = db.session.execute(text(sql), {"user_id": user})
    return result.fetchall()