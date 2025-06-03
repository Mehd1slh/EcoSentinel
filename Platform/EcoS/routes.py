from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from flask import render_template, redirect, url_for, flash, send_file, request, session, jsonify , json
from EcoS.forms import LoginForm, MapForm, UpdateAccountForm
from EcoS.entities import User
from EcoS import app, db, bcrypt , get_locale
from flask_login import login_user, logout_user, login_required, current_user
from PIL import Image
import secrets, os, smtplib , uuid
from flask_babel import Babel, _,lazy_gettext 
from dotenv import load_dotenv


executor = ThreadPoolExecutor()
load_dotenv('variables.env')



@app.route('/setlang')
def setlang():
    lang = request.args.get('lang', 'en')
    session['lang'] = lang
    return redirect(request.referrer)

@app.context_processor
def inject_babel():
    return dict(_=lazy_gettext)

@app.context_processor
def inject_locale():
    # This makes the function available directly, allowing you to call it in the template
    return {'get_locale': get_locale}


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():

            # # store in session
            # session['full_address'] = address_info['address']
            # session['city'] = address_info['city']
            # session['region'] = address_info['region']
            # session['country'] = address_info['country']
            # session['weather_data']=weather_data
            # session['weather_summary'] = weather_summary
            # session['soil_data']=soil_data
            # session['soil_summary'] = soil_summar

    return render_template('home.html', current_locale=get_locale())


@app.route("/users")
@login_required
def users():
    if current_user.is_authenticated:
        if current_user.privilege == 'admin':
            users = User.query.filter_by(privilege="user").all()
            return render_template('users.html', title=_('Users'), users=users, current_locale=session.get('lang'))
        else:
            flash(_("You Don't have the admin privilege"), 'warning')
            return redirect(url_for('home'))
        
@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.is_authenticated:
        if current_user.privilege == 'admin':
            users = User.query.filter_by(privilege="user").all()
            return render_template('users.html', title=_('Users'), users=users, current_locale=session.get('lang'))
        else:
            flash(_("You Don't have the admin privilege"), 'warning')
            return redirect(url_for('home'))
        
@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    
    if user:
        db.session.delete(user)
        db.session.commit()
        flash(_('User has been deleted successfully'), 'success')
    else:
        flash(_('User not found'), 'danger')
    
    return redirect(url_for('users'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.mdp, form.mdp.data):
            flash(_("Welcome Back %(username)s!", username=user.username), 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(_('Login Unsuccessful, please check your email and password'), 'danger')
    return render_template('login.html', title=_('Login'), form=form, current_locale=session.get('lang'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # Delete previous picture if it exists
    if current_user.img:
        prev_picture_path = os.path.join(app.root_path, 'static/profile_pics', current_user.img)
        if os.path.exists(prev_picture_path):
            os.remove(prev_picture_path)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(_('Your account has been updated!'), 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for('static', filename='profile_pics/' + current_user.img)
    return render_template('account.html', title=_('Account'), img_file=img_file, form=form, current_locale=session.get('lang'))
