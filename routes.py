from app import app
from flask import render_template, request, redirect
import users, sightings
import csv

with open('static/birdnames.csv', mode='r') as csvfile:
    birdlist = [bird[0] for bird in csv.reader(csvfile)]


@app.route("/", methods=["GET"])
def index():
    bird_sightings = sightings.get_list()
    return render_template("index.html", sightings = bird_sightings)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", message= "No username with that name or wrong password." )


@app.route("/sightings", methods=["GET", "POST"])
def show_sightings():
    if request.method == "GET":
        bird_sightings = sightings.get_list()
        comments = sightings.get_comments()
        return render_template("sightings.html", sightings = bird_sightings, comments = comments)
    if request.method == "POST":
        sighting_id = request.form["sighting_id"]
        comment = request.form["new_comment"]
        sightings.add_comment(sighting_id, comment)
        return redirect("/sightings")


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
            return redirect("/sightings")
        else:
            return render_template("new_sighting.html", birdlist = birdlist, message="Failed to post new sighting" )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    bird_sightings = sightings.get_list(users.user_id())
    friendlist = users.get_friendlist()

    if request.method == "GET":
        return render_template("profile.html", sightings = bird_sightings, friends = friendlist)
    
    if request.method == "POST":
        friend_username = request.form["friend_username"]
        result = users.add_friend(friend_username)
        if result is True:
            return redirect("/profile")
        else:
            return render_template("profile.html", sightings = bird_sightings, friends = friendlist, message = result)

    
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