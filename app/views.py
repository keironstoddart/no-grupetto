# flask
from flask import render_template, flash, redirect
from flask import request
# logins
from .forms import LoginForm
# Strava
from stravalib.client import Client
from app import app

MY_STRAVA_CLIENT_ID = 7626
MY_STRAVA_CLIENT_SECRET = '4b2e2887eb145e7e3bbeeaada7ee415ad19b9c92'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Name:',form.name.data)
        print('Password:',form.password.data)
        print('Remember Me:',form.remember_me.data)
        return redirect('/dashboard')
    return render_template(
                'login.html',
                title='Sign In',
                form=form
                )

@app.route('/dashboard')
def dashboard():
    return 'dashboard'

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
        athlete = client.get_athlete()
        # bring them to the login page for account creation
        return redirect('/login')
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
    return 'success'
