from db import db
import users
from sqlalchemy.sql import text


def get_all_sightings(user_id = None):
    if user_id is None:
        sql = "SELECT S.id, U.username, S.bird_name, S.time, S.location, S.additional_info FROM Users U, Sightings S WHERE U.id = S.user_id AND S.visibility = true ORDER BY S.time DESC"
        result = db.session.execute(text(sql))
    else:
        sql = "SELECT S.id, U.username, S.bird_name, S.time, S.location, S.additional_info FROM Users U, Sightings S WHERE U.id = S.user_id AND U.id = :user_id AND S.visibility = true ORDER BY S.time DESC"
        result = db.session.execute(text(sql), {"user_id":user_id})
    return result.fetchall()

def get_sightings_by_name(birdname):
    sql = "SELECT S.id, U.username, S.bird_name, S.time, S.location, S.additional_info FROM Users U, Sightings S WHERE U.id = S.user_id AND S.bird_name = :birdname AND S.visibility = true ORDER BY S.time DESC"
    result = db.session.execute(text(sql), {"birdname": birdname})
    return result.fetchall()

def get_follows_sightings(follows_id_numbers):
    try:
        sql = "SELECT S.id, U.username, S.bird_name, S.time, S.location, S.additional_info FROM Users U, Sightings S WHERE U.id = S.user_id AND U.id IN :follows_id_numbers AND S.visibility = true ORDER BY S.time DESC"
        result = db.session.execute(text(sql), {"follows_id_numbers": tuple(follows_id_numbers) })
        return result.fetchall()
    except:
        return False

def get_sighting_details(id):
    sql = "SELECT U.username, S.bird_name, S.time, S.location, S.additional_info FROM Users U, Sightings S WHERE S.id = :id AND U.id = S.user_id"
    result = db.session.execute(text(sql), {"id": id})
    result = result.fetchone()
    return result

def get_image(id):
    sql = "SELECT data FROM Images WHERE sighting_id = :id"
    result = db.session.execute(text(sql), {"id":id})
    result = result.fetchone()
    if result is None:
        return False
    
    return result[0]


def new_sighting(bird_name, time, location, additional_info, image):
    user_id = users.user_id()
    if user_id == 0:
        return "You must be logged in!"
    
    # If no image is sent then add new sighting.
    name = image.filename
    if name == "":
        sql = "INSERT INTO Sightings (user_id, bird_name, time, location, additional_info, visibility ) VALUES (:user_id, :bird_name, :time, :location, :additional_info, true)"
        db.session.execute(text(sql), {"user_id":user_id, "bird_name":bird_name, "time":time, "location":location, "additional_info":additional_info})
        db.session.commit()
        return True
    
    # Check for filename and size
    if not (name.endswith(".jpg") or name.endswith(".png")):
        return "Image type must be jpg or png and size below 100kb"
    data = image.read()
    if len(data) > 100*1024:
        return "Image type must be jpg or png and size below 100kb"
    
    sql = "INSERT INTO Sightings (user_id, bird_name, time, location, additional_info, visibility ) VALUES (:user_id, :bird_name, :time, :location, :additional_info, true)"
    db.session.execute(text(sql), {"user_id":user_id, "bird_name":bird_name, "time":time, "location":location, "additional_info":additional_info})
    db.session.commit()
    
    # Get sighting id so image may be referenced to it.
    sql = "SELECT id FROM Sightings WHERE user_id = :user_id AND bird_name = :bird_name AND time = :time AND location = :location"
    result = db.session.execute(text(sql), {"user_id":user_id, "bird_name":bird_name, "time":time, "location":location})
    id_number = result.fetchone()
    if id_number is None:
        return "Something went wrong"
    
    id_number = id_number[0]

    sql = "INSERT INTO Images (sighting_id, name, data, visibility) VALUES (:sighting_id, :name, :data, true)"
    db.session.execute( text(sql), {"sighting_id":id_number, "name":name, "data":data})
    db.session.commit()
    return True


def valid_bird_name(bird_name:str) -> bool:
    # Check if a bird is selected.
    if bird_name == "":
        return False
    else:
        return True

def delete_sighting(sighting_id):
    sql = "UPDATE Sightings SET visibility = false WHERE id = :id"
    db.session.execute(text(sql), {"id": sighting_id})
    db.session.commit()


