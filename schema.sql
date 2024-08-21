CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    moderator BOOLEAN
);
CREATE TABLE Bios (
    user_id INTEGER PRIMARY KEY REFERENCES Users,
    name TEXT,
    age TEXT,
    bio TEXT
);
CREATE TABLE Sightings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
    bird_name TEXT,
    time TIMESTAMP,
    location TEXT,
    additional_info TEXT,
    visibility BOOLEAN
);
CREATE TABLE Comments (
    id SERIAL PRIMARY KEY,
    sighting_id INTEGER REFERENCES Sightings,
    user_id INTEGER REFERENCES Users,
    content TEXT,
    sent_at TIMESTAMP,
    visibility BOOLEAN
);
CREATE TABLE Followers (
    user_id INTEGER REFERENCES Users,
    follow_id INTEGER REFERENCES Users,
    UNIQUE (user_id, follow_id)
);
CREATE TABLE Blacklist (
    user_id INTEGER REFERENCES Users,
    reason TEXT,
    date TIMESTAMP
);
CREATE TABLE Images (
    id SERIAL PRIMARY KEY,
    sighting_id INTEGER REFERENCES Sightings,
    name TEXT,
    data BYTEA,
    visibility BOOLEAN
);
