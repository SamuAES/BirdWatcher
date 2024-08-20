from db import db
from sqlalchemy.sql import text
from users import user_id, get_id_by_username

def add_follow(username):
    user = user_id()
    sql = "SELECT id FROM Users WHERE username = :username"
    result = db.session.execute(text(sql), {"username":username})
    follow_id = result.fetchone()
    
    if follow_id is None:
        return "No user with that name."
    follow_id = follow_id[0]
    if follow_id == user:
        return "You can't follow yourself."
        
    try:
        match_id = int(f"{user}{follow_id}")
        sql = "INSERT INTO Followers (match_id, user_id, follow_id) VALUES (:match_id, :user_id, :follow_id)"
        db.session.execute(text(sql), {"match_id":match_id, "user_id":user, "follow_id":follow_id})
        db.session.commit()
        return True
    except:
        return "You are already following that user."
    
def stop_follow(username):
    user = user_id()
    follow_id = get_id_by_username(username)
    sql = "DELETE FROM Followers WHERE user_id = :user_id AND follow_id = :follow_id"
    try:
        db.session.execute(text(sql), {"user_id":user, "follow_id":follow_id})
        db.session.commit()
        return True
    except:
        return False
    
    

def get_followslist():
    user = user_id()
    sql = "SELECT U.username FROM Users U, Followers F WHERE F.user_id = :user_id AND F.follow_id = U.id"
    result = db.session.execute(text(sql), {"user_id": user})
    return result.fetchall()

def get_followerlist():
    user = user_id()
    sql = "SELECT U.username FROM Users U, Followers F WHERE F.follow_id = :user_id AND F.user_id = U.id"
    result = db.session.execute(text(sql), {"user_id": user})
    return result.fetchall()

def is_following(username):
    user = user_id()
    follow_id = get_id_by_username(username)
    sql = "SELECT * FROM Followers WHERE user_id = :user_id AND follow_id = :target_id"
    result = db.session.execute(text(sql), {"user_id":user, "target_id":follow_id}).fetchone()
    
    if result is None:
        return False
    else:
        return True