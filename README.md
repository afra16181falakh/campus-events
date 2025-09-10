Campus Event Management – Reporting Prototype

This prototype is a small Flask + SQLite app that lets you create campus events, register students, mark attendance, collect feedback, and generate a few quick reports. It’s minimal and easy to test.

⸻

Tech Stack
	•	Backend: Flask (Python)
	•	Database: SQLite (campus.db in the repo root)
	•	Testing: Postman / curl

⸻

Setup
	1.	Python: 3.10+ recommended.
	2.	Install dependencies:

pip install -r requirements.txt


⸻

Running the Server
	•	Default port (5000):

python app.py

	•	If 5000 is busy, run on port 5001:

flask run --port=5001

Note: The first run creates campus.db automatically and seeds demo data.

⸻

Demo Data (Auto-seeded)
	•	Colleges: 2
	•	Students: 5 (IDs 1–5)
	•	Events: 3 (IDs 1–3)
	•	Some registrations, attendance, and feedback are preloaded so you can hit the report endpoints immediately.

⸻

Testing with Postman
	1.	Import postman_collection.json into Postman.
	2.	Set the collection variable baseUrl to the server you are running:
	•	http://localhost:5000
	•	or http://localhost:5001 if using a custom port.
	3.	Execute requests in this order for a clean demo:
	•	Health Check
	•	Register Student (valid) → then Register Student (duplicate → 409)
	•	Mark Attendance (valid) → then Attendance (unregistered → 409)
	•	Submit Feedback (valid) → then Feedback (duplicate → 409)
	•	Reports: Popularity, Student Participation (ID 1), Top Students, Events by Type (Workshop)

All errors return JSON with an "error" field and proper HTTP status codes.

⸻

Testing with curl

Set a helper variable for convenience:

BASE=http://localhost:5000

(or use http://localhost:5001 if using a different port)
	•	Health Check

curl -s "$BASE/"

	•	Create Event

curl -s -X POST "$BASE/events" \
  -H "Content-Type: application/json" \
  -d '{"name":"Intro to GenAI","type":"Workshop","date":"2025-10-10","college_id":1}'

	•	Register (valid)

curl -s -X POST "$BASE/register" \
  -H "Content-Type: application/json" \
  -d '{"student_id":1,"event_id":1}'

	•	Register (duplicate → 409)

curl -s -i -X POST "$BASE/register" \
  -H "Content-Type: application/json" \
  -d '{"student_id":1,"event_id":1}'

	•	Attendance (valid)

curl -s -X POST "$BASE/attendance" \
  -H "Content-Type: application/json" \
  -d '{"student_id":1,"event_id":1,"status":"present"}'

	•	Attendance (not registered → 409)

curl -s -i -X POST "$BASE/attendance" \
  -H "Content-Type: application/json" \
  -d '{"student_id":5,"event_id":3,"status":"present"}'

	•	Feedback (valid)

curl -s -X POST "$BASE/feedback" \
  -H "Content-Type: application/json" \
  -d '{"student_id":1,"event_id":1,"rating":5}'

	•	Feedback (duplicate → 409)

curl -s -i -X POST "$BASE/feedback" \
  -H "Content-Type: application/json" \
  -d '{"student_id":1,"event_id":1,"rating":4}'

	•	Reports

curl -s "$BASE/reports/popularity"
curl -s "$BASE/reports/student-participation/1"
curl -s "$BASE/reports/top-students"
curl -s "$BASE/reports/events?type=Workshop"


⸻

Error Handling
	•	Duplicate registration → HTTP 409
	•	Feedback is one per student-event (duplicate → 409)
	•	Attendance requires registration (otherwise → 409)
	•	All errors return JSON with an "error" field

⸻

Resetting the Database

If you want a fresh start:

rm -f campus.db
python app.py

This recreates the database and re-seeds the demo data automatically.

⸻

Screenshots / Demo

Screenshots of tested endpoints (from Postman) are saved in the reports/ folder:

Endpoint	Screenshot
Health Check	reports/health.png
Register Student	reports/register.png
Attendance	reports/attendance.png
Feedback	reports/feedback.png
Reports	reports/reports.png

These show the server responses, error handling, and reports in action.
