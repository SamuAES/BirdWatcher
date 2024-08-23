from app import app
from flask import render_template, request, redirect, session
import users, sightings, followers, comments, birds
import base64
from os import getenv



@app.route("/", methods=["GET"])
def index():
    bird_sightings = sightings.get_all_sightings()
    return render_template("index.html", sightings = bird_sightings)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")
    
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.check_blacklist(username):
            return render_template("login.html", message= "That username is banned!" )
        
        if users.login(username, password):
            return redirect("/own_page")
        
        else:
            return render_template("login.html", message= "Wrong username or password." )
    
            

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        input_data = []
        return render_template("register.html", input_data = input_data)
    elif request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        
        favourite_bird = request.form["favourite_bird"]
        age = request.form["age"]
        bio = request.form["bio"]

        input_data = [username, password1, password2, favourite_bird, age, bio]

        if password1 != password2:
            return render_template("register.html", input_data = input_data, message="Passwords are not the same.")
        
        elif users.register(username, password1):
            users.add_bio(favourite_bird, age, bio)
            return redirect("/")
        
        else:
            return render_template("register.html", input_data = input_data, message="Username is already in use.")


@app.route("/management", methods=["GET", "POST"])
def management():
    # Let only admin or moderators see /managament page.
    try:
        session["moderator"]
    except:
        try:
            session["admin"]
        except:
            return redirect("/")

    moderators = users.get_moderators()
    blacklist = users.get_blacklist()

    if request.method == "GET":    

        return render_template("management.html", moderators = moderators, blacklist = blacklist)
    
    elif request.method == "POST":

        # Promote username to moderator
        try:
            username = request.form["promote_username"]
            result = users.promote_moderator(username)

            if result is True:
                return redirect("/management")
            else:
                return render_template("management.html", moderators = moderators, blacklist = blacklist, message = result)
            
        except:
            pass

        # Demote moderator
        try:
            user_id = request.form["demote_username"]
            result = users.demote_moderator(user_id)
            if result is True:
                return redirect("/management")
            else:
                return render_template("management.html", moderators = moderators, blacklist = blacklist, message = result)
        except:
            pass

        # Ban user
        try:
            username = request.form["ban_username"]
            if username == getenv("admin"):
                return render_template("management.html", moderators = moderators, blacklist = blacklist, message = "You don't want to ban admin...")
            reason = request.form["reason"]
            result = users.ban_user(users.get_id_by_username(username), reason)
            if result is True:
                return redirect("/management")
            else:
                return render_template("management.html", moderators = moderators, blacklist = blacklist, message = result)
        except:
            pass

        # Unban user
        try:
            username = request.form["unban_username"]
            result = users.unban_user(users.get_id_by_username(username))
            if result is True:
                return redirect("/management")
            else:
                return render_template("management.html", moderators = moderators, blacklist = blacklist, message = result)
        except:
            pass

 

@app.route("/all_sightings", methods=["GET"])
def all_sightings():
    bird_sightings = sightings.get_all_sightings()
    return render_template("all_sightings.html", sightings = bird_sightings)
    
        
@app.route("/sighting/<int:id>", methods=["GET", "POST"])
def sighting_id(id):

    sighting_details = sightings.get_sighting_details(id)
    bird_details = birds.get_bird_details(sighting_details.bird_name)
    
    if request.method == "GET":
        sighting_comments = comments.get_comments(id)
        data = sightings.get_image(id)
        if data is False:
            return render_template("sighting_details.html", id = id, sighting = sighting_details, bird_details = bird_details, comments = sighting_comments)
        else:
            image = base64.b64encode(data).decode("utf-8")
            return render_template("sighting_details.html", id = id, sighting = sighting_details, bird_details = bird_details, comments = sighting_comments, image = image)
    
    elif request.method == "POST":
        # add new comment
        try:    
            sighting_id = request.form["sighting_id"]
            new_comment = request.form["new_comment"]
            comments.add_comment(sighting_id, new_comment)
            return redirect(f"/sighting/{id}")
        except:
            pass

        #delete comment
        try:
            comment_id = request.form["comment_id"]
            comments.delete_comment(comment_id)
            return redirect(f"/sighting/{id}")
        except:
            pass
        
        #delete sighting
        try:
            sighting_id = request.form["sighting_id"]
            sightings.delete_sighting(sighting_id)
            return redirect(f"/profile/{sighting_details.username}")
        except:
            pass

     

@app.route("/new_sighting", methods=["GET", "POST"])
def new_sighting():
    
    birdnames = birds.get_bird_names()
    # postgres returns a tuple for some reason so we have to parse only the first object
    birdnames = [bird[0] for bird in birdnames]
    
    if request.method == "GET":
        input_data = []
        return render_template("new_sighting.html", birdnames = birdnames, input_data = input_data )
    
    elif request.method == "POST":
        # Check if bird name is valid. (Must choose something.)
        bird_name = request.form["bird_name"]
        time = request.form["time"]
        location = request.form["location"]
        additional_info = request.form["additional_info"]
        image = request.files["image"]

        input_data = [bird_name, time, location, additional_info]

        if not sightings.valid_bird_name(bird_name):
            return render_template("new_sighting.html", birdnames = birdnames, input_data = input_data, message="Must choose a bird.")

        result = sightings.new_sighting(bird_name, time, location, additional_info, image)

        if result is True:
            return redirect("/")
        else:
            return render_template("new_sighting.html", birdnames = birdnames, input_data = input_data, message=result )


@app.route("/profile/<string:username>", methods=["GET", "POST"])
def profile(username):
    
    if username == users.get_username():
        return redirect("/own_page")

    bird_sightings = sightings.get_all_sightings(users.get_id_by_username(username))
    follower = followers.is_following(username)
    bio = users.get_bio(users.get_id_by_username(username))

    if request.method == "GET":
        return render_template("profile.html", sightings = bird_sightings, username = username, follower = follower, bio = bio)
    
    if request.method == "POST":

        button_result = request.form["follow_btn"]
        
        # If user wants to unfollow
        if button_result == "unfollow":

            result = followers.stop_follow(username)
            
            if result:
                return redirect("/profile/"+username)
            
            return render_template("profile.html", sightings = bird_sightings, username = username, bio = bio, follower = follower, message="Something went wrong. Please contact support.")
        
        # If user wants to follow
        result = followers.add_follow(username)

        if result:
            return redirect("/profile/"+username)
        return render_template("profile.html", sightings = bird_sightings, username = username, bio = bio, follower = follower, message="Something went wrong. Please contact support.")





@app.route("/own_page", methods=["GET", "POST"])
def own_page():
    
    bird_sightings = sightings.get_all_sightings(users.user_id())
    followslist = followers.get_followslist()
    followerlist = followers.get_followerlist()
    bio = users.get_bio(users.user_id())

    if request.method == "GET":
        return render_template("own_page.html", sightings = bird_sightings, follows = followslist, followers = followerlist, bio = bio)
    
    elif request.method == "POST":

        # Follow new user
        try:
            follow_username = request.form["follow_username"]
            result = followers.add_follow(follow_username)

            if result is True:
                return redirect("/own_page")
            else:
                return render_template("own_page.html", sightings = bird_sightings, follows = followslist, followers = followerlist, bio = bio, message = result)
        except:
            pass
        
        # Edit bio
        try:
            name = request.form["name"]
            age = request.form["age"]
            bio = request.form["bio"]
            if users.edit_bio(name, age, bio):
                return redirect("/own_page")
        except:
            return render_template("own_page.html", sightings = bird_sightings, follows = followslist, followers = followerlist, bio = bio, message = "Wasn't able to update profile. Please contact support.")










    
    