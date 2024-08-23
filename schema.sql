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
    user_id INTEGER UNIQUE REFERENCES Users,
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
CREATE TABLE Birds (
    orders TEXT,
    family_sci TEXT,
    family_en TEXT,
    genus TEXT,
    species_sci TEXT,
    authority TEXT,
    species_en TEXT PRIMARY KEY,
    breeding_range TEXT,
    breeding_range_subregions TEXT,
    nonbreeding_range TEXT
    );
