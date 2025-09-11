// Create Event
document
  .getElementById("createEventForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const title = document.getElementById("title").value;
    const type = document.getElementById("type").value;
    const date = document.getElementById("date").value;
    const description = document.getElementById("description").value;

    const response = await fetch("http://localhost:5000/events/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({ title, type, date, description }),
    });

    const data = await response.json();
    document.getElementById("createMessage").textContent = data.message;
  });

// Event Popularity Report
document
  .getElementById("eventPopularityBtn")
  .addEventListener("click", async () => {
    const response = await fetch(
      "http://localhost:5000/reports/event-popularity",
      { credentials: "include" }
    );
    const data = await response.json();
    displayReports(data, "Event Popularity");
  });

// Student Participation Report
document
  .getElementById("studentParticipationBtn")
  .addEventListener("click", async () => {
    const response = await fetch(
      "http://localhost:5000/reports/student-participation",
      { credentials: "include" }
    );
    const data = await response.json();
    displayReports(data, "Student Participation");
  });

// Top Active Students
document
  .getElementById("topActiveStudentsBtn")
  .addEventListener("click", async () => {
    const response = await fetch(
      "http://localhost:5000/reports/top-active-students",
      { credentials: "include" }
    );
    const data = await response.json();
    displayReports(data, "Top 3 Active Students");
  });

function displayReports(data, title) {
  const reportsDiv = document.getElementById("reports");
  reportsDiv.innerHTML = `<h3>${title}</h3>`;
  data.forEach((item) => {
    const div = document.createElement("div");
    div.className = "report";
    div.innerHTML = Object.keys(item)
      .map((key) => `<p><strong>${key}:</strong> ${item[key]}</p>`)
      .join("");
    reportsDiv.appendChild(div);
  });
}
