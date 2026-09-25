// ============================================================
// VAULT.FI — MODERN SILICON VALLEY FINTECH CONTROLLER
// Clean, friendly, high-converting UX (Stripe / Linear / Revolut standard)
// ============================================================

import { router, ROUTES } from "./router.js";
import {
  signInWithGoogle,
  signInAsDemoUser,
  logOut,
  onAuth,
} from "./auth.js";
import {
  subscribeUserProfile,
  updateUserProfile,
  subscribeVaults,
  createVault,
  depositToVault,
  withdrawFromVault,
  subscribeTransactions,
  createTransaction,
  subscribeInsights,
  dismissInsight,
  cutExpenseAndAddToVault,
  subscribeCooldowns,
  createCooldown,
  resolveCooldown,
} from "./firestore.js";
import { createVaultCardHTML } from "./vault-engine.js";
import {
  formatCurrency,
  calcProgress,
  showToast,
  openModal,
  closeModal,
  getInitials,
} from "./utils.js";

// Global App State
let currentUser = null;
let userProfile = null;
let vaultsList = [];
let transactionsList = [];
let insightsList = [];
let cooldownsList = [];

// Subscriptions handles
let unsubProfile = null;
let unsubVaults = null;
let unsubTransactions = null;
let unsubInsights = null;
let unsubCooldowns = null;

// ============================================================
// INITIALIZATION
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
  initGlobalAuthHandlers();
  initLandingPageFeatures();
  initModals();
  initSettingsForm();
  initCooldownFeatures();
  initQuickActions();

  // Listen for Auth Changes
  onAuth((user) => {
    currentUser = user;
    if (user) {
      setupUserSession(user);
    } else {
      teardownUserSession();
    }
  });

  // Router view transitions
  router.onRouteChange((path) => {
    if (path.startsWith("/app")) {
      renderActiveView(path);
    }
  });
});

// ============================================================
// AUTH & SESSION MANAGEMENT
// ============================================================
function initGlobalAuthHandlers() {
  document.querySelectorAll(".btn-google-auth").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        btn.classList.add("opacity-75");
        await signInWithGoogle();
        showToast("Signed in with Google! Welcome to Vault.fi.", "success");
        closeModal("auth-modal");
        router.navigate(ROUTES.DASHBOARD);
      } catch (err) {
        showToast(err.message || "Failed to sign in with Google.", "error");
      } finally {
        btn.classList.remove("opacity-75");
      }
    });
  });

  document.querySelectorAll(".btn-demo-auth").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        await signInAsDemoUser();
        showToast("Demo mode active. Welcome to Vault.fi!", "success");
        closeModal("auth-modal");
        router.navigate(ROUTES.DASHBOARD);
      } catch (err) {
        showToast("Demo sign in failed.", "error");
      }
    });
  });

  document.querySelectorAll(".btn-logout").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await logOut();
      showToast("Signed out successfully.", "info");
      router.navigate(ROUTES.LANDING);
    });
  });

  window.addEventListener("vaultfi:require-auth", () => {
    openModal("auth-modal");
    showToast("Please sign in to access your dashboard.", "info");
  });
}

function setupUserSession(user) {
  updateUserHeader(user);
  const uid = user.uid;

  if (unsubProfile) unsubProfile();
  unsubProfile = subscribeUserProfile(uid, (profile) => {
    userProfile = profile;
    updateUserProfileUI(profile);
  });

  if (unsubVaults) unsubVaults();
  unsubVaults = subscribeVaults(uid, (vaults) => {
    vaultsList = vaults;
    renderVaults();
    renderDashboardVaults();
    populateVaultDropdowns();
  });

  if (unsubTransactions) unsubTransactions();
  unsubTransactions = subscribeTransactions(uid, (txs) => {
    transactionsList = txs;
    renderRecentTransactions();
  });

  if (unsubInsights) unsubInsights();
  unsubInsights = subscribeInsights(uid, (insights) => {
    insightsList = insights;
    renderInsights();
    renderDashboardInsightBanner();
  });

  if (unsubCooldowns) unsubCooldowns();
  unsubCooldowns = subscribeCooldowns(uid, (cooldowns) => {
    cooldownsList = cooldowns;
    renderCooldowns();
  });
}

