# BirdWatcher
Share and comment on your bird sightings with other bird watchers!

BirdWatcher is a web application based on Python Flask library and PostgresSQL database where you can:

● Create and log in to your account.

● Record the time, date and location of your bird sighting.

● Add additional information about the sighting for example the weather conditions and the events that lead to the observation.

● Add image about your bird sighting.

● See what birds other people have seen.

● Comment on other peoples bird sightings and reply to comments about your sightings.

● Follow users so you can see easily what birds they have spotted recently!


# How to test the program

● Clone the repository.

● Create a PostgreSQL database according to schema.sql.

● Import birdlist.csv into your created database from static folder.

    You can copy csv file with following command prompt:

    COPY Birds FROM '...your_own_path\static\birdlist.csv' DELIMITER '|' CSV HEADER;

    Notice the delimiter is |.

    If you are using windows command prompt try:

    \copy Birds FROM '...your_own_path/static/birdlist.csv' DELIMITER '|' CSV HEADER;

    You can also import csv file into database using pgAdmin client.

● Create .env file to repository root and store there:

    DATABASE_URL = postgresql://username:password@host:port/dtabase_name
    SECRET_KEY = 'your secret key'
    admin = 'username'  #(This username will have admin rights.)

● Create virtual environment

● Install python dependencies from requirements.txt

● Run flask 



