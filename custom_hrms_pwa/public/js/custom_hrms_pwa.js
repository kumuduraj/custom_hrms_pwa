// Custom HRMS PWA JavaScript

// Set default date to today
function setDefaultDate() {
  if (!localStorage.getItem("selectedDate")) {
    localStorage.setItem(
      "selectedDate",
      new Date().toISOString().split("T")[0]
    );
  }
}

// Hide expenses/claims elements
function hideExpenses() {
  // Hide bottom nav claims tab
  document.querySelectorAll("a").forEach(function (el) {
    var href = el.getAttribute("href") || "";
    var text = el.textContent.toLowerCase();
    if (href.indexOf("/claims") !== -1 || text.indexOf("claim") !== -1) {
      el.style.display = "none";
    }
  });

  // Hide "Claim an Expense" quick action
  document.querySelectorAll("a, button, div").forEach(function (el) {
    var text = el.textContent.toLowerCase();
    if (text.indexOf("claim an expense") !== -1) {
      el.style.display = "none";
    }
  });
}

// Rebrand Frappe HR to SLHRM
function rebrandApp() {
  // Change page title
  if (document.title.indexOf("Frappe HR") !== -1) {
    document.title = document.title.replace(/Frappe HR/g, "SLHRM");
  }

  // Change app name in nav header
  document.querySelectorAll("h1, h2, h3, .app-name, .page-title").forEach(function (el) {
    if (el.textContent.trim() === "Frappe HR") {
      el.textContent = "SLHRM";
    }
  });

  // Change any element with "Frappe HR" text
  document.querySelectorAll("*").forEach(function (el) {
    if (el.children.length === 0 && el.textContent.trim() === "Frappe HR") {
      el.textContent = "SLHRM";
    }
  });
}

// Initialize PWA
function initPWA() {
  setDefaultDate();

  // Rebrand
  rebrandApp();
  hideExpenses();

  // MutationObserver to catch dynamic content
  var observer = new MutationObserver(function () {
    rebrandApp();
    hideExpenses();
  });
  observer.observe(document.body, { childList: true, subtree: true });

  // Register service worker for PWA
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker
      .register("/assets/custom_hrms_pwa/sw.js")
      .then(function (registration) {
        console.log("SW registered:", registration);
      })
      .catch(function (error) {
        console.log("SW registration failed:", error);
      });
  }
}

// Run on DOM ready
document.addEventListener("DOMContentLoaded", initPWA);