function teardownUserSession() {
  if (unsubProfile) { unsubProfile(); unsubProfile = null; }
  if (unsubVaults) { unsubVaults(); unsubVaults = null; }
  if (unsubTransactions) { unsubTransactions(); unsubTransactions = null; }
  if (unsubInsights) { unsubInsights(); unsubInsights = null; }
  if (unsubCooldowns) { unsubCooldowns(); unsubCooldowns = null; }
  userProfile = null;
  vaultsList = [];
  transactionsList = [];
  insightsList = [];
  cooldownsList = [];
}

function updateUserHeader(user) {
  const name = user.displayName || user.email?.split("@")[0] || "Saver";
  const email = user.email || "user@vault.fi";

  const greetingEl = document.getElementById("user-greeting");
  if (greetingEl) {
    greetingEl.innerHTML = `Welcome back, <span style="color: #2563EB;">${name}</span> 👋`;
  }

  const sbName = document.getElementById("sidebar-name");
  const sbEmail = document.getElementById("sidebar-email");
  const sbAvatar = document.getElementById("sidebar-avatar");
  const topAvatar = document.getElementById("topbar-avatar");

  if (sbName) sbName.textContent = name;
  if (sbEmail) sbEmail.textContent = email;

  const initials = getInitials(name);
  if (sbAvatar) sbAvatar.textContent = initials;
  if (topAvatar) topAvatar.textContent = initials;
}

function updateUserProfileUI(profile) {
  if (!profile) return;

  // Streak counter
  const streakEl = document.getElementById("streak-count");
  if (streakEl) {
    streakEl.textContent = `${profile.streakCount || 7} Day Streak`;
  }

  // Net Savings Metric with smooth count animation
  const netSavedEl = document.getElementById("total-saved-metric");
  if (netSavedEl) {
    netSavedEl.textContent = formatCurrency(profile.totalSaved || 0);
  }

  // Hourly wage badge
  const hourlyBadge = document.getElementById("sidebar-hourly-wage");
  if (hourlyBadge) {
    hourlyBadge.textContent = `₹${Math.round(profile.hourlyWage || 520)}/hr`;
  }

  // Settings
  const incomeInput = document.getElementById("setting-monthly-income");
  const wageDisplay = document.getElementById("setting-calculated-wage");
  const multiplierInputs = document.querySelectorAll('input[name="roundup-multiplier"]');

  if (incomeInput && document.activeElement !== incomeInput) {
    incomeInput.value = profile.monthlyIncome || 90000;
  }
  if (wageDisplay) {
    wageDisplay.textContent = `₹${Math.round(profile.hourlyWage || 520)} / hr`;
  }
  if (multiplierInputs) {
    multiplierInputs.forEach((radio) => {
      radio.checked = Number(radio.value) === Number(profile.roundUpMultiplier || 50);
    });
  }
}

// ============================================================
// PAGE 1: PUBLIC LANDING PAGE (/)
// ============================================================
function initLandingPageFeatures() {
  // Hero Interactive Vault Card Preview
  const heroProgress = document.getElementById("hero-vault-progress");
  const heroPct = document.getElementById("hero-vault-pct");
  const heroSaved = document.getElementById("hero-vault-saved");
  let heroCurrentAmount = 122400;
  const heroTargetAmount = 180000;

  function updateHeroPreview(newAmount) {
    heroCurrentAmount = Math.max(0, Math.min(heroTargetAmount, newAmount));
    const pct = calcProgress(heroCurrentAmount, heroTargetAmount);
    if (heroProgress) heroProgress.style.width = `${pct}%`;
    if (heroPct) heroPct.textContent = `${pct}%`;
    if (heroSaved) heroSaved.textContent = formatCurrency(heroCurrentAmount);
  }

  document.querySelectorAll(".btn-hero-add").forEach((btn) => {
    btn.addEventListener("click", () => {
      const add = Number(btn.getAttribute("data-add")) || 5000;
      updateHeroPreview(heroCurrentAmount + add);
    });
  });

  document.getElementById("btn-hero-reset")?.addEventListener("click", () => {
    updateHeroPreview(60000);
  });

  // Interactive Round-Up Demo Slider
  const slider = document.getElementById("roundup-demo-slider");
  const sliderValEl = document.getElementById("roundup-slider-val");
  const monthlySaveEl = document.getElementById("roundup-monthly-save");
  const annualSaveEl = document.getElementById("roundup-annual-save");
  const apySaveEl = document.getElementById("roundup-apy-save");
  const milestoneEl = document.getElementById("roundup-milestone-text");
  const sliderProgress = document.getElementById("roundup-slider-progress");

  function updateRoundUpDemo() {
    if (!slider) return;
    const roundUpAmount = Number(slider.value) || 50;
    if (sliderValEl) sliderValEl.textContent = `₹${roundUpAmount}`;

    const avgSpareChange = Math.round(roundUpAmount * 0.45);
    const monthlySaved = avgSpareChange * 45;
    const annualBase = monthlySaved * 12;
    const apyGrowth = Math.round(annualBase * 1.082);

    if (monthlySaveEl) monthlySaveEl.textContent = formatCurrency(monthlySaved);
    if (annualSaveEl) annualSaveEl.textContent = formatCurrency(annualBase);
    if (apySaveEl) apySaveEl.textContent = formatCurrency(apyGrowth);

    const pct = Math.min(100, Math.round((roundUpAmount / 500) * 100));
    if (sliderProgress) sliderProgress.style.width = `${pct}%`;

    if (milestoneEl) {
      if (roundUpAmount <= 30) {
        milestoneEl.textContent = "🎧 Unlocks: AirPods Pro 2 + 1 Year of Spotify Premium";
      } else if (roundUpAmount <= 80) {
        milestoneEl.textContent = "🏖️ Unlocks: 5-Day Goa beach vacation with zero guilt";
      } else if (roundUpAmount <= 200) {
        milestoneEl.textContent = "💻 Unlocks: Flagship MacBook Air or iPhone 16 Pro in cash";
      } else {
        milestoneEl.textContent = "🚀 Unlocks: Solo international relocation or motorcycle downpayment!";
      }
    }
  }

  if (slider) {
    slider.addEventListener("input", updateRoundUpDemo);
    updateRoundUpDemo();
  }
}

