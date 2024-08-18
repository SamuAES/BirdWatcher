# BirdWatcher
Share and comment on your bird sightings with other bird watchers!

BirdWatcher is a web application where you can:

● Create and log in to your account.

● Record the time, date and location of your bird sighting.

● Add additional information about the sighting for example the weather conditions and the events that lead to the observation.

● See what birds other people have seen.

● Reply to comments about your sightings and comment on other peoples bird sightings.

● Follow users so you can see easily what birds they have spotted recently!

# Current stage of development

● Currently you can create an account and log in.

● You can add new bird sightings and see what sightings other people have posted.

● You can add comments to other users sightings and you can add other people to your friend list.

● You can follow other users and you can see who is following you.

# Still in progress

● Add functionalities to management page so admin and moderators can ban/unban users and delete comments or sightings.

● Add database for birds so users can get additional information about birds if they click on bird name.

● Add funtionality that users can search for bird sightings by username or birdname.

● Customize the layout and interface of the pages.

# How to test the program

● Create a database according to schema.sql

● Create .env file and store there:

    DATABASE_URL = postgresql://username:password@host:port/dtabase_name
    SECRET_KEY = 'your secret key'
    admin = 'username'  #This username will have admin rights.

● Install python dependencies from requirements.txt

● Run flask 



