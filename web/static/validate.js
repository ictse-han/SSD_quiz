document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("form[data-validate-password]").forEach((form) => {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const password = form.querySelector('input[name="password"]').value;

      fetch("/api/check-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.valid) {
            form.submit();
          } else {
            alert("Password does not meet the requirements.");
          }
        });
    });
  });
});
