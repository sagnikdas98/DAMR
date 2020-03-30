# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging 

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app         import app, lm, db, bc
from app.models  import User
from app.forms   import LoginForm, RegisterForm, AzureCredentials
from app.scripts import DAMRWEB

# Provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout.html')
def logout():
    ''' Logout user '''
    logout_user()
    return redirect(url_for('index'))

# Reset Password - Not 
@app.route('/reset.html')
def reset():
    ''' Not implemented ''' 
    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/reset.html') )

# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    ''' Create a new user '''

    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/register.html', form=form, msg=msg ) )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/register.html', form=form, msg=msg ) )

# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user - Please register." 

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/login.html', form=form, msg=msg ) )

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'}, methods=['GET', 'POST'])
@app.route('/<path>', methods=['GET', 'POST'])
def index(path):

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    # Declare the credentials form
    form = AzureCredentials(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        namespace  = request.form.get('namespace' , '', type=str)
        sasName    = request.form.get('sasName'   , '', type=str)
        sasValue   = request.form.get('sasValue'  , '', type=str)

        # create object of DAMRWEB 
        damrweb = DAMRWEB(namespace, sasName, sasValue)
        print(damrweb)
        if damrweb:
            return redirect(url_for('robots'))
        else:
            msg = "Unable to create a DAMRWEB object, possibly invalid credentials."
    else:
        msg = "Invalid Input"
    content = None
    try:

        # try to match the pages defined in -> pages/<input file>
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path, form=form, msg=msg) )
    except:
        
        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/error-404.html' ) )

@app.route('/robots')
def robots():
    return render_template('layouts/default.html', content=render_template('pages/robots.html'))

# Return sitemap 
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')
