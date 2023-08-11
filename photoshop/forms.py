from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField,  BooleanField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from photoshop.models import User

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email= StringField('Email',validators=[DataRequired(), Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username')
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different email')

class LoginForm(FlaskForm):
    email= StringField('Email',validators=[DataRequired(), Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    remember= BooleanField('Remember me')
    submit= SubmitField('Login')

class ResizeForm(FlaskForm):
    picture= FileField('Profile picture',validators=[FileAllowed(['jpg','png'])])
    resizeWidth = IntegerField('Resize Width',validators=[DataRequired()])
    resizeHeight = IntegerField('Resize Height',validators=[DataRequired()])
    submit= SubmitField('Upload')

class BlurForm(FlaskForm):
    picture= FileField('Profile picture',validators=[FileAllowed(['jpg','png'])])
    radius= IntegerField('Gaussian Blur Radius',validators=[DataRequired()])
    submit= SubmitField('Upload')

class FilterForm(FlaskForm):
    picture= FileField('Profile picture',validators=[FileAllowed(['jpg','png'])])
    filter= RadioField('Choose a Filter',choices=[
        ('BLUR','BLUR'), ('CONTOUR','CONTOUR') ,('DETAIL','DETAIL') ,('EDGE_ENHANCE','EDGE_ENHANCE') ,('EDGE_ENHANCE_MORE','EDGE_ENHANCE_MORE'),
        ('EMBOSS','EMBOSS'), ('FIND_EDGES','FIND_EDGES') ,('SMOOTH','SMOOTH') ,('SMOOTH_MORE','SMOOTH_MORE'), ('SHARPEN','SHARPEN')
    ],validators=[DataRequired()])
    submit= SubmitField('Upload')

class MonoForm(FlaskForm):
    picture= FileField('Profile picture',validators=[FileAllowed(['jpg','png'])])
    submit= SubmitField('Upload')

    