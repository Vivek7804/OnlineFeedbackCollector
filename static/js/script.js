document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("feedbackForm");
  if (form) {
    form.addEventListener("submit", (event) => {
      const rating = form.querySelector('input[name="rating"]:checked');
      if (!rating) {
        event.preventDefault();
        alert("Please select a rating from 1 to 5.");
      }
    });
  }
});
