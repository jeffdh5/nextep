from flask import render_template, request, flash, redirect, g, session, url_for
from app import app, oid, lm, db
from models import User, ROLE_USER, ROLE_ADMIN
from flask.ext.login import login_user, logout_user, current_user, login_required
from scraper import prev_and_next_ep, synopsis, picture

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
    
    
@app.route('/logged_in', methods = ['GET', 'POST'])
def logged_in():
	return render_template("logged_in.html")

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
	return render_template("profile.html", episodes=prev_and_next_ep('http://www.tvrage.com/The_Office', 'str'), synopsis=synopsis('http://www.tvrage.com/The_Office'), picture = picture('http://www.tv.com/shows/the-office/'))

@app.route('/edit_shows', methods = ['GET', 'POST'])
def edit_shows():
	return render_template("edit_shows.html")

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    if request.method == 'POST':
        return oid.try_login('https://www.google.com/accounts/o8/id', ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In')

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False

    login_user(user, remember = remember_me)
    return redirect(url_for('logged_in'))
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
    
@app.before_request
def before_request():
    g.user = current_user