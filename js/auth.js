// ============================================================
// VAULT.FI — Authentication Service
// Google Auth + Demo Mode + Session Management
// ============================================================

import { auth, googleProvider } from "../firebase-config.js";
import {
  signInWithPopup,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  sendPasswordResetEmail,
  updateProfile,
  signOut,
  onAuthStateChanged,
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { seedInitialUserData } from "./firestore.js";

const DEMO_USER_KEY = "vaultfi_demo_user";

// Track current user state in-memory
let activeAuthUser = null;
const authListeners = [];

export function getActiveUser() {
  if (activeAuthUser) return activeAuthUser;
  // Check demo user
  try {
    const raw = localStorage.getItem(DEMO_USER_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) {}
  return null;
}

// ── Google Sign In ───────────────────────────────────────────
export async function signInWithGoogle() {
  try {
    const credential = await signInWithPopup(auth, googleProvider);
    const user = credential.user;
    // Clear demo flag if any
    localStorage.removeItem(DEMO_USER_KEY);
    activeAuthUser = user;
    // Seed initial user data if needed
    await seedInitialUserData(user.uid, user);
    notifyAuthListeners(user);
    return user;
  } catch (error) {
    console.error("[Auth] Google Sign-In error:", error);
    // If popup is blocked by browser or restricted origin, offer clean message
    if (error.code === "auth/popup-blocked" || error.code === "auth/operation-not-supported-in-this-environment") {
      throw new Error("Popup was blocked or not supported in this preview. Please allow popups or use 'Instant Demo Mode'.");
    }
    throw error;
  }
}

// ── Email / Password Sign In ──────────────────────────────────
export async function signInWithEmail(email, password) {
  try {
    const credential = await signInWithEmailAndPassword(auth, email, password);
    const user = credential.user;
    localStorage.removeItem(DEMO_USER_KEY);
    activeAuthUser = user;
    await seedInitialUserData(user.uid, user);
    notifyAuthListeners(user);
    return user;
  } catch (error) {
    console.error("[Auth] Email Sign-In error:", error);
    throw error;
  }
}

// ── Email / Password Sign Up ──────────────────────────────────
export async function signUpWithEmail(email, password, displayName) {
  try {
    const credential = await createUserWithEmailAndPassword(auth, email, password);
    const user = credential.user;
    if (displayName) {
      await updateProfile(user, { displayName });
    }
    localStorage.removeItem(DEMO_USER_KEY);
    activeAuthUser = user;
    await seedInitialUserData(user.uid, user);
    notifyAuthListeners(user);
    return user;
  } catch (error) {
    console.error("[Auth] Email Sign-Up error:", error);
    throw error;
  }
}

// ── Password Reset ───────────────────────────────────────────
export async function resetPassword(email) {
  try {
    await sendPasswordResetEmail(auth, email);
    return true;
  } catch (error) {
    console.error("[Auth] Reset Password error:", error);
    throw error;
  }
}

// ── Instant Demo / Guest Mode ─────────────────────────────────
export async function signInAsDemoUser() {
  const demoUser = {
    uid: "demo_genz_user_007",
    email: "cyber.saver@vault.fi",
    displayName: "Kai Sterling",
    photoURL: "assets/hero_avatar.jpg",
    isDemo: true,
  };
  localStorage.setItem(DEMO_USER_KEY, JSON.stringify(demoUser));
  activeAuthUser = demoUser;
  await seedInitialUserData(demoUser.uid, demoUser);
  notifyAuthListeners(demoUser);
  return demoUser;
}

// ── Sign Out ─────────────────────────────────────────────────
export async function logOut() {
  localStorage.removeItem(DEMO_USER_KEY);
  activeAuthUser = null;
  try {
    await signOut(auth);
  } catch (e) {
    console.warn("[Auth] signOut caught:", e);
  }
  notifyAuthListeners(null);
  window.location.hash = "#/";
}

// ── Auth Observer ────────────────────────────────────────────
function notifyAuthListeners(user) {
  authListeners.forEach((fn) => {
    try {
      fn(user);
    } catch (e) {
      console.error("[Auth] listener error:", e);
    }
  });
}

export function onAuth(callback) {
  authListeners.push(callback);

  // Check demo user first
  const demo = getActiveUser();
  if (demo && demo.isDemo) {
    setTimeout(() => callback(demo), 10);
    return () => {
      const idx = authListeners.indexOf(callback);
      if (idx !== -1) authListeners.splice(idx, 1);
    };
  }

  // Subscribe to real Firebase auth
  const unsubscribe = onAuthStateChanged(auth, async (user) => {
    if (user) {
      activeAuthUser = user;
      await seedInitialUserData(user.uid, user);
      callback(user);
    } else {
      const currentDemo = getActiveUser();
      if (currentDemo && currentDemo.isDemo) {
        activeAuthUser = currentDemo;
        callback(currentDemo);
      } else {
        activeAuthUser = null;
        callback(null);
      }
    }
  });

  return () => {
    unsubscribe();
    const idx = authListeners.indexOf(callback);
    if (idx !== -1) authListeners.splice(idx, 1);
  };
}
