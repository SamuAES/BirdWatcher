from db import db
from sqlalchemy.sql import text

def get_bird_names():
    sql = "SELECT species_en FROM Birds"
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_bird_details(birdname):
    sql = "SELECT * FROM Birds WHERE species_en = :birdname"
    result = db.session.execute(text(sql), {"birdname": birdname})
    result = result.fetchone()
    return result