// ============================================================
// PAGE 2: USER DASHBOARD (/app/dashboard)
// ============================================================
function renderDashboardVaults() {
  const container = document.getElementById("dashboard-vaults-carousel");
  if (!container) return;

  const activeVaults = vaultsList.slice(0, 3);
  if (activeVaults.length === 0) {
    container.innerHTML = `
      <div class="stripe-card" style="grid-column: 1 / -1; padding: 3rem 2rem; text-align: center;">
        <h3 style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin-bottom: 0.5rem;">No active vaults yet</h3>
        <p style="color: #64748B; max-width: 440px; margin: 0 auto 1.5rem; font-size: 0.95rem;">
          Create your first goal vault to start stashing cash automatically and track progress in real time.
        </p>
        <button class="btn-primary-blue" onclick="window.dispatchEvent(new CustomEvent('vaultfi:open-create-vault'))">
          + Create Your First Vault
        </button>
      </div>
    `;
    return;
  }

  container.innerHTML = activeVaults.map((vault) => createVaultCardHTML(vault)).join("");
  attachVaultCardListeners(container);
}

function renderDashboardInsightBanner() {
  const bannerContainer = document.getElementById("dashboard-ai-banner");
  if (!bannerContainer) return;

  const urgent = insightsList.find((i) => i.severity === "CRITICAL") || insightsList[0];
  if (!urgent) {
    bannerContainer.style.display = "none";
    return;
  }

  const isCrit = urgent.severity === "CRITICAL";

  bannerContainer.style.display = "block";
  bannerContainer.innerHTML = `
    <div class="stripe-card" style="border-left: 4px solid ${isCrit ? '#EF4444' : '#2563EB'}; padding: 1.25rem 1.75rem; display: flex; justify-content: space-between; align-items: center; gap: 1.5rem; flex-wrap: wrap;">
      <div>
        <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: ${isCrit ? '#EF4444' : '#2563EB'}; margin-bottom: 0.25rem;">
          ${isCrit ? '⚠️ Spending Leak Detected' : '💡 Financial Suggestion'}
        </div>
        <p style="font-weight: 600; font-size: 0.95rem; color: #0F172A; margin: 0;">
          "${urgent.message}"
        </p>
      </div>
      <div style="display: flex; gap: 0.75rem; align-items: center;">
        <button class="btn-primary-blue" data-route="/app/insights" style="padding: 0.5rem 1rem; font-size: 0.85rem;">
          Review Spending
        </button>
        <button class="btn-secondary-white btn-dismiss-insight" data-id="${urgent.insightId || urgent.id}" style="padding: 0.5rem 0.85rem; font-size: 0.85rem;">
          Dismiss
        </button>
      </div>
    </div>
  `;

  bannerContainer.querySelector(".btn-dismiss-insight")?.addEventListener("click", async (e) => {
    const id = e.currentTarget.getAttribute("data-id");
    if (currentUser) await dismissInsight(currentUser.uid, id);
    showToast("Alert dismissed.", "info");
  });
}

