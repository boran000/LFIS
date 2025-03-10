from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from app import db, app
from models import User, Announcement, Banner, Document, Media, Content, Assignment, Attendance, StudentProgress, TransferCertificate
from forms import (LoginForm, RegistrationForm, AnnouncementForm, ContactForm,
                  BannerForm, DocumentForm, MediaForm, ContentForm, AssignmentForm, AttendanceForm, StudentProgressForm, SubmitAssignmentForm, TCRequestForm)
import logging
from datetime import datetime

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
        banners = Banner.query.filter_by(is_active=True).order_by(Banner.order.asc()).all()
        logger.info(f"Retrieved {len(announcements)} announcements and {len(banners)} banners")
        return render_template('home.html', announcements=announcements, banners=banners)
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


# CMS Management Routes
@dashboard_bp.route('/banners/new', methods=['GET', 'POST'])
@login_required
def new_banner():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = BannerForm()
    if form.validate_on_submit():
        try:
            # Handle file upload
            image = form.image.data
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'banners', filename)
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)

            banner = Banner(
                title=form.title.data,
                description=form.description.data,
                image_url=f'/uploads/banners/{filename}',
                link_url=form.link_url.data,
                is_active=form.is_active.data,
                order=form.order.data
            )
            db.session.add(banner)
            db.session.commit()
            flash('Banner added successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error creating banner: {str(e)}")
            flash('Error creating banner. Please try again.', 'danger')

    return render_template('dashboard/banner_form.html', form=form, title='New Banner')

@dashboard_bp.route('/documents/new', methods=['GET', 'POST'])
@login_required
def new_document():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = DocumentForm()
    if form.validate_on_submit():
        try:
            # Handle file upload
            doc_file = form.document.data
            filename = secure_filename(doc_file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'documents', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            doc_file.save(file_path)

            document = Document(
                title=form.title.data,
                description=form.description.data,
                document_type=form.document_type.data,
                file_url=f'/uploads/documents/{filename}',
                is_public=form.is_public.data
            )
            db.session.add(document)
            db.session.commit()
            flash('Document uploaded successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error uploading document: {str(e)}")
            flash('Error uploading document. Please try again.', 'danger')

    return render_template('dashboard/document_form.html', form=form, title='Upload Document')

@dashboard_bp.route('/media/new', methods=['GET', 'POST'])
@login_required
def new_media():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = MediaForm()
    if form.validate_on_submit():
        try:
            # Handle media file upload
            media_file = form.media_file.data
            filename = secure_filename(media_file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'media', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            media_file.save(file_path)

            # Handle thumbnail if provided (for videos)
            thumbnail_url = None
            if form.thumbnail.data:
                thumb_file = form.thumbnail.data
                thumb_filename = secure_filename(thumb_file.filename)
                thumb_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'thumbnails', thumb_filename)
                os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
                thumb_file.save(thumb_path)
                thumbnail_url = f'/uploads/thumbnails/{thumb_filename}'

            media = Media(
                title=form.title.data,
                description=form.description.data,
                media_type=form.media_type.data,
                file_url=f'/uploads/media/{filename}',
                thumbnail_url=thumbnail_url,
                gallery_category=form.gallery_category.data,
                is_featured=form.is_featured.data
            )
            db.session.add(media)
            db.session.commit()
            flash('Media uploaded successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error uploading media: {str(e)}")
            flash('Error uploading media. Please try again.', 'danger')

    return render_template('dashboard/media_form.html', form=form, title='Upload Media')

@dashboard_bp.route('/content/new', methods=['GET', 'POST'])
@login_required
def new_content():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = ContentForm()
    if form.validate_on_submit():
        try:
            content = Content(
                title=form.title.data,
                content=form.content.data,
                page_key=form.page_key.data,
                is_published=form.is_published.data
            )
            db.session.add(content)
            db.session.commit()
            flash('Content page created successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error creating content: {str(e)}")
            flash('Error creating content. Please try again.', 'danger')

    return render_template('dashboard/content_form.html', form=form, title='New Content Page')

# Edit routes for CMS content
@dashboard_bp.route('/banners/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_banner(id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('dashboard.index'))

    banner = Banner.query.get_or_404(id)
    form = BannerForm(obj=banner)

    if form.validate_on_submit():
        try:
            banner.title = form.title.data
            banner.description = form.description.data
            banner.link_url = form.link_url.data
            banner.is_active = form.is_active.data
            banner.order = form.order.data

            if form.image.data:
                image = form.image.data
                filename = secure_filename(image.filename)
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'banners', filename)
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                image.save(image_path)
                banner.image_url = f'/uploads/banners/{filename}'

            db.session.commit()
            flash('Banner updated successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error updating banner: {str(e)}")
            flash('Error updating banner. Please try again.', 'danger')

    return render_template('dashboard/banner_form.html', form=form, title='Edit Banner', banner=banner)

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

# Teacher specific routes
@dashboard_bp.route('/assignments/new', methods=['GET', 'POST'])
@login_required
def new_assignment():
    if current_user.role != 'teacher':
        flash('Access denied. Teacher privileges required.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = AssignmentForm()
    if form.validate_on_submit():
        try:
            # Handle file upload if present
            file_url = None
            if form.file.data:
                file = form.file.data
                filename = secure_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'assignments', filename)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file.save(file_path)
                file_url = f'/uploads/assignments/{filename}'

            assignment = Assignment(
                title=form.title.data,
                description=form.description.data,
                due_date=form.due_date.data,
                file_url=file_url,
                teacher_id=current_user.id
            )
            db.session.add(assignment)
            db.session.commit()
            flash('Assignment created successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error creating assignment: {str(e)}")
            flash('Error creating assignment. Please try again.', 'danger')

    return render_template('dashboard/assignment_form.html', form=form, title='New Assignment')

@dashboard_bp.route('/attendance/take', methods=['GET', 'POST'])
@login_required
def take_attendance():
    if current_user.role != 'teacher':
        flash('Access denied. Teacher privileges required.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = AttendanceForm()
    if form.validate_on_submit():
        try:
            # Get all students
            students = User.query.filter_by(role='student').all()
            for student in students:
                attendance = Attendance(
                    student_id=student.id,
                    date=form.date.data,
                    status=request.form.get(f'status_{student.id}', 'absent'),
                    marked_by=current_user.id
                )
                db.session.add(attendance)
            db.session.commit()
            flash('Attendance marked successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error marking attendance: {str(e)}")
            flash('Error marking attendance. Please try again.', 'danger')

    students = User.query.filter_by(role='student').all()
    return render_template('dashboard/attendance_form.html', form=form, students=students, title='Take Attendance')

@dashboard_bp.route('/progress/record', methods=['GET', 'POST'])
@login_required
def student_progress():
    if current_user.role != 'teacher':
        flash('Access denied. Teacher privileges required.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = StudentProgressForm()
    if form.validate_on_submit():
        try:
            progress = StudentProgress(
                student_id=request.form.get('student_id'),
                subject=form.subject.data,
                grade=form.grade.data,
                remarks=form.remarks.data,
                term=form.term.data,
                academic_year=form.academic_year.data
            )
            db.session.add(progress)
            db.session.commit()
            flash('Progress recorded successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error recording progress: {str(e)}")
            flash('Error recording progress. Please try again.', 'danger')

    students = User.query.filter_by(role='student').all()
    return render_template('dashboard/progress_form.html', form=form, students=students, title='Record Progress')

# Student specific routes
@dashboard_bp.route('/assignments/submit/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def submit_assignment(assignment_id):
    if current_user.role != 'student':
        flash('Access denied. Student privileges required.', 'danger')
        return redirect(url_for('dashboard.index'))

    assignment = Assignment.query.get_or_404(assignment_id)
    form = SubmitAssignmentForm()

    if form.validate_on_submit():
        try:
            file = form.file.data
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'submissions', filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)

            assignment.status = 'submitted'
            assignment.file_url = f'/uploads/submissions/{filename}'
            db.session.commit()
            flash('Assignment submitted successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error submitting assignment: {str(e)}")
            flash('Error submitting assignment. Please try again.', 'danger')

    return render_template('dashboard/submit_assignment.html', form=form, assignment=assignment)

@dashboard_bp.route('/tc/request', methods=['GET', 'POST'])
@login_required
def request_tc():
    if current_user.role != 'student':
        flash('Access denied. Student privileges required.', 'danger')
        return redirect(url_for('dashboard.index'))

    form = TCRequestForm()
    if form.validate_on_submit():
        try:
            tc = TransferCertificate(
                student_id=current_user.id,
                reason=form.reason.data,
                tc_number=f'TC{current_user.id}-{datetime.utcnow().strftime("%Y%m%d%H%M")}'
            )
            db.session.add(tc)
            db.session.commit()
            flash('Transfer Certificate request submitted successfully!', 'success')
            return redirect(url_for('dashboard.index'))
        except Exception as e:
            logger.error(f"Error requesting TC: {str(e)}")
            flash('Error requesting TC. Please try again.', 'danger')

    return render_template('dashboard/tc_request.html', form=form)