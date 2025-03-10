from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, app
from models import User, Announcement
from forms import LoginForm, RegistrationForm, AnnouncementForm, ContactForm
import logging

logger = logging.getLogger(__name__)

# Create blueprints with URL prefixes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
main_bp = Blueprint('main', __name__)  # No prefix for main as it contains root routes
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

def register_blueprints(app):
    logger.info("Registering blueprints...")
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    logger.info("Blueprints registered successfully")

# Diagnostic route
@main_bp.route('/ping')
def ping():
    logger.info("Ping endpoint hit")
    return "pong"

# Main routes
@main_bp.route('/')
def home():
    logger.info("Home route accessed")
    try:
        announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(3).all()
        logger.info(f"Retrieved {len(announcements)} announcements")
        return render_template('home.html', announcements=announcements)
    except Exception as e:
        logger.error(f"Error in home route: {str(e)}")
        return "An error occurred", 500

@main_bp.route('/about')
def about():
    logger.info("About route accessed")
    return render_template('about.html')

@main_bp.route('/academics')
def academics():
    logger.info("Academics route accessed")
    return render_template('academics.html')

@main_bp.route('/admissions')
def admissions():
    logger.info("Admissions route accessed")
    return render_template('admissions.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    logger.info("Contact route accessed")
    form = ContactForm()
    if form.validate_on_submit():
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form)

@main_bp.route('/news')
def news():
    logger.info("News route accessed")
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('news.html', announcements=announcements)

# Dashboard routes
@dashboard_bp.route('/')
@login_required
def index():
    logger.info(f"Dashboard route accessed by user: {current_user.username}")
    if current_user.role == 'admin':
        return render_template('dashboard/admin.html')
    elif current_user.role == 'teacher':
        return render_template('dashboard/teacher.html')
    else:
        return render_template('dashboard/student.html')

@dashboard_bp.route('/announcements/new', methods=['GET', 'POST'])
@login_required
def new_announcement():
    logger.info(f"New announcement route accessed by user: {current_user.username}")
    if current_user.role not in ['admin', 'teacher']:
        flash('You do not have permission to create announcements.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            author_id=current_user.id
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement created successfully!', 'success')
        return redirect(url_for('main.news'))
    return render_template('dashboard/new_announcement.html', form=form)


# Auth routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    logger.info("Login route accessed")
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('dashboard.index'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    logger.info("Register route accessed")
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logger.info(f"Logout route accessed by user: {current_user.username}")
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))