function renderRecentTransactions() {
  const list = document.getElementById("recent-transactions-list");
  if (!list) return;

  if (transactionsList.length === 0) {
    list.innerHTML = `<div style="padding: 2.5rem; text-align: center; color: #64748B;">No recent transactions recorded.</div>`;
    return;
  }

  list.innerHTML = `
    <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
      <thead>
        <tr style="border-bottom: 1px solid #E2E8F0; color: #64748B; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;">
          <th style="padding: 0.85rem 1.25rem; font-weight: 600;">Transaction</th>
          <th style="padding: 0.85rem 1.25rem; font-weight: 600;">Category</th>
          <th style="padding: 0.85rem 1.25rem; font-weight: 600; text-align: right;">Amount</th>
        </tr>
      </thead>
      <tbody>
        ${transactionsList.slice(0, 6).map((tx) => {
          const isExpense = tx.type === "EXPENSE";
          const sign = isExpense ? "- " : "+ ";
          const color = isExpense ? "#EF4444" : "#2563EB";

          return `
            <tr style="border-bottom: 1px solid #F1F5F9; transition: background-color 0.15s ease;">
              <td style="padding: 1rem 1.25rem;">
                <div style="font-weight: 600; color: #0F172A;">${tx.note || "General Transaction"}</div>
                ${tx.roundUpAmount > 0 ? `<div style="font-size: 0.75rem; color: #2563EB; font-weight: 600;">+₹${tx.roundUpAmount} round-up saved</div>` : ''}
              </td>
              <td style="padding: 1rem 1.25rem; color: #64748B;">
                ${tx.category || "General"}
              </td>
              <td style="padding: 1rem 1.25rem; text-align: right; font-weight: 700; color: ${color};">
                ${sign}${formatCurrency(tx.amount)}
              </td>
            </tr>
          `;
        }).join("")}
      </tbody>
    </table>
  `;
}

// ============================================================
// PAGE 3: SMART 3D VAULTS MANAGER (/app/vaults)
// ============================================================
function renderVaults() {
  const grid = document.getElementById("vaults-grid");
  if (!grid) return;

  if (vaultsList.length === 0) {
    grid.innerHTML = `
      <div class="stripe-card" style="grid-column: 1 / -1; padding: 3.5rem 2rem; text-align: center;">
        <h3 style="font-size: 1.35rem; font-weight: 700; color: #0F172A; margin-bottom: 0.5rem;">No Vaults Active</h3>
        <p style="color: #64748B; max-width: 460px; margin: 0 auto 1.5rem; font-size: 0.95rem;">
          Create a targeted savings vault for your next gadget, vacation, or emergency safety cushion.
        </p>
        <button class="btn-primary-blue" onclick="window.dispatchEvent(new CustomEvent('vaultfi:open-create-vault'))">
          + Create New Vault
        </button>
      </div>
    `;
    return;
  }

  grid.innerHTML = vaultsList.map((v) => createVaultCardHTML(v)).join("");
  attachVaultCardListeners(grid);
}

function attachVaultCardListeners(container) {
  container.querySelectorAll(".btn-deposit-trigger").forEach((btn) => {
    btn.addEventListener("click", () => {
      const vaultId = btn.getAttribute("data-vault-id");
      const title = btn.getAttribute("data-vault-title");
      openDepositModal(vaultId, title);
    });
  });

  container.querySelectorAll(".btn-withdraw-trigger").forEach((btn) => {
    btn.addEventListener("click", () => {
      const vaultId = btn.getAttribute("data-vault-id");
      const title = btn.getAttribute("data-vault-title");
      const max = btn.getAttribute("data-max");
      openWithdrawModal(vaultId, title, max);
    });
  });
}

