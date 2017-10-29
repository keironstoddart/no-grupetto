# flask
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
# forms
from .forms import LoginForm
from .forms import SignupForm
# models
from .models import Athlete
# Strava
from stravalib.client import Client
from app import app, db, lm

MY_STRAVA_CLIENT_ID = 7626
MY_STRAVA_CLIENT_SECRET = '4b2e2887eb145e7e3bbeeaada7ee415ad19b9c92'

# this is run before every request
@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_athlete(id):
    return Athlete.query.get(int(id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # check to see if user is already logged in
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        # check to see if user exists
        # on sign up page make sure users cannot sign up with same user name
        athlete = Athlete.query.filter_by(name=name).first()
        if athlete is None:
            flash('Athlete does not exist, please join now.',category='alert alert-warning')
            return redirect(url_for('login'))
        else:
            # check to see if passwords match
            if athlete.password == form.password.data:
                login_user(athlete, remember = form.remember_me.data)
                return redirect(url_for('dashboard'))
            else:
                flash(u'Incorrect password, please try again.',category='alert alert-danger')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/')
@app.route('/index')
def index():
    code = request.args.get('code')
    state = request.args.get('state')
    if code:
        client = Client()
        access_token = client.exchange_code_for_token(
            client_id=MY_STRAVA_CLIENT_ID,
            client_secret=MY_STRAVA_CLIENT_SECRET,
            code=code
            )
        print('access token:',access_token)
        # store token in session variable for database write on sign up page
        session['token'] = access_token
        athlete = client.get_athlete()
        # bring them to the login page for account creation
        return redirect(url_for('signup'))
    return render_template('index.html')

@app.route('/connect')
def connect():
    client = Client()
    url = client.authorization_url(client_id=7626,
                                    redirect_uri='http://127.0.0.1:5000/authorization')
    print(url)
    access_token = 'd203124dc2d8cb71f9a7513329617e50fcc3f418'
    client.access_token = access_token
    athlete = client.get_athlete()
    print("For {id}, I now have an access token {token}".format(id=athlete.id, token=access_token))
    return str(athlete.weight)


@app.route('/authorization')
def authorization():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        strava = 'https://www.strava.com/oauth/authorize?client_id=7626&response_type=code&redirect_uri=http://127.0.0.1:5000&approval_prompt=force'
        return redirect(strava)
