from db import db
import users
from sqlalchemy.sql import text

def get_list(user_id = None):
    if user_id is None:
        sql = "SELECT U.username, S.bird_name, S.time, S.location, S.id, S.additional_info FROM users U, sightings S WHERE U.id = S.user_id ORDER BY S.time DESC"
        result = db.session.execute(text(sql))
    else:
        sql = "SELECT bird_name, time, location FROM sightings WHERE user_id = :user_id ORDER BY time DESC"
        result = db.session.execute(text(sql), {"user_id":user_id})
    
    return result.fetchall()

def new_sighting(bird_name, time, location, additional_info):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO sightings (user_id, bird_name, time, location, additional_info ) VALUES (:user_id, :bird_name, :time, :location, :additional_info)"
    db.session.execute(text(sql), {"user_id":user_id, "bird_name":bird_name, "time":time, "location":location, "additional_info":additional_info})
    db.session.commit()
    return True

def get_comments():
    sql = "SELECT C.sighting_id, U.username, C.content, C.sent_at FROM comments C, users U WHERE C.user_id = U.id"
    result = db.session.execute(text(sql))
    return result.fetchall()

def add_comment(sighting_id, content):
    user_id = users.user_id()
    sql = "INSERT INTO comments (sighting_id, user_id, content, sent_at) VALUES (:sighting_id, :user_id, :content, NOW())"
    db.session.execute(text(sql), {"sighting_id":sighting_id, "user_id":user_id, "content":content})
    db.session.commit()
    
