CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    sent_at TIMESTAMP
);
CREATE TABLE sightings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    bird_name TEXT,
    time TIMESTAMP,
    location TEXT,
    additional_info TEXT
);
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    sighting_id INTEGER REFERENCES sightings,
    user_id INTEGER REFERENCES users,
    content TEXT,
    sent_at TIMESTAMP
);
CREATE TABLE friendlist (
    match_id INTEGER UNIQUE,
    user_id INTEGER REFERENCES users,
    friend_id INTEGER REFERENCES users
)