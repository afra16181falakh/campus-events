document
  .getElementById("adminLoginForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const password = document.getElementById("password").value;

    const response = await fetch("http://localhost:5000/admin/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({ name, password }),
    });

    const data = await response.json();
    document.getElementById("message").textContent = data.message;

    if (response.ok) {
      // Store session or redirect
      window.location.href = "admin_dashboard.html";
    }
  });
