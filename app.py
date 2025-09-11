from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='../frontend', static_folder='../static')
app.config['SECRET_KEY'] = 'your_secret_key_here'
import os
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.getcwd(), "campus_event.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
CORS(app, supports_credentials=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'student'
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    usn = db.Column(db.String(20), unique=True)  # For students
    college_name = db.Column(db.String(100))  # For students
    phone_number = db.Column(db.String(20))  # For students

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('student_id', 'event_id', name='unique_registration'),)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'), nullable=False)
    attended = db.Column(db.Boolean, default=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comments = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Helper functions for password hashing
def set_password(user, password):
    user.password = generate_password_hash(password)

def check_password(user, password):
    return check_password_hash(user.password, password)

# Admin login
@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    print("Received data:", data)
    name = data.get('name')
    password = data.get('password')
    print("Name:", name, "Password:", password)
    user = User.query.filter_by(role='admin', name=name).first()
    print("User found:", user)
    if user:
        print("User password:", user.password)
        print("Check password:", check_password(user, password))
    if user and check_password(user, password):
        login_user(user)
        return jsonify({'message': 'Admin logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Student login
@app.route('/student/login', methods=['POST'])
def student_login():
    data = request.json
    print("Student login data:", data)
    usn = data.get('usn')
    college_name = data.get('college_name')
    phone_number = data.get('phone_number')
    print("USN:", usn, "College:", college_name, "Phone:", phone_number)
    user = User.query.filter_by(role='student', usn=usn, college_name=college_name, phone_number=phone_number).first()
    print("Student user found:", user)
    if user:
        login_user(user)
        return jsonify({'message': 'Student logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

# Admin creates event
@app.route('/events/create', methods=['POST'])
@login_required
def create_event():
    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json
    title = data.get('title')
    type_ = data.get('type')
    date_str = data.get('date')
    description = data.get('description')
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except Exception:
        return jsonify({'message': 'Invalid date format, use YYYY-MM-DD'}), 400
    event = Event(title=title, type=type_, date=date, description=description, created_by=current_user.id)
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully'}), 201

# List all events
@app.route('/events', methods=['GET'])
def list_events():
    events = Event.query.all()
    events_list = []
    for e in events:
        events_list.append({
            'id': e.id,
            'title': e.title,
            'type': e.type,
            'date': e.date.strftime('%Y-%m-%d'),
            'description': e.description
        })
    return jsonify(events_list), 200

# Student registers for event
@app.route('/events/register', methods=['POST'])
@login_required
def register_event():
    if current_user.role != 'student':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json
    event_id = data.get('event_id')
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    existing_registration = Registration.query.filter_by(student_id=current_user.id, event_id=event_id).first()
    if existing_registration:
        return jsonify({'message': 'Already registered'}), 400
    registration = Registration(student_id=current_user.id, event_id=event_id)
    db.session.add(registration)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'}), 201

# Mark attendance
@app.route('/events/attendance', methods=['POST'])
@login_required
def mark_attendance():
    if current_user.role != 'student':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json
    event_id = data.get('event_id')
    registration = Registration.query.filter_by(student_id=current_user.id, event_id=event_id).first()
    if not registration:
        return jsonify({'message': 'Not registered for event'}), 400
    attendance = Attendance.query.filter_by(registration_id=registration.id).first()
    if attendance:
        attendance.attended = True
    else:
        attendance = Attendance(registration_id=registration.id, attended=True)
        db.session.add(attendance)
    db.session.commit()
    return jsonify({'message': 'Attendance marked'}), 200

# Submit feedback
@app.route('/events/feedback', methods=['POST'])
@login_required
def submit_feedback():
    if current_user.role != 'student':
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.json
    event_id = data.get('event_id')
    rating = data.get('rating')
    comments = data.get('comments', '')
    registration = Registration.query.filter_by(student_id=current_user.id, event_id=event_id).first()
    if not registration:
        return jsonify({'message': 'Not registered for event'}), 400
    existing_feedback = Feedback.query.filter_by(registration_id=registration.id).first()
    if existing_feedback:
        return jsonify({'message': 'Feedback already submitted'}), 400
    if not (1 <= rating <= 5):
        return jsonify({'message': 'Rating must be between 1 and 5'}), 400
    feedback = Feedback(registration_id=registration.id, rating=rating, comments=comments)
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback submitted'}), 201

# Reports

# Event popularity report (sorted by registrations)
@app.route('/reports/event-popularity', methods=['GET'])
@login_required
def event_popularity_report():
    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    from sqlalchemy import func
    results = db.session.query(
        Event.id,
        Event.title,
        func.count(Registration.id).label('registrations')
    ).outerjoin(Registration, Event.id == Registration.event_id).group_by(Event.id).order_by(func.count(Registration.id).desc()).all()
    report = []
    for r in results:
        report.append({
            'event_id': r.id,
            'title': r.title,
            'registrations': r.registrations
        })
    return jsonify(report), 200

# Student participation report (events attended per student)
@app.route('/reports/student-participation', methods=['GET'])
@login_required
def student_participation_report():
    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    from sqlalchemy import func
    results = db.session.query(
        User.id,
        User.name,
        func.count(Attendance.id).label('events_attended')
    ).join(Registration, User.id == Registration.student_id)\
     .join(Attendance, Registration.id == Attendance.registration_id)\
     .filter(Attendance.attended == True)\
     .group_by(User.id).order_by(func.count(Attendance.id).desc()).all()
    report = []
    for r in results:
        report.append({
            'student_id': r.id,
            'name': r.name,
            'events_attended': r.events_attended
        })
    return jsonify(report), 200

# Bonus: Top 3 most active students
@app.route('/reports/top-active-students', methods=['GET'])
@login_required
def top_active_students():
    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    from sqlalchemy import func
    results = db.session.query(
        User.id,
        User.name,
        func.count(Attendance.id).label('events_attended')
    ).join(Registration, User.id == Registration.student_id)\
     .join(Attendance, Registration.id == Attendance.registration_id)\
     .filter(Attendance.attended == True)\
     .group_by(User.id).order_by(func.count(Attendance.id).desc()).limit(3).all()
    report = []
    for r in results:
        report.append({
            'student_id': r.id,
            'name': r.name,
            'events_attended': r.events_attended
        })
    return jsonify(report), 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/login', methods=['GET'])
def admin_login_page():
    return render_template('admin_login.html')

@app.route('/student/login', methods=['GET'])
def student_login_page():
    return render_template('student_login.html')

@app.route('/admin/dashboard', methods=['GET'])
@login_required
def admin_dashboard_page():
    if current_user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    return render_template('admin_dashboard.html')

@app.route('/student/dashboard', methods=['GET'])
@login_required
def student_dashboard_page():
    if current_user.role != 'student':
        return jsonify({'message': 'Unauthorized'}), 403
    return render_template('student_dashboard.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
