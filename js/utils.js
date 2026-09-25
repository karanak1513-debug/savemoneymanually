// ============================================================
// VAULT.FI — Shared Utilities
// ============================================================

// ── Currency Formatter ──────────────────────────────────────
export function formatCurrency(amount, currency = "INR", compact = false) {
  if (compact && Math.abs(amount) >= 1000) {
    const formatter = new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency,
      notation: "compact",
      maximumFractionDigits: 1,
    });
    return formatter.format(amount);
  }
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

// ── Date Formatters ─────────────────────────────────────────
export function formatDate(dateInput) {
  const date =
    dateInput?.toDate ? dateInput.toDate()
    : dateInput instanceof Date ? dateInput
    : new Date(dateInput);
  return new Intl.DateTimeFormat("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(date);
}

export function formatRelativeDate(dateInput) {
  const date =
    dateInput?.toDate ? dateInput.toDate()
    : dateInput instanceof Date ? dateInput
    : new Date(dateInput);
  const now = new Date();
  const diff = now - date;
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  if (days === 0) return "Today";
  if (days === 1) return "Yesterday";
  if (days < 7) return `${days} days ago`;
  return formatDate(date);
}

// ── Toast Notification ──────────────────────────────────────
const TOAST_ICONS = { success: "✓", error: "✕", info: "💡" };

export function showToast(message, type = "info", duration = 3500) {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${TOAST_ICONS[type] ?? "ℹ"}</span>
    <span>${message}</span>
  `;
  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.add("hide");
    toast.addEventListener("animationend", () => toast.remove());
  }, duration);
}

// ── Modal Helpers ────────────────────────────────────────────
export function openModal(overlayId) {
  const overlay = document.getElementById(overlayId);
  overlay?.classList.add("open");
  document.body.style.overflow = "hidden";
}

export function closeModal(overlayId) {
  const overlay = document.getElementById(overlayId);
  overlay?.classList.remove("open");
  document.body.style.overflow = "";
}

// ── Generate Initials ────────────────────────────────────────
export function getInitials(name) {
  if (!name) return "?";
  return name
    .split(" ")
    .map((w) => w[0])
    .join("")
    .toUpperCase()
    .slice(0, 2);
}

// ── Debounce ─────────────────────────────────────────────────
export function debounce(fn, ms = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

// ── Days Until ───────────────────────────────────────────────
export function daysUntil(dateInput) {
  const target =
    dateInput?.toDate ? dateInput.toDate()
    : dateInput instanceof Date ? dateInput
    : new Date(dateInput);
  const now = new Date();
  const diff = target - now;
  return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)));
}

// ── Progress Percentage ──────────────────────────────────────
export function calcProgress(current, target) {
  if (!target || target === 0) return 0;
  return Math.min(100, Math.round((current / target) * 100));
}

// ── Category Config ──────────────────────────────────────────
export const CATEGORIES = {
  food:        { label: "Food & Drinks",  emoji: "🍔", color: "#f97316" },
  transport:   { label: "Transport",      emoji: "🚗", color: "#06b6d4" },
  shopping:    { label: "Shopping",       emoji: "🛍️", color: "#8b5cf6" },
  entertainment:{ label: "Entertainment", emoji: "🎮", color: "#ec4899" },
  health:      { label: "Health",        emoji: "💊", color: "#10b981" },
  education:   { label: "Education",     emoji: "📚", color: "#3b82f6" },
  bills:       { label: "Bills",         emoji: "📄", color: "#ef4444" },
  salary:      { label: "Salary",        emoji: "💼", color: "#22c55e" },
  freelance:   { label: "Freelance",     emoji: "💻", color: "#a3e635" },
  investment:  { label: "Investment",    emoji: "📈", color: "#fbbf24" },
  savings:     { label: "Savings",       emoji: "🐷", color: "#7c3aed" },
  other:       { label: "Other",         emoji: "💸", color: "#94a3b8" },
};

// ── Goal Icons / Colors ──────────────────────────────────────
export const GOAL_ICONS = ["🏠","🚗","✈️","📱","💻","🎓","💍","🐶","🏋️","🎸","⛺","🎮","📸","🌴","🏄","💰","🏦","🎯","🎁","🛒"];
export const GOAL_COLORS = [
  "#7c3aed","#4f46e5","#06b6d4","#10b981","#f59e0b",
  "#ef4444","#ec4899","#3b82f6","#8b5cf6","#14b8a6",
];

// ── Auth Guard ────────────────────────────────────────────────
export function requireAuth(auth, redirectTo = "auth.html") {
  return new Promise((resolve, reject) => {
    const unsub = auth.onAuthStateChanged((user) => {
      unsub();
      if (user) { resolve(user); }
      else { window.location.href = redirectTo; reject(); }
    });
  });
}

// ── Sidebar Mobile Toggle ─────────────────────────────────────
export function initSidebarToggle() {
  const sidebar  = document.getElementById("sidebar");
  const overlay  = document.getElementById("sidebar-overlay");
  const hamburger = document.getElementById("hamburger-btn");

  hamburger?.addEventListener("click", () => {
    sidebar?.classList.toggle("open");
    overlay?.classList.toggle("hidden");
  });
  overlay?.addEventListener("click", () => {
    sidebar?.classList.remove("open");
    overlay?.classList.add("hidden");
  });
}

// ── Reveal on Scroll ──────────────────────────────────────────
export function initReveal() {
  const observer = new IntersectionObserver(
    (entries) => entries.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add("visible"); observer.unobserve(e.target); }
    }),
    { threshold: 0.1 }
  );
  document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));
}

// ── Format number with commas ────────────────────────────────
export function numComma(n) {
  return Number(n).toLocaleString("en-IN");
}

// ── Random ID ────────────────────────────────────────────────
export function randomId() {
  return Math.random().toString(36).slice(2, 11);
}