// ============================================================
// PAGE 4: IMPULSE BUY COOLDOWN CHAMBER (/app/cooldown)
// ============================================================
function initCooldownFeatures() {
  const itemInput = document.getElementById("cooldown-item-name");
  const priceInput = document.getElementById("cooldown-item-price");
  const hoursResult = document.getElementById("cooldown-work-hours-result");
  const wageNote = document.getElementById("cooldown-wage-note");
  const shockText = document.getElementById("cooldown-shock-text");

  function calculateLifeHours() {
    if (!priceInput || !hoursResult) return;
    const price = Number(priceInput.value) || 0;
    const hourlyWage = userProfile?.hourlyWage || 520;

    const workHours = (price / hourlyWage).toFixed(1);
    hoursResult.textContent = `${workHours} Work Hours`;

    if (wageNote) {
      wageNote.textContent = `Based on your calculated wage of ₹${Math.round(hourlyWage)}/hr`;
    }

    if (shockText) {
      const workDays = (workHours / 8).toFixed(1);
      if (price <= 0) {
        shockText.textContent = "Enter an item price to see how many hours of work it costs.";
      } else {
        shockText.textContent = `That's about ${workHours} hours (${workDays} full working days) of your life! Is this purchase worth ${workDays} days of labor?`;
      }
    }
  }

  priceInput?.addEventListener("input", calculateLifeHours);
  itemInput?.addEventListener("input", calculateLifeHours);

  const form = document.getElementById("cooldown-form");
  form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!currentUser) return;

    const itemName = itemInput.value.trim() || "Item";
    const itemPrice = Number(priceInput.value) || 0;
    const duration = Number(document.querySelector('input[name="cooldown-duration"]:checked')?.value) || 24;
    const hourlyWage = userProfile?.hourlyWage || 520;
    const workHours = Number((itemPrice / hourlyWage).toFixed(1));

    if (itemPrice <= 0) {
      showToast("Please enter a valid price.", "error");
      return;
    }

    try {
      await createCooldown(currentUser.uid, {
        itemName,
        itemPrice,
        workHours,
        durationHours: duration,
      });

      showToast(`Locked ${itemName} in cooldown for ${duration} hours! 🔒`, "success");
      form.reset();
      calculateLifeHours();
    } catch (err) {
      showToast("Could not lock item in cooldown.", "error");
    }
  });

  setInterval(tickCooldownTimers, 1000);
}

function renderCooldowns() {
  const container = document.getElementById("cooldown-active-list");
  if (!container) return;

  const active = cooldownsList.filter((c) => c.status === "ACTIVE" || c.status === "EXPIRED");

  if (active.length === 0) {
    container.innerHTML = `
      <div class="stripe-card" style="text-align: center; padding: 2.5rem; color: #64748B;">
        No items currently in cooldown. Your spending impulses are under control!
      </div>
    `;
    return;
  }

  container.innerHTML = active.map((c) => {
    const isExpired = new Date(c.lockedUntil) <= new Date() || c.status === "EXPIRED";

    return `
      <div class="stripe-card" style="padding: 1.5rem; margin-bottom: 1rem; border-left: 4px solid ${isExpired ? '#10B981' : '#2563EB'};" id="card-${c.cooldownId || c.id}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
          <div>
            <span style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: ${isExpired ? '#10B981' : '#2563EB'};">
              ${isExpired ? '✓ Cooldown Expired — Time to Decide' : '🔒 Cooldown Active'}
            </span>
            <h3 style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin: 0.25rem 0 0.5rem;">${c.itemName}</h3>
            <div style="color: #64748B; font-size: 0.9rem;">
              Price: <strong style="color: #0F172A;">${formatCurrency(c.itemPrice)}</strong> • <strong>${c.workHours} Work Hours</strong>
            </div>
          </div>

          <div style="text-align: right;">
            <div class="timer-countdown-badge" data-until="${c.lockedUntil}" style="font-size: 1.5rem; font-weight: 800; color: ${isExpired ? '#10B981' : '#2563EB'};">
              ${isExpired ? "00:00:00" : "Counting down..."}
            </div>
            <div style="font-size: 0.8rem; color: #64748B;">${c.durationHours}h Cooldown</div>
          </div>
        </div>

        ${isExpired ? `
          <div style="margin-top: 1.25rem; padding-top: 1rem; border-top: 1px solid #E2E8F0;">
            <p style="font-size: 0.9rem; font-weight: 600; color: #0F172A; margin-bottom: 0.75rem;">
              The impulse haze has cleared! What would you like to do?
            </p>
            <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
              <button class="btn-primary-blue btn-cooldown-send-vault" data-id="${c.cooldownId || c.id}" data-price="${c.itemPrice}">
                Send ₹${c.itemPrice.toLocaleString("en-IN")} to Vault
              </button>
              <button class="btn-secondary-white btn-cooldown-walk-away" data-id="${c.cooldownId || c.id}">
                Walk Away (Save Money)
              </button>
              <button class="btn-secondary-white btn-cooldown-buy-now" data-id="${c.cooldownId || c.id}" data-item="${c.itemName}" data-price="${c.itemPrice}" style="color: #EF4444;">
                Buy It Now
              </button>
            </div>
          </div>
        ` : `
          <div style="margin-top: 1rem; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.85rem; color: #64748B;">Money is locked. Sleep on it before buying!</span>
            <button class="btn-secondary-white btn-cooldown-unlock-test" data-id="${c.cooldownId || c.id}" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;">
              Test Expire Now
            </button>
          </div>
        `}
      </div>
    `;
  }).join("");

  attachCooldownActionListeners(container);
}

