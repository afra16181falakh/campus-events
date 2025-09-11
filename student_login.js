document
  .getElementById("studentLoginForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const usn = document.getElementById("usn").value;
    const college_name = document.getElementById("college_name").value;
    const phone_number = document.getElementById("phone_number").value;

    const response = await fetch("http://localhost:5000/student/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({ usn, college_name, phone_number }),
    });

    const data = await response.json();
    document.getElementById("message").textContent = data.message;

    if (response.ok) {
      // Store session or redirect
      window.location.href = "student_dashboard.html";
    }
  });
