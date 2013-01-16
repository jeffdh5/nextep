from flask import render_template, request, flash, redirect, g, session, url_for
from app import app, oid, lm, db
from models import User, Show, Day, ROLE_USER, ROLE_ADMIN
from flask.ext.login import login_user, logout_user, current_user, login_required
from scraper import prev_and_next_ep, synopsis, picture

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")
    
@app.route('/logged_in', methods = ['GET', 'POST'])
def logged_in():
	return render_template("logged_in.html")

@app.route('/user/<nickname>', methods = ['GET', 'POST'])
@login_required
def user(nickname):
	if request.method == 'GET':
		user = User.query.filter_by(nickname = nickname).first()
		week = Day.query.all()
		return render_template('profile.html', user=user, week=week)
	
	if request.method == 'POST':
		user = User.query.filter_by(nickname = nickname).first()
		week = Day.query.all()
		if request.form.get('show', None) != None:
			show_input = request.form.get('show', None)
			day_input = request.form.get('day', None)
			day = Day.query.filter_by(name=day_input).first()
			info = Show.query.filter_by(name=show_input).first()
			next_and_prev = prev_and_next_ep(info.tv_rage_link)
			next = next_and_prev[0]
			prev = next_and_prev[1]
			synop = synopsis(info.tv_rage_link)
			pic = picture(info.tv_link)
			return render_template('profile.html', user=user, day=day, shows=day.shows, week=week, info=info, name=info.name, next=next, prev=prev, synopsis=synop, picture=pic)
		elif request.form.get('day', None) != None:
			day_input = request.form.get('day', None)
			day = Day.query.filter_by(name=day_input).first()
			return render_template('profile.html', user=user, day=day, shows=day.shows, week=week)
"""	if request.method == 'POST':
		user = User.query.filter_by(nickname = nickname).first()
		day_input = request.form['day']
		show_input = request.form['show']
		day = Day.query.filter_by(name=day_input).first()
		week = Day.query.all()
		if show_input == '':
			return render_template('profile.html', user=user, shows=day.shows, week=week)
		else:
			info = Show.query.filter_by(name=show_input).first()
			next_and_prev = prev_and_next_ep(info.tv_link)
			next = next_and_prev[0]
			prev = next_and_prev[1]
			synopsis = synopsis(info.tv_link)
			picture = picture(info.tv_rage_link)
			return render_template('profile.html', user=user, show=day.shows, week=week, name=info.name, next=next, prev=prev, synopsis=synopsis, picture=picture)
"""

@app.route('/add_shows', methods = ['GET', 'POST'])
def edit_shows():
	return render_template("add_shows.html")

@app.route('/add_shows_admin', methods = ['GET', 'POST'])
def add_shows_admin():
	if request.method == 'GET':
		return render_template("add_shows_admin.html")
	elif request.method == 'POST':
		if request.form["Name"] == '':
			return render_template("add_shows_admin.html", error='No Name!')
		if request.form["Day"] == '':
			return render_template("add_shows_admin.html", error='No Day!')
		if request.form["TV.com"] == '':
			return render_template("add_shows_admin.html", error='No TV.com Link!')
		if request.form["TVRage.com"] == '':
			return render_template("add_shows_admin.html", error='No TVRage.com Link!')
		show = Show(name=request.form["Name"], day=request.form["Day"], tv_link=request.form["TV.com"], tv_rage_link=request.form["TVRage.com"])
		db.session.add(show)
		db.session.commit()
		return redirect(url_for('show_added_admin'))
		
@app.route('/show_added_admin', methods = ['GET', 'POST'])
def show_added_admin():
	return render_template("show_added_admin.html")

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