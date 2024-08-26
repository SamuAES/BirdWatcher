from db import db
import users
from sqlalchemy.sql import text


def add_comment(sighting_id, content):
    user_id = users.user_id()
    sql = "INSERT INTO Comments (sighting_id, user_id, content, sent_at, visibility) VALUES (:sighting_id, :user_id, :content, NOW(), true)"
    db.session.execute(text(sql), {"sighting_id":sighting_id, "user_id":user_id, "content":content})
    db.session.commit()

def get_comments(sighting_id):
    sql = "SELECT U.username, C.content, C.sent_at, C.id FROM Comments C, Users U WHERE C.sighting_id = :id AND C.user_id = U.id AND C.visibility = true"
    result = db.session.execute(text(sql), {"id": sighting_id})
    return result.fetchall()

def get_nof_comments(sighting_id):
    sql = "SELECT COUNT(*) FROM Comments WHERE sighting_id = :sighting_id"
    result = db.session.execute(text(sql), {"sighting_id":sighting_id})
    return result.fetchone()

def delete_comment(comment_id):
    sql = "UPDATE Comments SET visibility = false WHERE id = :id"
    db.session.execute(text(sql), {"id": comment_id})
    db.session.commit()