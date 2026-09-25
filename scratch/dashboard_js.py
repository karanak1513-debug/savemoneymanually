# -*- coding: utf-8 -*-
"""
Client-side JavaScript Module for SaveMoneyManually Dashboard
Optimized for LIGHTNING-FAST INSTANT REAL-TIME SAVES and zero-latency UI updates.
"""

DASHBOARD_JS = """
  <!-- ============================================================ -->
  <!-- APPLICATION LOGIC: DISSOLVE TRANSITION & DASHBOARD ACTIONS -->
  <!-- ============================================================ -->
  <script type="module">
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
    import {
      getAuth,
      GoogleAuthProvider,
      signInWithPopup,
      signOut,
      onAuthStateChanged
    } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
    import {
      getFirestore,
      collection,
      doc,
      addDoc,
      setDoc,
      updateDoc,
      deleteDoc,
      onSnapshot,
      query,
      orderBy,
      serverTimestamp
    } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

    // Firebase Configuration
    const firebaseConfig = {
      apiKey: "AIzaSyBDhpvyxivB2GVEhbHMlTVByGt5lxNR_As",
      authDomain: "savemoneymanually.firebaseapp.com",
      projectId: "savemoneymanually",
      storageBucket: "savemoneymanually.firebasestorage.app",
      messagingSenderId: "415442077873",
      appId: "1:415442077873:web:0cd96a3f5941c49268ba90",
      measurementId: "G-TFMH546K9F"
    };

    const app = initializeApp(firebaseConfig);
    const auth = getAuth(app);
    let db = null;
    try {
      db = getFirestore(app);
    } catch (e) {
      console.warn("Firestore init warning:", e);
    }
    const provider = new GoogleAuthProvider();

    // DOM Elements: Views
    const authView = document.getElementById('auth-view');
    const authCard = document.getElementById('auth-card');
    const dashboardView = document.getElementById('dashboard-view');

    // DOM Elements: Auth
    const btnGoogleAuth = document.getElementById('btn-google-auth');
    const btnAuthLabel = document.getElementById('btn-auth-label');
    const trailingArrow = document.getElementById('trailing-arrow');
    const btnAuthSpinner = document.getElementById('btn-auth-spinner');
    const btnDemoEnter = document.getElementById('btn-demo-enter');
    const authFeedback = document.getElementById('auth-feedback');

    // DOM Elements: Header & User
    const dashUserAvatar = document.getElementById('dash-user-avatar');
    const dashUserName = document.getElementById('dash-user-name');
    const btnDashSignout = document.getElementById('btn-dash-signout');

    // Application State
    let currentUser = null;
    let isDemoMode = false;
    let hourlyWageRate = 520;
    let goals = [];
    let ledger = [];
    let cooldowns = [];
    let currentCalDate = new Date();
    let selectedGoalCadence = 'DAILY';
    let ledgerFilter = 'ALL';

    // Unsubscribe handles
    let unsubGoals = null;
    let unsubLedger = null;

    // Toast helper
    function showToast(message, type = 'info') {
      const container = document.getElementById('toast-container');
      if (!container) return;
      const el = document.createElement('div');
      el.className = 'toast-msg';
      el.innerHTML = `<span>${type === 'success' ? '⚡' : type === 'error' ? '⚠️' : 'ℹ'}</span><span>${message}</span>`;
      container.appendChild(el);
      setTimeout(() => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(10px)';
        el.style.transition = 'all 0.25s ease';
        setTimeout(() => el.remove(), 250);
      }, 3000);
    }

    // ============================================================
    // ANTI-SPAM BUTTON DEBOUNCE LOCK UTILITY
    // ============================================================
    const SPIN_SVG = `<svg class="w-3.5 h-3.5 animate-spin flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>`;

    function lockBtn(btn, loadingLabel) {
      if (!btn) return;
      btn._originalHTML = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = `${SPIN_SVG} <span>${loadingLabel}</span>`;
    }

    function unlockBtn(btn) {
      if (!btn || !btn._originalHTML) return;
      btn.disabled = false;
      btn.innerHTML = btn._originalHTML;
      btn._originalHTML = null;
    }

    // ============================================================
    // LOCAL STORAGE RESILIENCE & DEFAULT SEED DATA
    // ============================================================
    const STORAGE_KEY = 'savemoneymanually_store_v2';

    function getLocalData() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : null;
      } catch (e) {
        return null;
      }
    }

    function saveLocalData(data) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
      } catch (e) {}
    }

    function getSeedState() {
      const now = new Date();
      const y = now.getFullYear();
      const m = String(now.getMonth() + 1).padStart(2, '0');
      const d = String(now.getDate()).padStart(2, '0');
      const todayStr = `${y}-${m}-${d}`;

      const d1 = `${y}-${m}-04`;
      const d2 = `${y}-${m}-08`;
      const d3 = `${y}-${m}-12`;
      const d4 = `${y}-${m}-15`;
      const d5 = `${y}-${m}-19`;
      const d6 = `${y}-${m}-22`;

      return {
        goals: [
          {
            id: 'goal-seed-1',
            name: 'Emergency Fortress',
            targetAmount: 200000,
            currentAmount: 52000,
            deadline: `${y+1}-03-31`,
            cadence: 'DAILY',
            createdAt: new Date().toISOString()
          },
          {
            id: 'goal-seed-2',
            name: 'Laptop Upgrade M3',
            targetAmount: 160000,
            currentAmount: 64000,
            deadline: `${y}-12-15`,
            cadence: 'MONTHLY',
            createdAt: new Date().toISOString()
          },
          {
            id: 'goal-seed-3',
            name: 'Gold Sovereign Reserve',
            targetAmount: 85000,
            currentAmount: 28000,
            deadline: `${y+1}-06-30`,
            cadence: 'YEARLY',
            createdAt: new Date().toISOString()
          }
        ],
        ledger: [
          { id: 'tx-1', goalId: 'goal-seed-1', goalName: 'Emergency Fortress', type: 'ADD', amount: 5000, note: 'Freelance savings envelope', date: d1, timestamp: new Date(d1).toISOString() },
          { id: 'tx-2', goalId: 'goal-seed-2', goalName: 'Laptop Upgrade M3', type: 'ADD', amount: 12000, note: 'Monthly disciplined stash', date: d2, timestamp: new Date(d2).toISOString() },
          { id: 'tx-3', goalId: 'goal-seed-1', goalName: 'Emergency Fortress', type: 'ADD', amount: 3500, note: 'Daily food saving & round-up', date: d3, timestamp: new Date(d3).toISOString() },
          { id: 'tx-4', goalId: 'goal-seed-3', goalName: 'Gold Sovereign Reserve', type: 'ADD', amount: 8000, note: 'Cash transfer to physical vault', date: d4, timestamp: new Date(d4).toISOString() },
          { id: 'tx-5', goalId: 'goal-seed-1', goalName: 'Emergency Fortress', type: 'MINUS', amount: 2500, note: 'Emergency vehicle brake fix', date: d5, timestamp: new Date(d5).toISOString() },
          { id: 'tx-6', goalId: 'goal-seed-2', goalName: 'Laptop Upgrade M3', type: 'ADD', amount: 4500, note: 'Bonus manual deposit', date: d6, timestamp: new Date(d6).toISOString() },
          { id: 'tx-7', goalId: 'goal-seed-1', goalName: 'Emergency Fortress', type: 'ADD', amount: 2000, note: 'Discipline daily check-in', date: todayStr, timestamp: new Date().toISOString() }
        ],
        cooldowns: []
      };
    }

    // ============================================================
    // DATA PERSISTENCE SYNC (OPTIMISTIC REAL-TIME + FIRESTORE BACKGROUND)
    // ============================================================
    function initDataSync(user) {
      currentUser = user;
      isDemoMode = !user || user.uid === 'demo-user';

      // Always load local state first for instant 0ms startup
      let stored = getLocalData();
      if (!stored || !stored.goals || stored.goals.length === 0) {
        stored = getSeedState();
        saveLocalData(stored);
      }
      goals = stored.goals || [];
      ledger = stored.ledger || [];
      cooldowns = stored.cooldowns || [];
      renderAll();

      if (isDemoMode || !db) return;

      // Attach Firestore background sync
      try {
        if (unsubGoals) unsubGoals();
        if (unsubLedger) unsubLedger();

        const goalsCol = collection(db, 'users', user.uid, 'goals');
        unsubGoals = onSnapshot(goalsCol, (snapshot) => {
          if (!snapshot.empty) {
            goals = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
            saveLocalData({ goals, ledger, cooldowns });
            renderAll();
          }
        }, (err) => {
          console.warn("Firestore goals snapshot note:", err.message);
        });

        const ledgerCol = collection(db, 'users', user.uid, 'ledger');
        unsubLedger = onSnapshot(ledgerCol, (snapshot) => {
          if (!snapshot.empty) {
            ledger = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
            saveLocalData({ goals, ledger, cooldowns });
            renderAll();
          }
        }, (err) => {
          console.warn("Firestore ledger snapshot note:", err.message);
        });

      } catch (err) {
        console.warn("Sync warning:", err);
      }
    }

    // ── FAST INSTANT REAL-TIME ACTIONS (OPTIMISTIC 0ms) ──────────

    function persistGoal(goalData) {
      const newGoal = {
        id: 'goal-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4),
        ...goalData,
        createdAt: new Date().toISOString()
      };

      // 1. Instant in-memory update
      goals.push(newGoal);

      // 2. Instant localStorage persistence
      saveLocalData({ goals, ledger, cooldowns });

      // 3. Instant UI re-render
      renderAll();

      // 4. Background Firestore write
      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const goalsCol = collection(db, 'users', currentUser.uid, 'goals');
        addDoc(goalsCol, { ...goalData, createdAt: serverTimestamp() }).catch(e => console.warn("Background goal save error:", e));
      }

      return newGoal;
    }

    function persistLedgerEntry(entryData) {
      const isAdd = entryData.type === 'ADD';
      const amt = Number(entryData.amount) || 0;
      const delta = isAdd ? amt : -amt;

      const newEntry = {
        id: 'tx-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4),
        ...entryData,
        amount: amt,
        timestamp: new Date().toISOString()
      };

      // 1. Instant in-memory ledger update
      ledger.unshift(newEntry);

      // 2. Instant goal currentAmount update
      const targetGoal = goals.find(g => g.id === entryData.goalId || g.name.toLowerCase() === (entryData.goalName || '').toLowerCase());
      if (targetGoal) {
        targetGoal.currentAmount = Math.max(0, (Number(targetGoal.currentAmount) || 0) + delta);
      }

      // 3. Instant localStorage persistence
      saveLocalData({ goals, ledger, cooldowns });

      // 4. Instant UI re-render
      renderAll();

      // 5. Background Firestore write
      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const ledgerCol = collection(db, 'users', currentUser.uid, 'ledger');
        addDoc(ledgerCol, { ...entryData, timestamp: serverTimestamp() }).catch(e => console.warn("Background ledger save error:", e));

        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('goal-seed')) {
          const goalRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          updateDoc(goalRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Background goal update error:", e));
        }
      }
    }

    function updateLedgerEntry(id, newAmount, newNote, newDate) {
      const existing = ledger.find(item => item.id === id);
      if (!existing) return;

      const oldAmount = Number(existing.amount) || 0;
      const amountDiff = newAmount - oldAmount;
      const isAdd = existing.type === 'ADD';
      const goalDelta = isAdd ? amountDiff : -amountDiff;
      const targetGoal = goals.find(g => g.id === existing.goalId || g.name === existing.goalName);

      // 1. Instant in-memory update
      existing.amount = newAmount;
      existing.note = newNote;
      existing.date = newDate;

      if (targetGoal) {
        targetGoal.currentAmount = Math.max(0, (Number(targetGoal.currentAmount) || 0) + goalDelta);
      }

      // 2. Instant localStorage persistence
      saveLocalData({ goals, ledger, cooldowns });

      // 3. Instant UI re-render
      renderAll();

      // 4. Background Firestore write
      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const entryRef = doc(db, 'users', currentUser.uid, 'ledger', id);
        updateDoc(entryRef, { amount: newAmount, note: newNote, date: newDate }).catch(e => console.warn("Background ledger update error:", e));

        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('goal-seed')) {
          const goalRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          updateDoc(goalRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Background goal update error:", e));
        }
      }
    }

    function deleteLedgerEntry(id) {
      const existing = ledger.find(item => item.id === id);
      if (!existing) return;

      const isAdd = existing.type === 'ADD';
      const reversalDelta = isAdd ? -Number(existing.amount) : Number(existing.amount);
      const targetGoal = goals.find(g => g.id === existing.goalId || g.name === existing.goalName);

      // 1. Instant in-memory removal
      ledger = ledger.filter(item => item.id !== id);

      if (targetGoal) {
        targetGoal.currentAmount = Math.max(0, (Number(targetGoal.currentAmount) || 0) + reversalDelta);
      }

      // 2. Instant localStorage persistence
      saveLocalData({ goals, ledger, cooldowns });

      // 3. Instant UI re-render
      renderAll();

      // 4. Background Firestore write
      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const entryRef = doc(db, 'users', currentUser.uid, 'ledger', id);
        deleteDoc(entryRef).catch(e => console.warn("Background delete error:", e));

        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('goal-seed')) {
          const goalRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          updateDoc(goalRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Background goal update error:", e));
        }
      }
    }

    // ============================================================
    // RENDER FUNCTIONS (ALL COCKPIT MODULES)
    // ============================================================
    function renderAll() {
      renderCommandMetrics();
      renderGoalsGrid();
      renderAIPacing();
      renderSavingsCalendar();
      renderLedger();
      renderGoalSelectors();
    }

    // 1. Hero Command Metrics
    function renderCommandMetrics() {
      let totalNet = 0;
      let monthSaved = 0;
      const curYear = new Date().getFullYear();
      const curMonth = new Date().getMonth();

      ledger.forEach(item => {
        const amt = Number(item.amount) || 0;
        const isAdd = item.type === 'ADD';
        if (isAdd) {
          totalNet += amt;
        } else {
          totalNet -= amt;
        }

        if (item.date) {
          const d = new Date(item.date);
          if (d.getFullYear() === curYear && d.getMonth() === curMonth) {
            if (isAdd) monthSaved += amt;
            else monthSaved -= amt;
          }
        }
      });

      if (totalNet < 0) totalNet = 0;
      const streak = computeDisciplineStreak();

      const elTotal = document.getElementById('metric-total-capital');
      if (elTotal) elTotal.textContent = '\u20b9' + totalNet.toLocaleString('en-IN');

      const elStreak = document.getElementById('metric-streak-count');
      if (elStreak) elStreak.textContent = `${streak} Days`;

      const elVaults = document.getElementById('metric-vaults-count');
      if (elVaults) elVaults.textContent = `${goals.length} Goals`;

      const elMonth = document.getElementById('metric-month-saved');
      if (elMonth) elMonth.textContent = '\u20b9' + Math.max(0, monthSaved).toLocaleString('en-IN');
    }

    function computeDisciplineStreak() {
      if (!ledger || ledger.length === 0) return 0;

      const addDates = new Set();
      ledger.forEach(item => {
        if (item.type === 'ADD' && item.date) {
          addDates.add(item.date.split('T')[0]);
        }
      });

      if (addDates.size === 0) return 0;

      const today = new Date();
      const fmt = (d) => {
        const y = d.getFullYear();
        const m = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${y}-${m}-${day}`;
      };

      let checkDate = new Date(today);
      let streak = 0;

      if (!addDates.has(fmt(checkDate))) {
        checkDate.setDate(checkDate.getDate() - 1);
      }

      while (addDates.has(fmt(checkDate))) {
        streak++;
        checkDate.setDate(checkDate.getDate() - 1);
      }

      return streak;
    }

    // 2. Goals Grid (Glassy Goal Cards)
    function renderGoalsGrid() {
      const container = document.getElementById('vaults-grid-container');
      const emptyState = document.getElementById('vaults-empty-state');
      if (!container) return;

      if (!goals || goals.length === 0) {
        container.innerHTML = '';
        if (emptyState) emptyState.classList.remove('hidden');
        return;
      }

      if (emptyState) emptyState.classList.add('hidden');

      container.innerHTML = goals.map(g => {
        const cur = Number(g.currentAmount) || 0;
        const tgt = Number(g.targetAmount) || 1;
        const pct = Math.min(100, Math.round((cur / tgt) * 100));

        let daysLeft = 0;
        let quotaStr = '';
        if (g.deadline) {
          const diff = new Date(g.deadline) - new Date();
          daysLeft = Math.max(1, Math.ceil(diff / (1000 * 60 * 60 * 24)));
          const remain = Math.max(0, tgt - cur);
          const daily = Math.round(remain / daysLeft);
          const monthly = Math.round(daily * 30.4);

          if (g.cadence === 'DAILY') quotaStr = `\u20b9${daily.toLocaleString('en-IN')}/day`;
          else if (g.cadence === 'MONTHLY') quotaStr = `\u20b9${monthly.toLocaleString('en-IN')}/mo`;
          else quotaStr = `\u20b9${(monthly * 12).toLocaleString('en-IN')}/yr`;
        }

        return `
          <div class="metallic-card p-5 relative overflow-hidden flex flex-col justify-between" style="border-radius:20px;">
            <div>
              <div class="flex items-start justify-between gap-2 mb-3">
                <div class="flex items-center gap-2.5">
                  <div class="w-9 h-9 rounded-xl bg-blue-50/80 border border-blue-100 flex items-center justify-center text-cobalt flex-shrink-0 shadow-sm">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                  </div>
                  <div>
                    <h4 class="font-extrabold text-charcoal text-sm leading-tight">${g.name}</h4>
                    <span class="text-[10px] font-mono font-bold text-cobalt uppercase tracking-wide">${g.cadence || 'DAILY'} &bull; ${quotaStr}</span>
                  </div>
                </div>
                <span class="font-mono text-xs font-bold text-coolslate bg-white/80 border border-slate-200/80 px-2.5 py-0.5 rounded-lg shadow-xs">${pct}%</span>
              </div>

              <!-- Shimmer Progress Bar -->
              <div class="progress-track my-3">
                <div class="progress-fill-shimmer" style="width: ${pct}%;"></div>
              </div>

              <div class="flex items-baseline justify-between text-xs mb-3">
                <span class="font-mono font-extrabold text-charcoal text-base">&#8377;${cur.toLocaleString('en-IN')}</span>
                <span class="text-coolslate font-mono text-[11px]">of &#8377;${tgt.toLocaleString('en-IN')}</span>
              </div>

              <div class="text-[10px] font-mono text-coolslate flex items-center gap-1.5 mb-4">
                <span>⏳</span>
                <span>${daysLeft} days remaining &bull; Due ${g.deadline || 'Ongoing'}</span>
              </div>
            </div>

            <!-- Card Actions -->
            <div class="flex items-center gap-2 pt-3 border-t border-white/60">
              <button class="btn-primary-metallic text-xs py-1.5 px-3 flex-1 btn-quick-goal-stash" data-goal-id="${g.id}" data-goal-name="${g.name}" type="button">
                + Add Funds
              </button>
            </div>
          </div>
        `;
      }).join('');

      // Wire quick stash buttons
      container.querySelectorAll('.btn-quick-goal-stash').forEach(btn => {
        btn.addEventListener('click', () => {
          const gName = btn.dataset.goalName;
          openAddSavingsModal(gName);
        });
      });
    }

    // 3. Antigravity AI Dynamic Pacing Engine
    function renderAIPacing() {
      const selector = document.getElementById('ai-goal-selector');
      const selectedId = selector ? selector.value : null;

      let activeGoal = goals.find(g => g.id === selectedId) || goals[0];
      if (!activeGoal) return;

      const cur = Number(activeGoal.currentAmount) || 0;
      const tgt = Number(activeGoal.targetAmount) || 1;
      const remain = Math.max(0, tgt - cur);

      let daysLeft = 1;
      if (activeGoal.deadline) {
        const diff = new Date(activeGoal.deadline) - new Date();
        daysLeft = Math.max(1, Math.ceil(diff / (1000 * 60 * 60 * 24)));
      }

      const dailyQuota = Math.round(remain / daysLeft);
      const monthlyQuota = Math.round(dailyQuota * 30.4);

      // Compute recent velocity over last 7 days for this goal
      const now = new Date();
      const sevenDaysAgo = new Date(now.getTime() - 7 * 86400000);
      let recentSum = 0;
      ledger.forEach(item => {
        if ((item.goalId === activeGoal.id || item.goalName === activeGoal.name) && item.type === 'ADD' && item.date) {
          const d = new Date(item.date);
          if (d >= sevenDaysAgo) recentSum += Number(item.amount) || 0;
        }
      });
      const recentDailyVelocity = Math.round(recentSum / 7);

      const banner = document.getElementById('ai-pacing-banner');
      const icon = document.getElementById('ai-pacing-icon');
      const headline = document.getElementById('ai-pacing-headline');
      const detail = document.getElementById('ai-pacing-detail');

      if (cur >= tgt) {
        banner.className = 'mt-5 p-4 rounded-2xl pacing-banner-optimal transition-all duration-300';
        icon.textContent = '🏆';
        headline.textContent = `Goal Achieved: "${activeGoal.name}" is 100% completed!`;
        detail.textContent = `You have reached \u20b9${cur.toLocaleString('en-IN')}! Create a new vault or expand your horizon.`;
      } else if (recentDailyVelocity >= dailyQuota && recentDailyVelocity > 0) {
        const earlyDays = Math.max(1, Math.round(daysLeft - (remain / recentDailyVelocity)));
        banner.className = 'mt-5 p-4 rounded-2xl pacing-banner-optimal transition-all duration-300';
        icon.textContent = '⚡';
        headline.textContent = `Pacing Optimal: You are projected to hit "${activeGoal.name}" ${earlyDays} days early!`;
        detail.textContent = `Current 7-day velocity is \u20b9${recentDailyVelocity.toLocaleString('en-IN')}/day vs. required \u20b9${dailyQuota.toLocaleString('en-IN')}/day. Superb discipline!`;
      } else if (recentDailyVelocity < dailyQuota * 0.75 && recentSum > 0) {
        const deficit = Math.round((dailyQuota - recentDailyVelocity) * 7);
        banner.className = 'mt-5 p-4 rounded-2xl pacing-banner-warning transition-all duration-300';
        icon.textContent = '⚠️';
        headline.textContent = `Pacing Warning: You are \u20b9${deficit.toLocaleString('en-IN')} behind pace on "${activeGoal.name}".`;
        detail.textContent = `Aapne target cadence se kam save kiya hai. Deadline maintain karne ke liye agle 7 din daily quota \u20b9${dailyQuota.toLocaleString('en-IN')} maintain karein.`;
      } else {
        banner.className = 'mt-5 p-4 rounded-2xl pacing-banner-optimal transition-all duration-300';
        icon.textContent = '🎯';
        headline.textContent = `Cadence Calibrated: Target requires \u20b9${dailyQuota.toLocaleString('en-IN')} / day.`;
        detail.textContent = `Save \u20b9${dailyQuota.toLocaleString('en-IN')} daily or \u20b9${monthlyQuota.toLocaleString('en-IN')} monthly to hit your \u20b9${tgt.toLocaleString('en-IN')} goal by ${activeGoal.deadline || 'deadline'}.`;
      }

      const elDaily = document.getElementById('ai-quota-daily');
      if (elDaily) elDaily.textContent = `\u20b9${dailyQuota.toLocaleString('en-IN')} / day`;

      const elMonth = document.getElementById('ai-quota-monthly');
      if (elMonth) elMonth.textContent = `\u20b9${monthlyQuota.toLocaleString('en-IN')} / mo`;

      const elDays = document.getElementById('ai-days-remaining');
      if (elDays) elDays.textContent = `${daysLeft} Days`;

      const elDead = document.getElementById('ai-deadline-date');
      if (elDead) elDead.textContent = `Target: ${activeGoal.deadline || '--'}`;

      const elEta = document.getElementById('ai-projected-eta');
      const effVelocity = recentDailyVelocity > 0 ? recentDailyVelocity : dailyQuota;
      const projDays = effVelocity > 0 ? Math.ceil(remain / effVelocity) : daysLeft;
      const projDate = new Date(Date.now() + projDays * 86400000);
      const etaFormatted = projDate.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
      if (elEta) elEta.textContent = etaFormatted;
    }

    // 4. Interactive Savings Calendar & Streak Matrix
    function renderSavingsCalendar() {
      const grid = document.getElementById('calendar-grid');
      const monthTitle = document.getElementById('cal-month-title');
      if (!grid || !monthTitle) return;

      const year = currentCalDate.getFullYear();
      const month = currentCalDate.getMonth();
      const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      monthTitle.textContent = `${monthNames[month]} ${year}`;

      const dayMap = {};
      ledger.forEach(item => {
        if (item.type === 'ADD' && item.date) {
          const key = item.date.split('T')[0];
          dayMap[key] = (dayMap[key] || 0) + (Number(item.amount) || 0);
        }
      });

      const firstDay = new Date(year, month, 1).getDay();
      const daysInMonth = new Date(year, month + 1, 0).getDate();
      const prevMonthDays = new Date(year, month, 0).getDate();

      const today = new Date();
      const isCurrentMonth = today.getFullYear() === year && today.getMonth() === month;
      const todayDateNum = today.getDate();

      let cellsHTML = '';
      let activeDaysCount = 0;

      for (let i = firstDay - 1; i >= 0; i--) {
        const d = prevMonthDays - i;
        cellsHTML += `<div class="cal-day-cell cal-other-month"><span>${d}</span></div>`;
      }

      for (let d = 1; d <= daysInMonth; d++) {
        const yStr = year;
        const mStr = String(month + 1).padStart(2, '0');
        const dStr = String(d).padStart(2, '0');
        const dateKey = `${yStr}-${mStr}-${dStr}`;

        const savedAmount = dayMap[dateKey] || 0;
        const isToday = isCurrentMonth && d === todayDateNum;
        const hasSaved = savedAmount > 0;
        if (hasSaved) activeDaysCount++;

        let classes = 'cal-day-cell cursor-pointer';
        if (hasSaved) classes += ' cal-active-saved';
        if (isToday) classes += ' cal-today';

        cellsHTML += `
          <div class="${classes}" data-date="${dateKey}" title="${hasSaved ? 'Saved: \u20b9' + savedAmount.toLocaleString('en-IN') : 'No savings logged'}">
            <span class="cal-day-num ${isToday ? 'font-extrabold text-cobalt' : ''}">${d}</span>
            ${hasSaved ? `<span class="cal-day-badge">+\u20b9${savedAmount >= 1000 ? (savedAmount/1000).toFixed(savedAmount%1000===0?0:1) + 'k' : savedAmount}</span>` : '<span class="text-[9px] text-slate-300">&bull;</span>'}
          </div>
        `;
      }

      const totalCells = firstDay + daysInMonth;
      const remainder = (7 - (totalCells % 7)) % 7;
      for (let i = 1; i <= remainder; i++) {
        cellsHTML += `<div class="cal-day-cell cal-other-month"><span>${i}</span></div>`;
      }

      grid.innerHTML = cellsHTML;

      const rateEl = document.getElementById('cal-discipline-rate');
      const countEl = document.getElementById('cal-month-days-count');
      const pct = Math.round((activeDaysCount / daysInMonth) * 100);
      if (rateEl) rateEl.textContent = `${pct}%`;
      if (countEl) countEl.textContent = `${activeDaysCount} / ${daysInMonth}`;

      grid.querySelectorAll('.cal-active-saved').forEach(cell => {
        cell.addEventListener('click', () => {
          const dateStr = cell.dataset.date;
          const dayEntries = ledger.filter(item => item.date === dateStr && item.type === 'ADD');
          const totalDay = dayEntries.reduce((s, e) => s + Number(e.amount), 0);
          showToast(`📅 ${dateStr}: \u20b9${totalDay.toLocaleString('en-IN')} saved across ${dayEntries.length} entries!`, 'info');
        });
      });
    }

    // 5. Chronological Ledger Table
    function renderLedger() {
      const tbody = document.getElementById('ledger-table-body');
      const emptyState = document.getElementById('ledger-empty-state');
      if (!tbody) return;

      let filtered = [...ledger];
      if (ledgerFilter === 'ADD') filtered = filtered.filter(i => i.type === 'ADD');
      if (ledgerFilter === 'MINUS') filtered = filtered.filter(i => i.type === 'MINUS');

      filtered.sort((a, b) => new Date(b.date || b.timestamp) - new Date(a.date || a.timestamp));

      if (filtered.length === 0) {
        tbody.innerHTML = '';
        if (emptyState) emptyState.classList.remove('hidden');
        return;
      }

      if (emptyState) emptyState.classList.add('hidden');

      tbody.innerHTML = filtered.map(item => {
        const isAdd = item.type === 'ADD';
        const amt = Number(item.amount) || 0;
        const sign = isAdd ? '+' : '-';
        const colorCls = isAdd ? 'text-emerald-600 font-extrabold' : 'text-crimson font-extrabold';
        const badgeCls = isAdd ? 'ledger-badge-add' : 'ledger-badge-minus';
        const badgeLabel = isAdd ? '+ DEPOSIT' : '- WITHDRAW';

        return `
          <tr class="hover:bg-blue-50/40 transition-colors">
            <td class="py-3 px-3 font-mono text-coolslate text-[11px] whitespace-nowrap">${item.date || 'Today'}</td>
            <td class="py-3 px-3 font-bold text-charcoal max-w-[140px] truncate">${item.goalName || 'General Stash'}</td>
            <td class="py-3 px-3">
              <span class="text-[9px] font-mono font-bold px-2.5 py-0.5 rounded-full ${badgeCls}">${badgeLabel}</span>
            </td>
            <td class="py-3 px-3 text-coolslate max-w-[180px] truncate">${item.note || '--'}</td>
            <td class="py-3 px-3 text-right font-mono ${colorCls} text-sm">${sign}\u20b9${amt.toLocaleString('en-IN')}</td>
            <td class="py-3 px-3 text-right whitespace-nowrap space-x-1">
              <button class="btn-edit-entry text-[11px] font-semibold text-cobalt hover:bg-blue-50/80 px-2 py-1 rounded-lg transition-colors cursor-pointer" data-id="${item.id}" type="button">Edit</button>
              <button class="btn-del-entry text-[11px] font-semibold text-rose-600 hover:bg-rose-50/80 px-2 py-1 rounded-lg transition-colors cursor-pointer" data-id="${item.id}" type="button">Delete</button>
            </td>
          </tr>
        `;
      }).join('');

      tbody.querySelectorAll('.btn-edit-entry').forEach(btn => {
        btn.addEventListener('click', () => openEditLedgerModal(btn.dataset.id));
      });
      tbody.querySelectorAll('.btn-del-entry').forEach(btn => {
        btn.addEventListener('click', () => openDeleteLedgerModal(btn.dataset.id));
      });
    }

    // 6. Populate dropdown selectors for goals
    function renderGoalSelectors() {
      const aiSel = document.getElementById('ai-goal-selector');
      if (aiSel) {
        const curVal = aiSel.value;
        aiSel.innerHTML = goals.map(g => `<option value="${g.id}">${g.name}</option>`).join('');
        if (curVal && goals.some(g => g.id === curVal)) {
          aiSel.value = curVal;
        }
      }

      const withSel = document.getElementById('withdrawal-vault-select');
      if (withSel) {
        withSel.innerHTML = goals.map(g => `<option value="${g.id}">${g.name} (\u20b9${(g.currentAmount || 0).toLocaleString('en-IN')} available)</option>`).join('');
      }
    }

    // ============================================================
    // MODAL HANDLERS & FAST INSTANT SUBMITS (REAL-TIME)
    // ============================================================

    function closeModals() {
      document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('open'));
    }

    document.querySelectorAll('.modal-close').forEach(btn => {
      btn.addEventListener('click', closeModals);
    });

    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeModals();
      });
    });

    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeModals();
    });

    // ── 1. Create Goal Vault Modal ───────────────────────────────
    const modalCreateGoal = document.getElementById('modal-create-goal');
    const formCreateGoal = document.getElementById('form-create-goal');
    const goalInputName = document.getElementById('goal-input-name');
    const goalInputAmount = document.getElementById('goal-input-amount');
    const goalInputDeadline = document.getElementById('goal-input-deadline');
    const goalMathText = document.getElementById('goal-math-text');
    const btnCreateGoalSubmit = document.getElementById('btn-create-goal-submit');

    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomY = tomorrow.getFullYear();
    const tomM = String(tomorrow.getMonth() + 1).padStart(2, '0');
    const tomD = String(tomorrow.getDate()).padStart(2, '0');
    if (goalInputDeadline) goalInputDeadline.min = `${tomY}-${tomM}-${tomD}`;

    function updateGoalLiveMath() {
      const amt = Number(goalInputAmount.value) || 0;
      const deadVal = goalInputDeadline.value;

      if (!amt || !deadVal) {
        goalMathText.textContent = "Enter amount and target date to compute required daily or monthly savings quota.";
        return;
      }

      const diff = new Date(deadVal) - new Date();
      const days = Math.max(1, Math.ceil(diff / (1000 * 60 * 60 * 24)));
      const daily = Math.round(amt / days);
      const monthly = Math.round(daily * 30.4);

      goalMathText.innerHTML = `
        <strong>Aapko is target ko hit karne ke liye roz &#8377;${daily.toLocaleString('en-IN')}, ya mahine ke &#8377;${monthly.toLocaleString('en-IN')} bachane honge.</strong><br/>
        <span class="text-[11px] text-blue-700">Requires &#8377;${daily.toLocaleString('en-IN')} / day across ${days} remaining days.</span>
      `;
    }

    goalInputAmount?.addEventListener('input', updateGoalLiveMath);
    goalInputDeadline?.addEventListener('input', updateGoalLiveMath);

    document.querySelectorAll('.btn-cadence-toggle').forEach(btn => {
      btn.addEventListener('click', () => {
        selectedGoalCadence = btn.dataset.cadence;
        document.querySelectorAll('.btn-cadence-toggle').forEach(b => {
          b.className = 'btn-cadence-toggle py-2 px-3 text-xs font-bold rounded-xl border border-slate-200/80 bg-white/70 text-coolslate transition-all cursor-pointer';
        });
        btn.className = 'btn-cadence-toggle py-2 px-3 text-xs font-bold rounded-xl border border-cobalt bg-blue-50/90 text-cobalt transition-all cursor-pointer';
      });
    });

    formCreateGoal?.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = goalInputName.value.trim();
      const amt = Number(goalInputAmount.value) || 0;
      const deadline = goalInputDeadline.value;

      let hasErr = false;
      if (!name) { document.getElementById('goal-err-name')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('goal-err-name')?.classList.add('hidden');

      if (amt < 100) { document.getElementById('goal-err-amount')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('goal-err-amount')?.classList.add('hidden');

      if (!deadline) { document.getElementById('goal-err-deadline')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('goal-err-deadline')?.classList.add('hidden');

      if (hasErr) return;

      // INSTANT FAST REAL-TIME SAVE
      lockBtn(btnCreateGoalSubmit, 'Secured! ⚡');

      persistGoal({
        name,
        targetAmount: amt,
        currentAmount: 0,
        deadline,
        cadence: selectedGoalCadence
      });

      setTimeout(() => {
        unlockBtn(btnCreateGoalSubmit);
        modalCreateGoal.classList.remove('open');
        goalInputName.value = '';
        goalInputAmount.value = '';
        goalInputDeadline.value = '';
        showToast(`🎯 Goal Vault "${name}" secured and live!`, 'success');
      }, 120);
    });

    const openCreateGoalModal = () => {
      modalCreateGoal.classList.add('open');
      setTimeout(() => goalInputName.focus(), 250);
    };

    document.getElementById('btn-quick-new-vault')?.addEventListener('click', openCreateGoalModal);
    document.getElementById('btn-grid-new-vault')?.addEventListener('click', openCreateGoalModal);
    document.getElementById('btn-empty-new-vault')?.addEventListener('click', openCreateGoalModal);

    // ── 2. Add Savings Modal (+ REAL-TIME FAST SAVE) ─────────────
    const modalAddSavings = document.getElementById('modal-add-savings');
    const formAddSavings = document.getElementById('form-add-savings');
    const addVaultInput = document.getElementById('add-savings-vault-input');
    const addChipsWrapper = document.getElementById('add-chips-wrapper');
    const addChipsSuggestions = document.getElementById('add-chips-suggestions');
    const addAmountInput = document.getElementById('add-savings-amount');
    const addNoteInput = document.getElementById('add-savings-note');
    const addDateInput = document.getElementById('add-savings-date');
    const btnAddSavingsSubmit = document.getElementById('btn-add-savings-submit');
    let addSelectedChip = '';

    const nowY = new Date().getFullYear();
    const nowM = String(new Date().getMonth() + 1).padStart(2, '0');
    const nowD = String(new Date().getDate()).padStart(2, '0');
    if (addDateInput) addDateInput.value = `${nowY}-${nowM}-${nowD}`;

    function setAddChip(label) {
      addSelectedChip = label;
      addChipsWrapper.querySelectorAll('.vault-chip').forEach(c => c.remove());
      if (!label) {
        addVaultInput.placeholder = 'e.g. Emergency Fund, Laptop Upgrade…';
        return;
      }
      const chip = document.createElement('span');
      chip.className = 'vault-chip';
      chip.innerHTML = `${label}<button class="chip-remove" type="button" aria-label="Remove">&times;</button>`;
      chip.querySelector('.chip-remove').addEventListener('click', (e) => {
        e.stopPropagation();
        clearAddChip();
      });
      addChipsWrapper.insertBefore(chip, addVaultInput);
      addVaultInput.placeholder = '';
      addVaultInput.value = '';
      addChipsSuggestions.classList.remove('visible');
    }

    function clearAddChip() {
      addSelectedChip = '';
      addChipsWrapper.querySelectorAll('.vault-chip').forEach(c => c.remove());
      addVaultInput.placeholder = 'e.g. Emergency Fund, Laptop Upgrade…';
      addVaultInput.focus();
    }

    function showAddSuggestions(q = '') {
      const query = q.trim().toLowerCase();
      const allLabels = goals.map(g => g.name);
      const filtered = allLabels.filter(name => !query || name.toLowerCase().includes(query));

      if (filtered.length === 0 || addSelectedChip) {
        addChipsSuggestions.classList.remove('visible');
        return;
      }

      addChipsSuggestions.innerHTML = filtered.map(name => `
        <div class="chip-suggestion-item" data-name="${name}">
          <span class="s-icon">🎯</span>
          <span>${name}</span>
        </div>
      `).join('');

      addChipsSuggestions.querySelectorAll('.chip-suggestion-item').forEach(item => {
        item.addEventListener('mousedown', (e) => {
          e.preventDefault();
          setAddChip(item.dataset.name);
        });
      });

      addChipsSuggestions.classList.add('visible');
    }

    addVaultInput?.addEventListener('focus', () => showAddSuggestions(addVaultInput.value));
    addVaultInput?.addEventListener('input', () => showAddSuggestions(addVaultInput.value));
    addVaultInput?.addEventListener('blur', () => setTimeout(() => addChipsSuggestions.classList.remove('visible'), 160));
    addVaultInput?.addEventListener('keydown', (e) => {
      if ((e.key === 'Enter' || e.key === ',') && addVaultInput.value.trim()) {
        e.preventDefault();
        setAddChip(addVaultInput.value.trim());
      }
      if (e.key === 'Backspace' && !addVaultInput.value && addSelectedChip) {
        clearAddChip();
      }
    });

    document.querySelectorAll('.btn-add-preset').forEach(btn => {
      btn.addEventListener('click', () => {
        addAmountInput.value = btn.dataset.amount;
        document.querySelectorAll('.btn-add-preset').forEach(b => b.classList.remove('border-cobalt', 'text-cobalt', 'bg-blue-50/80'));
        btn.classList.add('border-cobalt', 'text-cobalt', 'bg-blue-50/80');
      });
    });

    // CRITICAL: FAST REAL-TIME SAVE (0ms latency, instant response)
    formAddSavings?.addEventListener('submit', (e) => {
      e.preventDefault();
      const vaultName = addSelectedChip || addVaultInput.value.trim();
      const amt = Number(addAmountInput.value) || 0;
      const note = addNoteInput.value.trim() || 'Manual savings deposit';
      const date = addDateInput.value || `${nowY}-${nowM}-${nowD}`;

      let hasErr = false;
      if (!vaultName) { document.getElementById('add-err-vault')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('add-err-vault')?.classList.add('hidden');

      if (amt <= 0) { document.getElementById('add-err-amount')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('add-err-amount')?.classList.add('hidden');

      if (hasErr) return;

      lockBtn(btnAddSavingsSubmit, 'Stashed! ⚡');

      const goalMatch = goals.find(g => g.name.toLowerCase() === vaultName.toLowerCase());
      const goalId = goalMatch ? goalMatch.id : 'custom-' + Date.now();

      // Instant optimistic save
      persistLedgerEntry({
        goalId,
        goalName: vaultName,
        type: 'ADD',
        amount: amt,
        note,
        date
      });

      // Quick smooth close
      setTimeout(() => {
        modalAddSavings.classList.remove('open');
        clearAddChip();
        addAmountInput.value = '';
        addNoteInput.value = '';
        document.querySelectorAll('.btn-add-preset').forEach(b => b.classList.remove('border-cobalt', 'text-cobalt', 'bg-blue-50/80'));
        unlockBtn(btnAddSavingsSubmit);
        showToast(`+₹${amt.toLocaleString('en-IN')} added to "${vaultName}"! ⚡`, 'success');
      }, 120);
    });

    function openAddSavingsModal(preselectGoal = '') {
      modalAddSavings.classList.add('open');
      if (preselectGoal) {
        setAddChip(preselectGoal);
      } else if (goals.length > 0) {
        setAddChip(goals[0].name);
      }
      setTimeout(() => addAmountInput.focus(), 250);
    }

    document.getElementById('btn-quick-add-savings')?.addEventListener('click', () => openAddSavingsModal());

    // ── 3. Record Emergency Withdrawal Modal (- REAL-TIME FAST) ──
    const modalWithdrawal = document.getElementById('modal-record-withdrawal');
    const formWithdrawal = document.getElementById('form-record-withdrawal');
    const withVaultSelect = document.getElementById('withdrawal-vault-select');
    const withAmountInput = document.getElementById('withdrawal-amount');
    const withNoteInput = document.getElementById('withdrawal-note');
    const withDateInput = document.getElementById('withdrawal-date');
    const btnWithdrawalSubmit = document.getElementById('btn-withdrawal-submit');

    if (withDateInput) withDateInput.value = `${nowY}-${nowM}-${nowD}`;

    formWithdrawal?.addEventListener('submit', (e) => {
      e.preventDefault();
      const goalId = withVaultSelect.value;
      const amt = Number(withAmountInput.value) || 0;
      const note = withNoteInput.value.trim();
      const date = withDateInput.value || `${nowY}-${nowM}-${nowD}`;

      let hasErr = false;
      if (!goalId) { document.getElementById('withdrawal-err-vault')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('withdrawal-err-vault')?.classList.add('hidden');

      if (amt <= 0) { document.getElementById('withdrawal-err-amount')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('withdrawal-err-amount')?.classList.add('hidden');

      if (!note) { document.getElementById('withdrawal-err-note')?.classList.remove('hidden'); hasErr = true; }
      else document.getElementById('withdrawal-err-note')?.classList.add('hidden');

      if (hasErr) return;

      lockBtn(btnWithdrawalSubmit, 'Recorded! 🛡️');

      const goalMatch = goals.find(g => g.id === goalId);
      const goalName = goalMatch ? goalMatch.name : 'Vault';

      // Instant optimistic save
      persistLedgerEntry({
        goalId,
        goalName,
        type: 'MINUS',
        amount: amt,
        note,
        date
      });

      setTimeout(() => {
        unlockBtn(btnWithdrawalSubmit);
        modalWithdrawal.classList.remove('open');
        withAmountInput.value = '';
        withNoteInput.value = '';
        showToast(`-₹${amt.toLocaleString('en-IN')} emergency withdrawal logged for "${goalName}".`, 'info');
      }, 120);
    });

    document.getElementById('btn-quick-withdrawal')?.addEventListener('click', () => {
      modalWithdrawal.classList.add('open');
      setTimeout(() => withAmountInput.focus(), 250);
    });

    // ── 4. Edit Ledger Entry Modal ──────────────────────────────
    const modalEditLedger = document.getElementById('modal-edit-ledger');
    const formEditLedger = document.getElementById('form-edit-ledger');
    const editEntryId = document.getElementById('edit-entry-id');
    const editEntryVault = document.getElementById('edit-entry-vault');
    const editEntryTypeBadge = document.getElementById('edit-entry-type-badge');
    const editEntryAmount = document.getElementById('edit-entry-amount');
    const editEntryNote = document.getElementById('edit-entry-note');
    const editEntryDate = document.getElementById('edit-entry-date');
    const btnEditLedgerSubmit = document.getElementById('btn-edit-ledger-submit');

    function openEditLedgerModal(id) {
      const entry = ledger.find(e => e.id === id);
      if (!entry) return;

      editEntryId.value = entry.id;
      editEntryVault.textContent = entry.goalName || 'General Stash';
      editEntryTypeBadge.textContent = entry.type === 'ADD' ? '+ DEPOSIT' : '- WITHDRAW';
      editEntryTypeBadge.className = `font-mono text-[10px] font-bold px-2 py-0.5 rounded-full ${entry.type === 'ADD' ? 'ledger-badge-add' : 'ledger-badge-minus'}`;
      editEntryAmount.value = entry.amount;
      editEntryNote.value = entry.note || '';
      editEntryDate.value = entry.date || '';

      modalEditLedger.classList.add('open');
    }

    formEditLedger?.addEventListener('submit', (e) => {
      e.preventDefault();
      const id = editEntryId.value;
      const amt = Number(editEntryAmount.value) || 0;
      const note = editEntryNote.value.trim();
      const date = editEntryDate.value;

      if (!id || amt <= 0) return;

      lockBtn(btnEditLedgerSubmit, 'Saved! ⚡');

      updateLedgerEntry(id, amt, note, date);

      setTimeout(() => {
        unlockBtn(btnEditLedgerSubmit);
        modalEditLedger.classList.remove('open');
        showToast('Transaction record updated!', 'success');
      }, 120);
    });

    // ── 5. Delete Ledger Confirmation Modal ──────────────────────
    const modalDeleteLedger = document.getElementById('modal-delete-ledger');
    const deleteEntryId = document.getElementById('delete-entry-id');
    const delPreviewDate = document.getElementById('del-preview-date');
    const delPreviewVault = document.getElementById('del-preview-vault');
    const delPreviewAmount = document.getElementById('del-preview-amount');
    const delPreviewNote = document.getElementById('del-preview-note');
    const btnDeleteLedgerConfirm = document.getElementById('btn-delete-ledger-confirm');

    function openDeleteLedgerModal(id) {
      const entry = ledger.find(e => e.id === id);
      if (!entry) return;

      deleteEntryId.value = entry.id;
      delPreviewDate.textContent = entry.date || 'Today';
      delPreviewVault.textContent = entry.goalName || 'Goal';
      delPreviewAmount.textContent = (entry.type === 'ADD' ? '+' : '-') + '\u20b9' + Number(entry.amount).toLocaleString('en-IN');
      delPreviewAmount.className = entry.type === 'ADD' ? 'font-mono text-emerald-600 font-bold' : 'font-mono text-crimson font-bold';
      delPreviewNote.textContent = entry.note || '--';

      modalDeleteLedger.classList.add('open');
    }

    btnDeleteLedgerConfirm?.addEventListener('click', () => {
      const id = deleteEntryId.value;
      if (!id) return;

      lockBtn(btnDeleteLedgerConfirm, 'Deleted!');

      deleteLedgerEntry(id);

      setTimeout(() => {
        unlockBtn(btnDeleteLedgerConfirm);
        modalDeleteLedger.classList.remove('open');
        showToast('Transaction removed & balance reversed.', 'info');
      }, 120);
    });

    // ── 6. Privacy & Disclaimer Modal ───────────────────────────
    const modalPrivacy = document.getElementById('modal-privacy-disclaimer');
    const openPrivacyModal = () => modalPrivacy.classList.add('open');

    document.getElementById('btn-header-disclaimer')?.addEventListener('click', openPrivacyModal);
    document.getElementById('btn-banner-disclaimer')?.addEventListener('click', openPrivacyModal);
    document.getElementById('btn-footer-disclaimer')?.addEventListener('click', openPrivacyModal);

    // ── 7. Calendar Month Navigation ────────────────────────────
    document.getElementById('cal-prev-btn')?.addEventListener('click', () => {
      currentCalDate.setMonth(currentCalDate.getMonth() - 1);
      renderSavingsCalendar();
    });

    document.getElementById('cal-next-btn')?.addEventListener('click', () => {
      currentCalDate.setMonth(currentCalDate.getMonth() + 1);
      renderSavingsCalendar();
    });

    document.getElementById('cal-today-btn')?.addEventListener('click', () => {
      currentCalDate = new Date();
      renderSavingsCalendar();
    });

    // ── 8. Ledger Filter Buttons ─────────────────────────────────
    document.getElementById('filter-ledger-all')?.addEventListener('click', () => {
      ledgerFilter = 'ALL';
      setFilterActive('filter-ledger-all');
      renderLedger();
    });

    document.getElementById('filter-ledger-add')?.addEventListener('click', () => {
      ledgerFilter = 'ADD';
      setFilterActive('filter-ledger-add');
      renderLedger();
    });

    document.getElementById('filter-ledger-minus')?.addEventListener('click', () => {
      ledgerFilter = 'MINUS';
      setFilterActive('filter-ledger-minus');
      renderLedger();
    });

    function setFilterActive(activeId) {
      ['filter-ledger-all', 'filter-ledger-add', 'filter-ledger-minus'].forEach(id => {
        const btn = document.getElementById(id);
        if (id === activeId) {
          btn.className = 'text-[11px] font-bold px-3 py-1 rounded-lg bg-white/90 text-charcoal shadow-xs transition-all cursor-pointer';
        } else {
          btn.className = 'text-[11px] font-bold px-3 py-1 rounded-lg text-coolslate hover:text-charcoal transition-all cursor-pointer';
        }
      });
    }

    // ── 9. AI Goal Selector Change ──────────────────────────────
    document.getElementById('ai-goal-selector')?.addEventListener('change', () => {
      renderAIPacing();
    });

    // ── 10. Impulse Cooldown Chamber ─────────────────────────────
    (function initCooldownEngine() {
      const cdPrice = document.getElementById('cd-item-price');
      const cdHoursOut = document.getElementById('cd-hours-output');
      const cdDaysOut = document.getElementById('cd-days-output');
      const cdWeeksOut = document.getElementById('cd-weeks-output');
      const submitBtn = document.getElementById('btn-cooldown-submit');

      cdPrice?.addEventListener('input', () => {
        const p = Number(cdPrice.value) || 0;
        const hrs = p / hourlyWageRate;
        const days = hrs / 8;
        const wks = days / 5;
        cdHoursOut.textContent = hrs > 0 ? hrs.toFixed(1) : '0.0';
        cdDaysOut.textContent = p > 0 ? `${days.toFixed(1)} work days` : 'Enter price to begin';
        cdWeeksOut.textContent = p > 0 && wks >= 0.1 ? `${wks.toFixed(1)} work weeks` : '';
      });

      document.getElementById('cooldown-calc-form')?.addEventListener('submit', (e) => {
        e.preventDefault();
        const itemName = document.getElementById('cd-item-name').value.trim();
        const price = Number(cdPrice.value) || 0;
        if (!itemName || price <= 0) return;

        lockBtn(submitBtn, 'Engaging Lock...');

        setTimeout(() => {
          const container = document.getElementById('cooldown-active-items');
          document.getElementById('cooldown-empty-state')?.classList.add('hidden');

          const card = document.createElement('div');
          card.className = 'bg-white/70 backdrop-blur-md border border-white/80 rounded-xl p-3.5 flex items-center justify-between shadow-xs';
          card.innerHTML = `
            <div>
              <div class="text-xs font-bold text-charcoal">${itemName}</div>
              <div class="text-[10px] font-mono text-coolslate mt-0.5">\u20b9${price.toLocaleString('en-IN')} &bull; ${(price / hourlyWageRate).toFixed(1)} labor-hours</div>
            </div>
            <div class="text-right">
              <div class="font-mono font-bold text-cobalt text-sm timer-tick" data-secs="172800">48:00:00</div>
              <button class="text-[10px] font-bold text-emerald-600 hover:underline mt-0.5 btn-resolve-cooldown cursor-pointer" data-item="${itemName}" data-val="${price}">Stash Now &rarr;</button>
            </div>
          `;
          container.prepend(card);

          card.querySelector('.btn-resolve-cooldown').addEventListener('click', () => {
            const firstGoal = goals[0];
            persistLedgerEntry({
              goalId: firstGoal ? firstGoal.id : 'impulse-shield',
              goalName: firstGoal ? firstGoal.name : 'Impulse Defended',
              type: 'ADD',
              amount: price,
              note: `Impulse Defended: ${itemName}`,
              date: `${nowY}-${nowM}-${nowD}`
            });
            card.remove();
            if (!container.querySelector('.bg-white/70')) {
              document.getElementById('cooldown-empty-state')?.classList.remove('hidden');
            }
            showToast(`🎉 Impulse defeated! \u20b9${price.toLocaleString('en-IN')} secured into your vault!`, 'success');
          });

          document.getElementById('cd-item-name').value = '';
          cdPrice.value = '';
          cdHoursOut.textContent = '0.0';
          cdDaysOut.textContent = 'Enter price to begin';
          cdWeeksOut.textContent = '';

          unlockBtn(submitBtn);
          showToast(`🔒 ${itemName} locked in 48-Hour Cooldown Chamber!`, 'success');
        }, 150);
      });

      setInterval(() => {
        document.querySelectorAll('.timer-tick').forEach(el => {
          let s = Number(el.getAttribute('data-secs')) || 0;
          if (s > 0) s--;
          el.setAttribute('data-secs', s);
          const h = Math.floor(s / 3600);
          const m = Math.floor((s % 3600) / 60);
          const sec = s % 60;
          el.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
        });
      }, 1000);
    })();

    // ============================================================
    // AUTH GATEWAY & DISSOLVE TRANSITION
    // ============================================================
    let isTransitioning = false;

    function transitionToDashboard(userData) {
      if (isTransitioning) return;
      isTransitioning = true;

      const name = userData.displayName || userData.email?.split('@')[0] || "Saver";
      dashUserName.textContent = name;
      if (userData.photoURL) {
        dashUserAvatar.innerHTML = `<img src="${userData.photoURL}" alt="${name}" class="w-full h-full object-cover rounded-full" />`;
      } else {
        dashUserAvatar.textContent = (name[0] || 'S').toUpperCase();
      }

      initDataSync(userData);

      authCard.classList.add('dissolve-exit');

      setTimeout(() => {
        authView.style.display = 'none';
        dashboardView.classList.remove('hidden');
        void dashboardView.offsetWidth;
        dashboardView.classList.add('active');
        window.scrollTo({ top: 0, behavior: 'smooth' });
        isTransitioning = false;
        showToast(`Welcome back, ${name}. Autonomous cockpit active.`, 'success');
      }, 350);
    }

    function transitionToAuth() {
      if (isTransitioning) return;
      isTransitioning = true;

      dashboardView.classList.remove('active');

      setTimeout(() => {
        dashboardView.classList.add('hidden');
        authView.style.display = 'flex';
        authCard.classList.remove('dissolve-exit');
        void authCard.offsetWidth;
        isTransitioning = false;
        showToast('Signed out of session.', 'info');
      }, 350);
    }

    btnGoogleAuth?.addEventListener('click', async () => {
      btnGoogleAuth.disabled = true;
      btnAuthLabel.textContent = "Connecting with Google...";
      trailingArrow.classList.add('hidden');
      btnAuthSpinner.classList.remove('hidden');

      try {
        await signInWithPopup(auth, provider);
      } catch (err) {
        console.error("Auth error:", err);
        let msg = "Could not authenticate with Google.";
        if (err.code === 'auth/popup-closed-by-user') msg = "Sign-in popup was closed.";
        else if (err.code === 'auth/popup-blocked') msg = "Popup was blocked by browser.";
        authFeedback.textContent = msg;
        authFeedback.className = "text-xs font-medium rounded-xl p-3 mt-4 text-left bg-rose-50 text-rose-700 border border-rose-200 block";
      } finally {
        btnGoogleAuth.disabled = false;
        btnAuthLabel.textContent = "Continue with Google";
        trailingArrow.classList.remove('hidden');
        btnAuthSpinner.classList.add('hidden');
      }
    });

    btnDemoEnter?.addEventListener('click', () => {
      transitionToDashboard({
        uid: 'demo-user',
        displayName: "Kai Sterling",
        email: "kai.sterling@savemoneymanually.app",
        photoURL: null
      });
    });

    btnDashSignout?.addEventListener('click', async () => {
      try {
        await signOut(auth);
      } catch (e) {}
      transitionToAuth();
    });

    window.triggerAuthDashboard = (user) => {
      transitionToDashboard(user);
    };

    onAuthStateChanged(auth, (user) => {
      if (user) {
        if (!window.isVaultPhase2Complete) {
          window.pendingAuthUser = user;
        } else {
          transitionToDashboard(user);
        }
      }
    });

  </script>
"""
