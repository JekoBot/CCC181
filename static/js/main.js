// Served at /static/js/main.js and linked from templates/base.html.
console.log("UniformQ starter app loaded");

const joinForm = document.getElementById("join-form");
if (joinForm) {
  const joinButton = joinForm.querySelector("button[type=submit]");
  const joinLabel = joinButton.textContent;

  joinForm.addEventListener("submit", () => {
    joinButton.disabled = true;
    joinButton.textContent = "Getting your queue number…";
  });

  // If the student comes back with the browser's Back button, reset the button.
  window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
      joinButton.disabled = false;
      joinButton.textContent = joinLabel;
    }
  });
}
document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!confirm(form.dataset.confirm)) event.preventDefault();
  });
});