function attachCooldownActionListeners(container) {
  container.querySelectorAll(".btn-cooldown-send-vault").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const cid = btn.getAttribute("data-id");
      const price = Number(btn.getAttribute("data-price"));
      if (!currentUser) return;

      const targetVault = vaultsList[0];
      if (targetVault) {
        await depositToVault(currentUser.uid, targetVault.vaultId || targetVault.id, price, "Saved from Impulse Cooldown");
      } else {
        await updateUserProfile(currentUser.uid, { totalSaved: (userProfile?.totalSaved || 0) + price });
      }

      await resolveCooldown(currentUser.uid, cid, "SAVED");
      showToast(`Stashed ₹${price.toLocaleString("en-IN")} into your savings vault!`, "success");
    });
  });

  container.querySelectorAll(".btn-cooldown-walk-away").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const cid = btn.getAttribute("data-id");
      if (!currentUser) return;
      await resolveCooldown(currentUser.uid, cid, "CANCELLED");
      showToast("Walked away from impulse buy. Money saved!", "info");
    });
  });

  container.querySelectorAll(".btn-cooldown-buy-now").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const cid = btn.getAttribute("data-id");
      const item = btn.getAttribute("data-item");
      const price = Number(btn.getAttribute("data-price"));
      if (!currentUser) return;
      await createTransaction(currentUser.uid, {
        amount: price,
        type: "EXPENSE",
        category: "SHOPPING",
        note: `Conscious Purchase: ${item}`,
      });
      await resolveCooldown(currentUser.uid, cid, "BOUGHT");
      showToast(`Logged conscious expense of ₹${price.toLocaleString("en-IN")}.`, "info");
    });
  });

  container.querySelectorAll(".btn-cooldown-unlock-test").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const cid = btn.getAttribute("data-id");
      if (!currentUser) return;
      await resolveCooldown(currentUser.uid, cid, "EXPIRED");
      renderCooldowns();
    });
  });
}

function tickCooldownTimers() {
  document.querySelectorAll(".timer-countdown-badge").forEach((badge) => {
    const until = new Date(badge.getAttribute("data-until"));
    const now = new Date();
    const diff = until - now;

    if (diff <= 0) {
      badge.textContent = "00:00:00";
    } else {
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const mins = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const secs = Math.floor((diff % (1000 * 60)) / 1000);
      badge.textContent = `${String(hours).padStart(2, "0")}:${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
    }
  });
}

// ============================================================
// PAGE 5: AI INSIGHTS & LEAKAGE AUDIT (/app/insights)
// ============================================================
function renderInsights() {
  const container = document.getElementById("insights-feed-list");
  if (!container) return;

  if (insightsList.length === 0) {
    container.innerHTML = `
      <div class="stripe-card" style="text-align: center; padding: 3rem;">
        <h3 style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin-bottom: 0.5rem;">Zero Spending Leaks</h3>
        <p style="color: #64748B;">Your financial discipline is spotless. No wasteful subscriptions detected.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = insightsList.map((item) => {
    const isCrit = item.severity === "CRITICAL";
    return `
      <div class="stripe-card" style="padding: 1.5rem; margin-bottom: 1rem; border-left: 4px solid ${isCrit ? '#EF4444' : '#2563EB'};" id="insight-${item.insightId || item.id}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1.5rem; flex-wrap: wrap;">
          <div>
            <div style="font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: ${isCrit ? '#EF4444' : '#2563EB'}; margin-bottom: 0.25rem;">
              ${item.severity} Alert
            </div>
            <h4 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 0 0 0.4rem;">${item.title}</h4>
            <p style="color: #64748B; font-size: 0.95rem; line-height: 1.5; margin: 0;">
              "${item.message}"
            </p>
          </div>

          <div style="display: flex; gap: 0.5rem; align-items: center;">
            <button class="btn-primary-blue btn-cut-expense" data-id="${item.insightId || item.id}">
              Cut This Expense
            </button>
            <button class="btn-secondary-white btn-snooze-insight" data-id="${item.insightId || item.id}">
              Snooze
            </button>
          </div>
        </div>
      </div>
    `;
  }).join("");

  attachInsightsActionListeners(container);
}

function attachInsightsActionListeners(container) {
  container.querySelectorAll(".btn-cut-expense").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = btn.getAttribute("data-id");
      if (!currentUser) return;

      const targetVault = vaultsList[0];
      const targetVaultId = targetVault ? (targetVault.vaultId || targetVault.id) : null;

      await cutExpenseAndAddToVault(currentUser.uid, id, 1200, targetVaultId);
      showToast("Subscription cut! Saved ₹1,200 transferred to your vault.", "success");
    });
  });

  container.querySelectorAll(".btn-snooze-insight").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = btn.getAttribute("data-id");
      if (!currentUser) return;
      await dismissInsight(currentUser.uid, id);
      showToast("Alert snoozed for 7 days.", "info");
    });
  });
}

