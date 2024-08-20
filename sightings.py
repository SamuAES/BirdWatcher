from db import db
from app import birdlist
import users
from sqlalchemy.sql import text

def get_sightings(user_id = None):
    if user_id is None:
        sql = "SELECT U.username, S.bird_name, S.time, S.location, S.id, S.additional_info FROM Users U, Sightings S WHERE U.id = S.user_id AND S.visibility = true ORDER BY S.time DESC"
        result = db.session.execute(text(sql))
    else:
        sql = "SELECT U.username, S.bird_name, S.time, S.location, S.id, S.additional_info FROM Users U, Sightings S WHERE U.id = S.user_id AND U.id = :user_id AND S.visibility = true ORDER BY S.time DESC"
        result = db.session.execute(text(sql), {"user_id":user_id})
    
    return result.fetchall()

def new_sighting(bird_name, time, location, additional_info):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO Sightings (user_id, bird_name, time, location, additional_info, visibility ) VALUES (:user_id, :bird_name, :time, :location, :additional_info, true)"
    db.session.execute(text(sql), {"user_id":user_id, "bird_name":bird_name, "time":time, "location":location, "additional_info":additional_info})
    db.session.commit()
    return True

def get_comments():
    sql = "SELECT C.sighting_id, U.username, C.content, C.sent_at, C.id FROM Comments C, Users U WHERE C.user_id = U.id AND visibility = true"
    result = db.session.execute(text(sql))
    return result.fetchall()

def add_comment(sighting_id, content):
    user_id = users.user_id()
    sql = "INSERT INTO Comments (sighting_id, user_id, content, sent_at, visibility) VALUES (:sighting_id, :user_id, :content, NOW(), true)"
    db.session.execute(text(sql), {"sighting_id":sighting_id, "user_id":user_id, "content":content})
    db.session.commit()

def valid_bird_name(bird_name:str) -> bool:
    """
    Check if bird name is selected for new sighting.
    """
    if bird_name == "":
        return False
    else:
        return True

def delete_comment(comment_id):
    sql = "UPDATE Comments SET visibility = false WHERE id = :id"
    db.session.execute(text(sql), {"id": comment_id})
    db.session.commit()

def delete_sighting(sighting_id):
    sql = "UPDATE Sightings SET visibility = false WHERE id = :id"
    db.session.execute(text(sql), {"id": sighting_id})
    db.session.commit()


