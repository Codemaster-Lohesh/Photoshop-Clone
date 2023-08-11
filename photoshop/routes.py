import os
import secrets
from PIL import Image, ImageFilter
from flask import render_template, url_for, flash, redirect, request, abort, send_file
from photoshop import app, db, bcrypt
from photoshop.forms import RegistrationForm, LoginForm, ResizeForm, BlurForm, FilterForm, MonoForm
from photoshop.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccesful, Please check username and password','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def getImagePath(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)

    return picture_path

def resizeImage(form_picture,resizeWidth,resizeHeight):
    picture_path = getImagePath(form_picture)

    output_size = (resizeWidth, resizeHeight)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_path

@app.route('/resize', methods=['GET', 'POST'])
@login_required
def resize():
    form = ResizeForm()
    if form.validate_on_submit:
        if form.picture.data:
            resizedPicture=resizeImage(form.picture.data,form.resizeWidth.data,form.resizeHeight.data)
            return send_file(resizedPicture, as_attachment=True)
    return render_template('resize.html',form=form)

def blurImage(form_picture,radius):
    picture_path = getImagePath(form_picture)

    i = Image.open(form_picture)
    i.filter(ImageFilter.GaussianBlur(radius)).save(picture_path)

    return picture_path


@app.route('/blur', methods=['GET', 'POST'])
@login_required
def blur():
    form = BlurForm()
    if form.validate_on_submit:
        if form.picture.data:
            blurredPicture=blurImage(form.picture.data,form.radius.data)
            return send_file(blurredPicture, as_attachment=True)
    return render_template('blur.html',form=form)

def filterImage(form_picture,filter):
    picture_path = getImagePath(form_picture)

    i = Image.open(form_picture)
    i.filter(eval('ImageFilter.'+filter)).save(picture_path)

    return picture_path
    
@app.route('/filter', methods=['GET', 'POST'])
@login_required
def filter():
    form = FilterForm()
    if form.validate_on_submit:
        if form.picture.data:
            filteredPicture=filterImage(form.picture.data,form.filter.data)
            return send_file(filteredPicture, as_attachment=True)
    return render_template('filter.html',form=form)

def monoImage(form_picture):
    picture_path = getImagePath(form_picture)

    i = Image.open(form_picture)
    i.convert(mode='L').save(picture_path)

    return picture_path

@app.route('/monochromatic', methods=['GET', 'POST'])
@login_required
def monochromatic():
    form=MonoForm()
    if form.validate_on_submit:
        if form.picture.data:
            monoPicture = monoImage(form.picture.data)
            return send_file(monoPicture, as_attachment=True)
    return render_template('mono.html',form=form)