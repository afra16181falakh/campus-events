from app import app, db, User, Event, set_password
from datetime import datetime

def populate_sample_data():
    with app.app_context():
        # Check if data already exists
        if User.query.filter_by(role='admin').first():
            print("Sample data already exists!")
            return

        # Create admin user
        admin = User(role='admin', name='admin')
        set_password(admin, 'password')
        db.session.add(admin)

        # Create sample students
        students = [
            User(role='student', name='John Doe', usn='USN001', college_name='College A', phone_number='1234567890'),
            User(role='student', name='Jane Smith', usn='USN002', college_name='College A', phone_number='0987654321'),
            User(role='student', name='Bob Johnson', usn='USN003', college_name='XYZ University', phone_number='1122334455'),
        ]
        for student in students:
            # Set dummy password for students for login validation
            student.password = 'student123'
            db.session.add(student)

        # Create sample events
        events = [
            Event(title='Tech Seminar', type='Seminar', date=datetime(2023, 10, 15), description='A seminar on latest tech trends', created_by=1),
            Event(title='Cultural Fest', type='Festival', date=datetime(2023, 11, 20), description='Annual cultural festival', created_by=1),
            Event(title='Sports Meet', type='Sports', date=datetime(2023, 12, 5), description='Inter-college sports competition', created_by=1),
        ]
        for event in events:
            db.session.add(event)

        db.session.commit()
        print("Sample data populated successfully!")

if __name__ == '__main__':
    populate_sample_data()
