# Campus Event Management Platform - TODO

## Project Setup

- [x] Create project directories (backend, frontend, static, templates)
- [x] Set up Flask app with requirements.txt
- [x] Initialize database with SQLAlchemy

## Database Models

- [x] Create User model (admin/student)
- [x] Create Event model
- [x] Create Registration model
- [x] Create Attendance model
- [x] Create Feedback model

## Authentication

- [x] Implement admin login route (/admin/login)
- [x] Implement student login route (/student/login)
- [x] Add session management

## Event Management

- [x] Implement event creation (/events/create) - Admin only
- [x] Implement event listing (/events) - Public
- [ ] Implement event update/delete (optional, for completeness)

## Student Features

- [x] Implement event registration (/events/register)
- [x] Implement attendance marking (/events/attendance)
- [x] Implement feedback submission (/events/feedback)

## Reports

- [x] Implement event popularity report (/reports/event-popularity)
- [x] Implement student participation report (/reports/student-participation)
- [x] Add bonus: Top 3 most active students

## Frontend UI

- [x] Create admin login page
- [x] Create student login page
- [x] Create admin dashboard (create events)
- [x] Create student dashboard (browse events, register, etc.)
- [x] Create event listing page
- [x] Add basic CSS styling
- [x] Add JavaScript for form submissions

## Sample Data & Testing

- [x] Create script to populate sample data
- [x] Test all APIs
- [x] Test UI workflows
- [x] Update README with setup instructions

## Project Management

- [x] Create package.json with npm scripts
- [x] Add convenient setup and run commands

## Final Touches

- [x] Handle edge cases (duplicate registrations, etc.)
- [x] Ensure modularity and cleanliness
- [x] Run end-to-end test
