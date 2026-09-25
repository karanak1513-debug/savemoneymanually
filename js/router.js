// ============================================================
// VAULT.FI — Client Router & Route Guard
// Manages the 6 distinct pages, SEO metadata, and auth guards.
// ============================================================

import { getActiveUser, onAuth } from "./auth.js";

export const ROUTES = {
  LANDING: "/",
  DASHBOARD: "/app/dashboard",
  VAULTS: "/app/vaults",
  COOLDOWN: "/app/cooldown",
  INSIGHTS: "/app/insights",
  SETTINGS: "/app/settings",
};

const ROUTE_CONFIG = {
  [ROUTES.LANDING]: {
    id: "page-landing",
    authRequired: false,
    title: "Vault.fi | Autonomous 3D Savings Engine for Gen-Z",
    description: "Save like a boss. 3D liquid vaults, automatic round-ups, impulse buy locks, and AI-driven leak detection.",
    canonical: "https://savemoneymanually.web.app/",
    robots: "index, follow",
  },
  [ROUTES.DASHBOARD]: {
    id: "page-dashboard",
    authRequired: true,
    title: "Dashboard | Vault.fi",
    description: "Central financial command center with real-time net savings and dynamic streak tracking.",
    canonical: "https://savemoneymanually.web.app/app/dashboard",
    robots: "noindex, nofollow",
  },
  [ROUTES.VAULTS]: {
    id: "page-vaults",
    authRequired: true,
    title: "Smart 3D Vaults Manager | Vault.fi",
    description: "Frosted glass 3D liquid vaults with dynamic wave progress and instant deposit controllers.",
    canonical: "https://savemoneymanually.web.app/app/vaults",
    robots: "noindex, nofollow",
  },
  [ROUTES.COOLDOWN]: {
    id: "page-cooldown",
    authRequired: true,
    title: "Impulse Buy Cooldown Chamber | Vault.fi",
    description: "Cost in life-hours calculator and countdown safe box to defeat emotional spending.",
    canonical: "https://savemoneymanually.web.app/app/cooldown",
    robots: "noindex, nofollow",
  },
  [ROUTES.INSIGHTS]: {
    id: "page-insights",
    authRequired: true,
    title: "AI Insights & Leakage Audit | Vault.fi",
    description: "Witty, blunt Gen-Z feedback identifying unused subscriptions and weekend spikes.",
    canonical: "https://savemoneymanually.web.app/app/insights",
    robots: "noindex, nofollow",
  },
  [ROUTES.SETTINGS]: {
    id: "page-settings",
    authRequired: true,
    title: "User Settings & Profile | Vault.fi",
    description: "Manage monthly income, calculate hourly wage, and toggle round-up multipliers.",
    canonical: "https://savemoneymanually.web.app/app/settings",
    robots: "noindex, nofollow",
  },
};

class Router {
  constructor() {
    this.currentPath = null;
    this.routeListeners = [];
    this.init();
  }

  init() {
    // Listen for browser navigation
    window.addEventListener("hashchange", () => this.handleNavigation());
    window.addEventListener("popstate", () => this.handleNavigation());

    // Intercept clicks on links with data-route
    document.addEventListener("click", (e) => {
      const link = e.target.closest("a[data-route], button[data-route]");
      if (link) {
        e.preventDefault();
        const path = link.getAttribute("data-route");
        this.navigate(path);
      }
    });

    // Listen for auth state changes to protect routes
    onAuth((user) => {
      const path = this.normalizePath(window.location.hash || window.location.pathname);
      const config = ROUTE_CONFIG[path];
      if (config && config.authRequired && !user) {
        this.navigate(ROUTES.LANDING);
      } else if (user && path === ROUTES.LANDING && window.location.hash.includes("app")) {
        // preserve intent
        this.navigate(path);
      }
    });

    // Initial navigation
    setTimeout(() => this.handleNavigation(), 0);
  }

  normalizePath(raw) {
    let clean = raw || "/";
    if (clean.startsWith("#")) clean = clean.slice(1);
    if (!clean.startsWith("/")) clean = "/" + clean;
    if (clean.endsWith("/") && clean.length > 1) clean = clean.slice(0, -1);
    return ROUTE_CONFIG[clean] ? clean : ROUTES.LANDING;
  }

  navigate(path) {
    const cleanPath = this.normalizePath(path);
    const targetHash = "#" + cleanPath;
    if (window.location.hash !== targetHash) {
      window.location.hash = targetHash;
    } else {
      this.handleNavigation();
    }
  }

  handleNavigation() {
    const raw = window.location.hash.replace(/^#/, "") || window.location.pathname;
    let path = this.normalizePath(raw);
    const config = ROUTE_CONFIG[path];

    // Auth Route Guard
    const user = getActiveUser();
    if (config.authRequired && !user) {
      console.warn("[Router] Route guard: User not authenticated, redirecting to landing.");
      window.location.hash = "#" + ROUTES.LANDING;
      // Trigger login prompt modal
      window.dispatchEvent(new CustomEvent("vaultfi:require-auth", { detail: { attemptedPath: path } }));
      path = ROUTES.LANDING;
    }

    this.currentPath = path;
    this.updateSEO(ROUTE_CONFIG[path]);
    this.renderView(path);
    this.updateActiveNavLinks(path);

    // Notify listeners
    this.routeListeners.forEach((fn) => fn(path, user));
  }

  updateSEO(meta) {
    if (!meta) return;
    document.title = meta.title;

    // Meta description
    let descTag = document.querySelector('meta[name="description"]');
    if (!descTag) {
      descTag = document.createElement("meta");
      descTag.name = "description";
      document.head.appendChild(descTag);
    }
    descTag.content = meta.description;

    // Robots
    let robotsTag = document.querySelector('meta[name="robots"]');
    if (!robotsTag) {
      robotsTag = document.createElement("meta");
      robotsTag.name = "robots";
      document.head.appendChild(robotsTag);
    }
    robotsTag.content = meta.robots;

    // Canonical
    let canonicalTag = document.querySelector('link[rel="canonical"]');
    if (!canonicalTag) {
      canonicalTag = document.createElement("link");
      canonicalTag.rel = "canonical";
      document.head.appendChild(canonicalTag);
    }
    canonicalTag.href = meta.canonical;
  }

  renderView(path) {
    const targetConfig = ROUTE_CONFIG[path];
    if (!targetConfig) return;

    // Toggle app shell vs public landing view
    const isApp = path.startsWith("/app");
    const appShell = document.getElementById("app-shell");
    const landingView = document.getElementById("page-landing");

    if (isApp) {
      if (appShell) appShell.style.display = "flex";
      if (landingView) landingView.style.display = "none";
    } else {
      if (appShell) appShell.style.display = "none";
      if (landingView) landingView.style.display = "block";
    }

    // Hide all page containers
    document.querySelectorAll(".page-view").forEach((view) => {
      view.classList.remove("active");
      view.style.display = "none";
    });

    // Show active page container
    const activePage = document.getElementById(targetConfig.id);
    if (activePage) {
      activePage.style.display = "block";
      // Force repaint for transition
      setTimeout(() => {
        activePage.classList.add("active");
      }, 20);
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  updateActiveNavLinks(path) {
    document.querySelectorAll("[data-route]").forEach((el) => {
      const route = el.getAttribute("data-route");
      if (route === path) {
        el.classList.add("active");
      } else {
        el.classList.remove("active");
      }
    });
  }

  onRouteChange(callback) {
    this.routeListeners.push(callback);
  }
}

export const router = new Router();
