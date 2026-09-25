// ============================================================
// VAULT.FI — AUTHENTICATION GATEWAY CONTROLLER
// Single-Action Google Auth via Firebase + 3D Canvas Integration
// ============================================================

import {
  auth,
  provider,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
} from "./firebase-config.js";
import { initVault3DCanvas } from "./vault-canvas-3d.js";

// DOM Elements
const canvasEl = document.getElementById("vault-3d-stage");
const btnGoogleAuth = document.getElementById("btn-google-auth");
const btnText = document.getElementById("btn-auth-text");
const btnSpinner = document.getElementById("btn-auth-spinner");
const googleIcon = document.getElementById("google-g-icon");

const authContainer = document.getElementById("auth-action-container");
const sessionContainer = document.getElementById("session-active-container");
const sessionAvatar = document.getElementById("session-user-avatar");
const sessionName = document.getElementById("session-user-name");
const sessionEmail = document.getElementById("session-user-email");
const btnSignOut = document.getElementById("btn-signout");
const feedbackBanner = document.getElementById("gateway-feedback");

// Initialize 3D Canvas
let vault3D = null;
if (canvasEl) {
  vault3D = initVault3DCanvas(canvasEl);
}

// Hover interactivity between 3D Canvas and Google Auth Action
if (btnGoogleAuth && vault3D) {
  btnGoogleAuth.addEventListener("mouseenter", () => {
    if (!btnGoogleAuth.disabled) {
      vault3D.setMode("HOVER");
    }
  });

  btnGoogleAuth.addEventListener("mouseleave", () => {
    if (!btnGoogleAuth.disabled) {
      vault3D.setMode("IDLE");
    }
  });
}

// Single Action: Authenticate with Google via Firebase
btnGoogleAuth?.addEventListener("click", async () => {
  clearFeedback();
  setLoadingState(true);
  if (vault3D) vault3D.setMode("AUTHENTICATING");

  try {
    const result = await signInWithPopup(auth, provider);
    const user = result.user;
    if (vault3D) vault3D.setMode("SUCCESS");
    showFeedback("Successfully authenticated with Google.", "success");
    renderAuthenticatedSession(user);
  } catch (error) {
    console.error("[Vault.fi Gateway] Auth error:", error);
    if (vault3D) vault3D.setMode("IDLE");

    let message = "Could not authenticate with Google. Please try again.";
    if (error.code === "auth/popup-closed-by-user") {
      message = "Google Sign-In was cancelled.";
    } else if (error.code === "auth/popup-blocked") {
      message = "Popup was blocked by your browser. Please allow popups for this site.";
    } else if (error.code === "auth/network-request-failed") {
      message = "Network error. Please check your internet connection.";
    }
    showFeedback(message, "error");
  } finally {
    setLoadingState(false);
  }
});

// Sign Out Handler
btnSignOut?.addEventListener("click", async () => {
  try {
    await signOut(auth);
    if (vault3D) vault3D.setMode("IDLE");
    showFeedback("Signed out successfully.", "info");
    renderUnauthenticated();
  } catch (err) {
    console.error("[Vault.fi Gateway] SignOut error:", err);
  }
});

// Firebase Auth State Observer
onAuthStateChanged(auth, (user) => {
  if (user) {
    if (vault3D) vault3D.setMode("SUCCESS");
    renderAuthenticatedSession(user);
  } else {
    if (vault3D) vault3D.setMode("IDLE");
    renderUnauthenticated();
  }
});

// UI State Renderers
function setLoadingState(isLoading) {
  if (!btnGoogleAuth) return;
  btnGoogleAuth.disabled = isLoading;

  if (isLoading) {
    btnGoogleAuth.classList.add("loading");
    if (btnText) btnText.textContent = "Connecting to Google...";
    if (btnSpinner) btnSpinner.style.display = "inline-block";
    if (googleIcon) googleIcon.style.opacity = "0.4";
  } else {
    btnGoogleAuth.classList.remove("loading");
    if (btnText) btnText.textContent = "Continue with Google";
    if (btnSpinner) btnSpinner.style.display = "none";
    if (googleIcon) googleIcon.style.opacity = "1";
  }
}

function renderAuthenticatedSession(user) {
  if (authContainer) authContainer.style.display = "none";
  if (sessionContainer) {
    sessionContainer.style.display = "block";
    sessionContainer.classList.add("fade-in");
  }

  const name = user.displayName || user.email?.split("@")[0] || "Authenticated User";
  const email = user.email || "";
  const photo = user.photoURL;

  if (sessionName) sessionName.textContent = name;
  if (sessionEmail) sessionEmail.textContent = email;

  if (sessionAvatar) {
    if (photo) {
      sessionAvatar.innerHTML = `<img src="${photo}" alt="${name}" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;" />`;
    } else {
      const initial = (name[0] || "U").toUpperCase();
      sessionAvatar.innerHTML = `<span style="font-weight: 700; color: #2563EB;">${initial}</span>`;
    }
  }
}

function renderUnauthenticated() {
  if (authContainer) authContainer.style.display = "block";
  if (sessionContainer) sessionContainer.style.display = "none";
}

function showFeedback(text, type = "info") {
  if (!feedbackBanner) return;
  feedbackBanner.textContent = text;
  feedbackBanner.className = `gateway-feedback active ${type}`;

  setTimeout(() => {
    if (feedbackBanner.textContent === text) {
      clearFeedback();
    }
  }, 4500);
}

function clearFeedback() {
  if (!feedbackBanner) return;
  feedbackBanner.textContent = "";
  feedbackBanner.className = "gateway-feedback";
}
