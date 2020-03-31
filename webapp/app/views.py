# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging

# Flask modules
from flask import (
    render_template,
    render_template_string,
    make_response,
    request,
    url_for,
    redirect,
    send_from_directory,
    flash,
    jsonify,
)
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app import app, lm, db, bc
from app.models import User, Robot
from app.forms import LoginForm, RegisterForm, AzureCredentials, AddRobot
from app.scripts import DAMRWEB

bot_id = None

# Provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Logout user
@app.route("/logout.html")
def logout():
    """ Logout user """
    logout_user()
    return redirect(url_for("index"))


# Reset Password - Not
@app.route("/reset.html")
def reset():
    """ Not implemented """
    return render_template(
        "layouts/auth-default.html", content=render_template("pages/reset.html")
    )


# Register a new user
@app.route("/register.html", methods=["GET", "POST"])
def register():
    """ Create a new user """

    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == "GET":

        return render_template(
            "layouts/auth-default.html",
            content=render_template("pages/register.html", form=form, msg=msg),
        )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get("username", "", type=str)
        password = request.form.get("password", "", type=str)
        email = request.form.get("email", "", type=str)

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = "Error: User exists!"

        else:
            pw_hash = password  # bc.generate_password_hash(password)
            user = User(username, email, pw_hash)
            user.save()
            msg = 'User created, please <a href="' + url_for("login") + '">login</a>'

    else:
        msg = "Input error"

    return render_template(
        "layouts/auth-default.html",
        content=render_template("pages/register.html", form=form, msg=msg),
    )


# Authenticate user
@app.route("/login.html", methods=["GET", "POST"])
def login():

    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get("username", "", type=str)
        password = request.form.get("password", "", type=str)

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:

            # if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for("index"))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user - Please register."

    return render_template(
        "layouts/auth-default.html",
        content=render_template("pages/login.html", form=form, msg=msg),
    )


# App main route + generic routing
@app.route("/", defaults={"path": "index.html"}, methods=["GET", "POST"])
@app.route("/<path>", methods=["GET", "POST"])
def index(path):

    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    # Declare the credentials form
    form = AzureCredentials(request.form)
    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if request.method == "POST" and form.validate():
        namespace = form.namespace.data
        sasName = form.sasName.data
        sasValue = form.sasValue.data

        # create object of DAMRWEB
        damrweb = DAMRWEB(namespace, sasName, sasValue)
        if damrweb:
            return redirect(url_for("robots"))
        else:
            flash(
                "Unable to create a DAMRWEB object, possibly invalid credentials.",
                "error",
            )
    content = None
    try:

        # try to match the pages defined in -> pages/<input file>
        return render_template(
            "layouts/default.html",
            content=render_template("pages/" + path, form=form, msg=msg),
        )
    except:

        return render_template(
            "layouts/auth-default.html", content=render_template("pages/error-404.html")
        )


# Manage the robots
@app.route("/robots", methods=["GET", "POST"])
def robots():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    form = AddRobot(request.form)
    robots = Robot.query.all()
    if request.method == "POST" and form.validate():
        ipAddress = form.ipAddress.data
        robot = Robot.query.filter_by(ipAddress=ipAddress).first()
        if robot:
            flash("Error: IP Address assigned to existing robot")
        else:
            robot = Robot(ipAddress=ipAddress)
            robot.save()
            flash("Robot Added")
    return render_template(
        "layouts/default.html",
        content=render_template("pages/robots.html", form=form, robots=robots),
    )


# Move the robots
@app.route("/robot_move/<ipAddress>", methods=["GET"])
def robot_move(ipAddress):
    global bot_id
    bot_id = ipAddress
    data = dict()
    template_name = "pages/robot-move.html"
    data["popup"] = render_template(template_name, ipAddress=ipAddress)
    return jsonify(data)


@app.route("/robot_keys", methods=["GET", "POST"])
def robot_keys():
    print(list(request.form.items()))
    data = dict()
    template_name = "pages/robot-move.html"
    data["popup"] = render_template(template_name)
    return jsonify(data)


# Return sitemap
@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(os.path.join(app.root_path, "static"), "sitemap.xml")
