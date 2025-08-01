// Show temporary alert messages (e.g., "Added to cart")
function showMessage(msg, duration = 2000) {
  const msgBox = document.createElement("div");
  msgBox.className = "popup-message";
  msgBox.textContent = msg;
  document.body.appendChild(msgBox);
  setTimeout(() => {
    msgBox.remove();
  }, duration);
}

// Validate password and confirm password match (for register page)
function validateRegisterForm() {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    const password = document.querySelector("input[name='password']").value;
    const confirm = document.querySelector("input[name='confirm']").value;
    if (password !== confirm) {
      e.preventDefault();
      showMessage("❗ Passwords do not match", 2500);
    }
  });
}

// Add to cart button override (instant feedback + redirect)
function setupAddToCartButtons() {
  const buttons = document.querySelectorAll("button[data-cart]");
  buttons.forEach(btn => {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      const url = btn.getAttribute("data-cart");
      showMessage("✅ Added to cart");
      setTimeout(() => {
        window.location.href = url;
      }, 500);
    });
  });
}

// Confirm before Pay
function setupPayButton() {
  const payBtn = document.querySelector("form[action='/pay'] button");
  if (payBtn) {
    payBtn.addEventListener("click", function (e) {
      if (!confirm("Are you sure you want to place the order?")) {
        e.preventDefault();
      }
    });
  }
}

// Run on every page load
document.addEventListener("DOMContentLoaded", () => {
  validateRegisterForm();
  setupAddToCartButtons();
  setupPayButton();
});
