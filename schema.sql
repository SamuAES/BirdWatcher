CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    moderator BOOLEAN
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
CREATE TABLE FollowList (
    match_id INTEGER UNIQUE,
    user_id INTEGER REFERENCES Users,
    follow_id INTEGER REFERENCES Users
);
CREATE TABLE Blacklist (
    id INTEGER REFERENCES Users,
    permanent BOOLEAN,
    ban_length TIMESTAMP,
    reason TEXT,
    unbanned BOOLEAN DEFAULT false
);
