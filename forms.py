from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField, BooleanField, FileField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, URL, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent')
    ])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Register')

class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post Announcement')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

# New forms for CMS
class BannerForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    image = FileField('Banner Image', validators=[DataRequired()])
    link_url = StringField('Link URL', validators=[Optional(), URL()])
    is_active = BooleanField('Active')
    order = IntegerField('Display Order', default=0)
    submit = SubmitField('Save Banner')

class DocumentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    document_type = SelectField('Document Type', choices=[
        ('certificate', 'Certificate'),
        ('form', 'Form'),
        ('notice', 'Notice'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    document = FileField('Document File', validators=[DataRequired()])
    is_public = BooleanField('Public Access', default=True)
    submit = SubmitField('Upload Document')

class MediaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    media_type = SelectField('Media Type', choices=[
        ('photo', 'Photo'),
        ('video', 'Video')
    ], validators=[DataRequired()])
    media_file = FileField('Media File', validators=[DataRequired()])
    thumbnail = FileField('Thumbnail (for videos)')
    gallery_category = SelectField('Gallery Category', choices=[
        ('events', 'Events'),
        ('campus', 'Campus'),
        ('activities', 'Activities'),
        ('other', 'Other')
    ])
    is_featured = BooleanField('Featured')
    submit = SubmitField('Upload Media')

class ContentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    page_key = StringField('Page Identifier', validators=[DataRequired()])
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save Content')