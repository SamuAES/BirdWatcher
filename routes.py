from app import app, birdlist
from flask import render_template, request, redirect, session
import users, sightings, followers



@app.route("/", methods=["GET"])
def index():
    bird_sightings = sightings.get_sightings()
    return render_template("index.html", sightings = bird_sightings)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/own_page")
        else:
            return render_template("login.html", message= "No username with that name or wrong password." )

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("register.html", message="Passwords are not the same.")
        elif len(username) == 0:
            return render_template("register.html", message="Username must be between 1 to 20 characters long.")
        elif len(password1) == 0:
            return render_template("register.html", message="Password must be between 1 to 20 characters long.")
        elif users.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", message="Username is already in use.")


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

    if request.method == "GET":    

        return render_template("management.html", moderators = moderators)
    
    if request.method == "POST":

        # Promote username to moderator
        try:
            username = request.form["promote_username"]
            result = users.promote_moderator(username)

            if result is True:
                return redirect("/management")
            else:
                return render_template("management.html", moderators = moderators, message = result)
            
        except:
            pass

        # Demote moderator
        try:
            user_id = request.form["demote_username"]
            result = users.demote_moderator(user_id)
            if result is True:
                return redirect("/management")
            else:
                return render_template("management.html", moderators = moderators, message = result)
        except:
            pass
 
    
        


@app.route("/sightings", methods=["GET", "POST"])
def show_sightings():
    if request.method == "GET":
        bird_sightings = sightings.get_sightings()
        comments = sightings.get_comments()
        return render_template("sightings.html", sightings = bird_sightings, comments = comments)
    
    if request.method == "POST":
        
        #add new comment
        try:    
            sighting_id = request.form["sighting_id"]
            comment = request.form["new_comment"]
            sightings.add_comment(sighting_id, comment)
            return redirect("/sightings")
        except:
            pass
        
        #delete comment
        try:
            comment_id = request.form["comment_id"]
            sightings.delete_comment(comment_id)
            return redirect("/sightings")
        except:
            pass
        
        #delete sighting
        try:
            sighting_id = request.form["sighting_id"]
            sightings.delete_sighting(sighting_id)
            return redirect("/sightings")
        except:
            pass
        

        

@app.route("/new_sighting", methods=["GET", "POST"])
def new_sighting():
    if request.method == "GET":
        return render_template("new_sighting.html", birdlist = birdlist )
    if request.method == "POST":

        bird_name = request.form["bird_name"]
        if not sightings.valid_bird_name(bird_name):
            return render_template("new_sighting.html", birdlist = birdlist, message="Must choose a bird.")
        
        time = request.form["time"]
        location = request.form["location"]
        additional_info = request.form["additional_info"]

        if sightings.new_sighting(bird_name, time, location, additional_info):
            return redirect("/own_page")
        else:
            return render_template("new_sighting.html", birdlist = birdlist, message="Failed to post new sighting" )


@app.route("/profile/<string:username>", methods=["GET", "POST"])
def profile(username):
    
    if username == users.get_username():
        return redirect("/own_page")

    bird_sightings = sightings.get_sightings(users.get_id_by_username(username))
    comments = sightings.get_comments()
    follower = followers.is_following(username)

    if request.method == "GET":
        return render_template("profile.html", sightings = bird_sightings, comments = comments, username = username, follower = follower)
    
    if request.method == "POST":

        # Follow / Unfollow button
        try:
            button_result = request.form["follow_btn"]
            
            # If user wants to unfollow
            if button_result == "unfollow":

                result = followers.stop_follow(username)
                
                if result:
                    return redirect("/profile/"+username)
                
                return render_template("profile.html", sightings = bird_sightings, comments = comments, username = username, follower = follower, message="Something went wrong. Please contact support.")
            
            # If user wants to follow
            result = followers.add_follow(username)

            if result:
                return redirect("/profile/"+username)
            return render_template("profile.html", sightings = bird_sightings, comments = comments, username = username, follower = follower, message="Something went wrong. Please contact support.")

        except:
            pass

        # Add comment
        try:    
            sighting_id = request.form["sighting_id"]
            comment = request.form["new_comment"]
            sightings.add_comment(sighting_id, comment)
            return redirect("/profile/"+username)
        except:
            pass

        # Delete comment
        try:
            comment_id = request.form["comment_id"]
            sightings.delete_comment(comment_id)
            return redirect("/profile/"+username)
        except:
            pass

        # Delete sighting
        try:
            sighting_id = request.form["sighting_id"]
            sightings.delete_sighting(sighting_id)
            return redirect("/profile/"+username)
        except:
            pass


@app.route("/own_page", methods=["GET", "POST"])
def own_page():
    
    bird_sightings = sightings.get_sightings(users.user_id())
    comments = sightings.get_comments()
    followslist = followers.get_followslist()
    followerlist = followers.get_followerlist()

    if request.method == "GET":
        return render_template("own_page.html", sightings = bird_sightings, follows = followslist, followers = followerlist, comments = comments)
    
    if request.method == "POST":
        
        #follow new user
        try:
            follow_username = request.form["follow_username"]
            result = followers.add_follow(follow_username)

            if result is True:
                return redirect("/own_page")
            else:
                return render_template("own_page.html", sightings = bird_sightings, follows = followslist, followers = followerlist, comments = comments, message = result)
        except:
            pass
        
        #add new comment
        try:    
            sighting_id = request.form["sighting_id"]
            comment = request.form["new_comment"]
            sightings.add_comment(sighting_id, comment)
            return redirect("/own_page")
        except:
            pass
        
        #delete comment
        try:
            comment_id = request.form["comment_id"]
            sightings.delete_comment(comment_id)
            return redirect("/own_page")
        except:
            pass
        
        #delete sighting
        try:
            sighting_id = request.form["sighting_id"]
            sightings.delete_sighting(sighting_id)
            return redirect("/own_page")
        except:
            pass









    
    