// ============================================================
// PAGE 6: USER SETTINGS & PROFILE (/app/settings)
// ============================================================
function initSettingsForm() {
  const incomeInput = document.getElementById("setting-monthly-income");
  const hoursSlider = document.getElementById("setting-weekly-hours");
  const hoursDisplay = document.getElementById("setting-weekly-hours-val");
  const calculatedWageEl = document.getElementById("setting-calculated-wage");

  function recalculateWage() {
    const income = Number(incomeInput?.value) || 90000;
    const weeklyHours = Number(hoursSlider?.value) || 40;
    if (hoursDisplay) hoursDisplay.textContent = `${weeklyHours} hrs / week`;

    const monthlyHours = weeklyHours * 4.333;
    const hourlyWage = Math.round(income / monthlyHours);

    if (calculatedWageEl) {
      calculatedWageEl.textContent = `₹${hourlyWage.toLocaleString("en-IN")} / hr`;
    }
    return hourlyWage;
  }

  incomeInput?.addEventListener("input", recalculateWage);
  hoursSlider?.addEventListener("input", recalculateWage);

  document.getElementById("btn-save-settings")?.addEventListener("click", async () => {
    if (!currentUser) return;

    const monthlyIncome = Number(incomeInput?.value) || 90000;
    const hourlyWage = recalculateWage();
    const roundUpMultiplier = Number(document.querySelector('input[name="roundup-multiplier"]:checked')?.value) || 50;

    try {
      await updateUserProfile(currentUser.uid, {
        monthlyIncome,
        hourlyWage,
        roundUpMultiplier,
      });
      showToast("Settings updated successfully.", "success");
    } catch (err) {
      showToast("Failed to save settings.", "error");
    }
  });

  document.getElementById("btn-reset-demo-data")?.addEventListener("click", async () => {
    if (!currentUser) return;
    if (confirm("Reset demo data to initial baseline state?")) {
      await signInAsDemoUser();
      showToast("Demo data reset.", "success");
      location.reload();
    }
  });
}

// ============================================================
// QUICK ACTIONS & MODALS
// ============================================================
function initQuickActions() {
  const hamburger = document.getElementById("hamburger-btn");
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebar-overlay");

  hamburger?.addEventListener("click", () => {
    sidebar?.classList.toggle("open");
    overlay?.classList.toggle("hidden");
  });
  overlay?.addEventListener("click", () => {
    sidebar?.classList.remove("open");
    overlay?.classList.add("hidden");
  });

  document.getElementById("btn-quick-deposit")?.addEventListener("click", () => openDepositModal());
  document.getElementById("btn-quick-expense")?.addEventListener("click", () => openModal("log-expense-modal"));
  document.getElementById("btn-quick-new-vault")?.addEventListener("click", () => openModal("create-vault-modal"));

  window.addEventListener("vaultfi:open-create-vault", () => openModal("create-vault-modal"));
}

