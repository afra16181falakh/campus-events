// Load Events
async function loadEvents() {
  const response = await fetch("http://localhost:5000/events");
  const events = await response.json();
  const eventsList = document.getElementById("eventsList");
  eventsList.innerHTML = "";
  events.forEach((event) => {
    const div = document.createElement("div");
    div.className = "event";
    div.innerHTML = `
            <h3>${event.title}</h3>
            <p><strong>Type:</strong> ${event.type}</p>
            <p><strong>Date:</strong> ${event.date}</p>
            <p><strong>Description:</strong> ${event.description}</p>
            <button onclick="registerForEvent(${event.id})">Register</button>
        `;
    eventsList.appendChild(div);
  });
}

async function registerForEvent(eventId) {
  const response = await fetch("http://localhost:5000/events/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({ event_id: eventId }),
  });
  const data = await response.json();
  alert(data.message);
}

// Mark Attendance
document
  .getElementById("attendanceForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const eventId = document.getElementById("eventIdAttendance").value;

    const response = await fetch("http://localhost:5000/events/attendance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({ event_id: eventId }),
    });

    const data = await response.json();
    document.getElementById("attendanceMessage").textContent = data.message;
  });

// Submit Feedback
document
  .getElementById("feedbackForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const eventId = document.getElementById("eventIdFeedback").value;
    const rating = document.getElementById("rating").value;
    const comments = document.getElementById("comments").value;

    const response = await fetch("http://localhost:5000/events/feedback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        event_id: eventId,
        rating: parseInt(rating),
        comments,
      }),
    });

    const data = await response.json();
    document.getElementById("feedbackMessage").textContent = data.message;
  });

// Load events on page load
loadEvents();
