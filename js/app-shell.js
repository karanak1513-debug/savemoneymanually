// ============================================================
// VAULT.FI — App Shell / Layout Manager
// Injects sidebar, sets active nav, populates user info,
// and sets up sidebar mobile toggle.
// ============================================================

import { auth } from "../firebase-config.js";
import { onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { logOut } from "./auth.js";
import { getInitials, showToast, initSidebarToggle } from "./utils.js";

/**
 * Initialize the app shell. Call at top of every app page.
 * @param {string} activePage - "dashboard" | "goals" | "transactions" | "profile"
 * @returns {Promise<firebase.User>} - the authenticated user
 */
export function initAppShell(activePage) {
  return new Promise((resolve, reject) => {
    // Load sidebar HTML
    fetch("partials/sidebar.html")
      .then((r) => r.text())
      .then((html) => {
        const container = document.getElementById("sidebar-container");
        if (container) {
          container.innerHTML = html;
          setupShell(activePage, resolve, reject);
        } else {
          setupShell(activePage, resolve, reject);
        }
      })
      .catch(() => setupShell(activePage, resolve, reject));
  });
}

function setupShell(activePage, resolve, reject) {
  onAuthStateChanged(auth, (user) => {
    if (!user) {
      window.location.href = "auth.html";
      reject();
      return;
    }

    // Mark active nav item
    document.querySelectorAll(".nav-item").forEach((el) => {
      el.classList.toggle("active", el.dataset.page === activePage);
    });

    // Populate user info
    const name   = user.displayName || user.email?.split("@")[0] || "Vaultie";
    const email  = user.email || "";
    const initials = getInitials(name);

    const avatarEl = document.getElementById("sidebar-avatar");
    const nameEl   = document.getElementById("sidebar-name");
    const emailEl  = document.getElementById("sidebar-email");

    if (avatarEl) avatarEl.textContent = initials;
    if (nameEl)   nameEl.textContent   = name;
    if (emailEl)  emailEl.textContent  = email;

    // Logout
    document.getElementById("logout-btn")?.addEventListener("click", async () => {
      try {
        await logOut();
      } catch {
        showToast("Error signing out. Try again.", "error");
      }
    });

    // Mobile sidebar toggle
    initSidebarToggle();

    // Reveal loading overlay
    document.getElementById("loading-overlay")?.classList.add("hidden");

    resolve(user);
  });
}