function initModals() {
  document.querySelectorAll(".modal-close, .modal-cancel").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const modal = e.target.closest(".modal-overlay");
      if (modal) closeModal(modal.id);
    });
  });

  const createForm = document.getElementById("create-vault-form");
  createForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!currentUser) return;

    const title = document.getElementById("vault-input-title").value.trim();
    const targetAmount = Number(document.getElementById("vault-input-target").value) || 10000;
    const deadline = document.getElementById("vault-input-deadline").value;
    const category = document.getElementById("vault-input-category").value;

    try {
      await createVault(currentUser.uid, {
        title,
        targetAmount,
        deadline,
        category,
        color: "#2563EB",
        currentAmount: 0,
        isLocked: false,
      });

      showToast(`Savings vault "${title}" created!`, "success");
      closeModal("create-vault-modal");
      createForm.reset();
    } catch (err) {
      showToast("Could not create vault.", "error");
    }
  });

  const depositForm = document.getElementById("deposit-form");
  depositForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!currentUser) return;

    const vaultId = document.getElementById("deposit-vault-select").value;
    const amount = Number(document.getElementById("deposit-amount-input").value) || 0;
    const note = document.getElementById("deposit-note-input").value.trim() || "Vault Deposit";

    if (amount <= 0) {
      showToast("Please enter a valid deposit amount.", "error");
      return;
    }

    try {
      await depositToVault(currentUser.uid, vaultId, amount, note);
      showToast(`Deposited ₹${amount.toLocaleString("en-IN")} into vault!`, "success");
      closeModal("deposit-modal");
      depositForm.reset();
    } catch (err) {
      showToast("Deposit could not be processed.", "error");
    }
  });

  const expenseForm = document.getElementById("log-expense-form");
  const expenseAmountInput = document.getElementById("expense-amount-input");
  const expenseRoundUpPreview = document.getElementById("expense-roundup-preview");

  function calculateExpenseRoundUp() {
    const amount = Number(expenseAmountInput?.value) || 0;
    const mult = Number(userProfile?.roundUpMultiplier || 50);
    const remainder = amount % mult;
    const roundUp = remainder === 0 ? 0 : mult - remainder;

    if (expenseRoundUpPreview) {
      expenseRoundUpPreview.textContent = `+₹${roundUp} spare change will be automatically saved to your vault!`;
    }
    return roundUp;
  }
  expenseAmountInput?.addEventListener("input", calculateExpenseRoundUp);

  expenseForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!currentUser) return;

    const amount = Number(expenseAmountInput.value) || 0;
    const note = document.getElementById("expense-note-input").value.trim() || "Daily Expense";
    const category = document.getElementById("expense-category-select").value;
    const roundUpAmount = calculateExpenseRoundUp();

    try {
      await createTransaction(currentUser.uid, {
        amount,
        type: "EXPENSE",
        category,
        roundUpAmount,
        note,
      });

      showToast(`Expense logged. +₹${roundUpAmount} spare change stashed!`, "success");
      closeModal("log-expense-modal");
      expenseForm.reset();
    } catch (err) {
      showToast("Failed to log expense.", "error");
    }
  });
}

function openDepositModal(targetVaultId = null, title = "") {
  populateVaultDropdowns(targetVaultId);
  const titleHint = document.getElementById("deposit-vault-name-hint");
  if (titleHint) titleHint.textContent = title ? `Depositing to: ${title}` : "Select target vault";
  openModal("deposit-modal");
}

function openWithdrawModal(vaultId, title, maxAmount) {
  const amountStr = prompt(`Withdraw funds from "${title}" (Available: ${formatCurrency(maxAmount)}):`, "1000");
  if (!amountStr) return;
  const num = Number(amountStr);
  if (num > 0 && num <= Number(maxAmount) && currentUser) {
    withdrawFromVault(currentUser.uid, vaultId, num, `Withdrawal from ${title}`)
      .then(() => showToast(`Withdrew ${formatCurrency(num)}.`, "info"))
      .catch(() => showToast("Withdrawal failed.", "error"));
  } else if (num > Number(maxAmount)) {
    showToast("Cannot withdraw more than current vault balance!", "error");
  }
}

function populateVaultDropdowns(selectedId = null) {
  const depositSelect = document.getElementById("deposit-vault-select");
  if (!depositSelect) return;

  depositSelect.innerHTML = vaultsList.map((v) => `
    <option value="${v.vaultId || v.id}" ${(v.vaultId === selectedId || v.id === selectedId) ? "selected" : ""}>
      ${v.title} (${formatCurrency(v.currentAmount || 0)} / ${formatCurrency(v.targetAmount || 0)})
    </option>
  `).join("");
}

function renderActiveView(path) {
  if (path === ROUTES.DASHBOARD) {
    renderDashboardVaults();
    renderDashboardInsightBanner();
    renderRecentTransactions();
  } else if (path === ROUTES.VAULTS) {
    renderVaults();
  } else if (path === ROUTES.COOLDOWN) {
    renderCooldowns();
  } else if (path === ROUTES.INSIGHTS) {
    renderInsights();
  }
}
