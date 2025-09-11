# Campus Event Management Platform

A full-stack web application for managing campus events with separate logins for admins and students.

## Features

- **Admin Features:**

  - Login with name and password
  - Create events (title, type, date, description)
  - View reports (event popularity, student participation, top active students)

- **Student Features:**

  - Login with USN, college name, and phone number
  - Browse and register for events
  - Mark attendance
  - Submit feedback (1-5 rating)

- **Reports:**
  - Total registrations per event
  - Attendance percentage
  - Average feedback score
  - Event Popularity Report (sorted by registrations)
  - Student Participation Report (events attended per student)
  - Top 3 most active students

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** Flask-Login

## Setup Instructions

### Quick Setup (Recommended)

```bash
npm run install-deps  # Install Python deps, create DB, populate sample data
npm start            # Start the Flask server
```

### Manual Setup

1. **Navigate to the project directory:**

   ```bash
   cd /Users/afrafalakh/Desktop/campus-event
   ```

2. **Install Python dependencies:**

   ```bash
   npm run setup
   # OR manually: cd backend && pip install -r requirements.txt
   ```

3. **Initialize database:**

   ```bash
   npm run db-init
   # OR manually: cd backend && python create_db.py
   ```

4. **Populate sample data (optional):**

   ```bash
   npm run populate-data
   # OR manually: cd backend && python sample_data.py
   ```

5. **Run the Flask application:**

   ```bash
   npm start
   # OR manually: cd backend && python app.py
   ```

6. **Access the application:**
   - Backend API: `http://127.0.0.1:5000`
   - Frontend pages: Open HTML files in `frontend/` directory in browser

## Database Schema

### Users Table

- id (Primary Key)
- role (admin/student)
- name
- password (hashed)
- usn (for students)
- college_name (for students)
- phone_number (for students)

### Events Table

- id (Primary Key)
- title
- type
- date
- description
- created_by (Foreign Key to Users)

### Registrations Table

- id (Primary Key)
- student_id (Foreign Key to Users)
- event_id (Foreign Key to Events)
- Unique constraint on (student_id, event_id)

### Attendance Table

- id (Primary Key)
- registration_id (Foreign Key to Registrations)
- attended (Boolean)

### Feedback Table

- id (Primary Key)
- registration_id (Foreign Key to Registrations)
- rating (1-5)
- comments

## API Endpoints

- `POST /admin/login` - Admin login
- `POST /student/login` - Student login
- `POST /events/create` - Create event (Admin only)
- `GET /events` - List all events
- `POST /events/register` - Register for event (Student only)
- `POST /events/attendance` - Mark attendance (Student only)
- `POST /events/feedback` - Submit feedback (Student only)
- `GET /reports/event-popularity` - Event popularity report (Admin only)
- `GET /reports/student-participation` - Student participation report (Admin only)
- `GET /reports/top-active-students` - Top 3 active students (Admin only)

## Sample Data

- Admin: name="Admin User", password="admin123"
- Students: USN001, USN002, USN003 with respective details
- Events: Tech Seminar, Cultural Fest, Sports Meet

## Usage

1. Start the backend server.
2. Open the frontend HTML files in a browser.
3. Login as admin or student.
4. Admins can create events and view reports.
5. Students can browse events, register, mark attendance, and submit feedback.

## Edge Cases Handled

- Duplicate registrations prevented
- Attendance can only be marked once per registration
- Feedback can only be submitted once per registration
- Invalid ratings (not 1-5) rejected
- Unauthorized access to admin-only features

## Future Improvements

- Add event update/delete functionality
- Implement proper session management in frontend
- Add more detailed error handling
- Improve UI/UX with a modern framework like React
- Add email notifications for event registrations
