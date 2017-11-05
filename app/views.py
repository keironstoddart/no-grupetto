# flask
from flask import render_template, flash, redirect, session, url_for, request, g, Response
from flask_login import login_user, logout_user, current_user, login_required
# forms
from .forms import LoginForm
from .forms import SignupForm
# models
from .models import Athlete
from .models import Activity
# Strava
from stravalib.client import Client
from stravalib import unithelper
# Pandas
import pandas as pd
# utilities
from .utils import query_to_pandas, statistics
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
    if form.validate_on_submit():
        name = form.name.data
        athlete = Athlete.query.filter_by(name=name).first()
        if athlete != None:
            flash('Username already exists.',category='alert alert-warning')
            return redirect(url_for('signup'))
        else:
            athlete = Athlete(
                        name=name,
                        password=form.password.data,
                        token=session['token']
                        )
            db.session.add(athlete)
            db.session.commit()
            login_user(athlete, remember = form.remember_me.data)
            return redirect(url_for('dashboard'))

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

@app.route('/push_data/<structure>/<how>')
@login_required
def push_data(structure='csv',how='view'):
    activities = Activity.query.filter_by(athlete_id=current_user.id)
    activities = query_to_pandas(activities)
    if structure == 'csv':
        data = activities.to_csv()
        filename = 'data.csv'
    else:
        data = activities.to_json(orient='index')
        filename = 'data.json'
    if how == 'view':
        return data
    else:
        return Response(
        data,
        mimetype="text/" + structure,
        headers={"Content-disposition":
                 "attachment; filename=" + filename})

@app.route('/data')
@login_required
def data():
    return render_template('data.html')

def data_pull():
    client = Client()
    client.access_token = current_user.token
    activities = client.get_activities()
    for act in activities:
        # check to see if activity is already written to local database
        activity = Activity.query.filter_by(strava_id=act.id).first()
        if activity == None:
            act = client.get_activity(act.id)
            # if not write to database
            activity = Activity(
                athlete_id = current_user.id,
                bpm = act.average_heartrate,
                strava_id = act.id,
                distance = unithelper.miles(act.distance).get_num(),
                elevation = unithelper.feet(act.total_elevation_gain).get_num(),
                calories = act.calories,
                speed = unithelper.miles_per_hour(act.average_speed).get_num(),
                max_speed = unithelper.miles_per_hour(act.max_speed).get_num(),
                city = act.location_city,
                state = act.location_state,
                date = act.start_date_local,
                act_type = act.type,
                name = act.name,
                time = act.moving_time
            )
            db.session.add(activity)
            db.session.commit()

@app.route('/dashboard')
@login_required
def dashboard():
    # grab activities and convert to dataframe
    activities = Activity.query.filter_by(athlete_id=current_user.id)
    activities = query_to_pandas(activities)
    career = statistics(activities)

    return render_template('dashboard.html', career=career)

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
        # todo: check to see if token already exists in back end
        # if it does take to the log in page and include message
        # that account is already authorized.
        athlete = Athlete.query.filter_by(token=access_token).first()
        if athlete != None:
            flash('Athlete already authorized. Please log in.',category='alert alert-success')
            return redirect(url_for('login'))

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
