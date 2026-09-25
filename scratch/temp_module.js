
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
      getDoc,
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
    const dashboardView = document.getElementById('dashboard-view');
    const btnGoogleAuth = document.getElementById('btn-google-auth');
    const btnAuthLabel = document.getElementById('btn-auth-label');
    const btnAuthSpinner = document.getElementById('btn-auth-spinner');
    const btnDemoEnter = document.getElementById('btn-demo-enter');
    const authFeedback = document.getElementById('auth-feedback');
    const dashUserAvatar = document.getElementById('dash-user-avatar');
    const dashUserAvatarMobile = document.getElementById('dash-user-avatar-mobile');
    const dashUserName = document.getElementById('dash-user-name');
    const btnDashSignout = document.getElementById('btn-dash-signout');
    const btnDashSignoutMobile = document.getElementById('btn-dash-signout-mobile');

    // Application State (100% CLEAN - ZERO DUMMY DATA)
    let currentUser = null;
    let isDemoMode = false;
    let goals = [];
    let ledger = [];
    let currentCalDate = new Date();
    let selectedGoalCadence = 'DAILY';
    let ledgerFilter = 'ALL';
    let currentTab = 'home';

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
        el.style.transform = 'translateY(-6px)';
        el.style.transition = 'all 0.25s ease';
        setTimeout(() => el.remove(), 250);
      }, 3000);
    }

    // Anti-spam single-click lock utility
    const SPIN_SVG = `<svg class="w-4 h-4 animate-spin flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>`;
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

    // Storage key & resilience
    const STORAGE_KEY = 'vaultfi_spa_clean_store_v1';
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

    // ============================================================
    // LOWER NAVIGATION ROUTER: ZERO-RELOAD DOM SWITCHING
    // ============================================================
    const TABS = ['home', 'goals', 'calendar', 'ledger'];

    function switchTab(targetTab) {
      if (!TABS.includes(targetTab)) targetTab = 'home';
      currentTab = targetTab;

      // 1. Instantaneous view container visibility toggle
      TABS.forEach(t => {
        const viewEl = document.getElementById(`view-${t}`);
        if (viewEl) {
          if (t === targetTab) {
            viewEl.classList.remove('hidden');
            viewEl.classList.add('dissolve-enter');
          } else {
            viewEl.classList.add('hidden');
            viewEl.classList.remove('dissolve-enter');
          }
        }
      });

      // 2. Update Mobile Bottom Navigation Dock items
      TABS.forEach(t => {
        const mBtn = document.getElementById(`tab-${t}`);
        if (mBtn) {
          const dot = mBtn.querySelector('.active-dot');
          if (t === targetTab) {
            mBtn.className = 'mobile-nav-item flex-1 flex flex-col items-center justify-center py-1.5 text-blue-600 font-bold transition-all cursor-pointer';
            if (dot) dot.classList.remove('opacity-0');
          } else {
            mBtn.className = 'mobile-nav-item flex-1 flex flex-col items-center justify-center py-1.5 text-slate-500 font-medium transition-all cursor-pointer';
            if (dot) dot.classList.add('opacity-0');
          }
        }
      });

      // 3. Update Desktop Sidebar Lower Rail items
      TABS.forEach(t => {
        const dBtn = document.getElementById(`tab-${t}-desktop`);
        if (dBtn) {
          const dot = dBtn.querySelector('.active-dot');
          if (t === targetTab) {
            dBtn.className = 'desktop-nav-item w-full flex items-center justify-between px-3.5 py-3 rounded-xl text-xs font-bold transition-all cursor-pointer bg-blue-50/90 text-blue-600 border border-blue-200/80 shadow-xs';
            if (dot) dot.classList.remove('opacity-0');
          } else {
            dBtn.className = 'desktop-nav-item w-full flex items-center justify-between px-3.5 py-3 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent';
            if (dot) dot.classList.add('opacity-0');
          }
        }
      });

      // 4. Trigger specific view refresh
      if (targetTab === 'home') renderHomeView();
      if (targetTab === 'goals') renderGoalsGrid();
      if (targetTab === 'calendar') renderSavingsCalendar();
      if (targetTab === 'ledger') renderLedger();

      window.scrollTo({ top: 0, behavior: 'instant' });
    }

    // Attach click listeners to all tab switches across mobile dock and desktop rail
    document.querySelectorAll('.mobile-nav-item, .desktop-nav-item, .nav-switch-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.dataset.target;
        if (target) switchTab(target);
      });
    });

    // ============================================================
    // DATA PERSISTENCE & REAL-TIME FIRESTORE SYNC
    // ============================================================
    function initDataSync(user) {
      currentUser = user;
      isDemoMode = !user || user.uid === 'demo-user';

      let stored = getLocalData();
      if (!stored) {
        stored = { goals: [], ledger: [] };
        saveLocalData(stored);
      }
      goals = stored.goals || [];
      ledger = stored.ledger || [];
      renderAll();

      if (isDemoMode || !db) return;

      try {
        if (unsubGoals) unsubGoals();
        if (unsubLedger) unsubLedger();

        const goalsCol = collection(db, 'users', user.uid, 'goals');
        unsubGoals = onSnapshot(goalsCol, (snapshot) => {
          goals = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
          saveLocalData({ goals, ledger });
          renderAll();
        }, (err) => console.warn("Goals snapshot note:", err.message));

        const ledgerCol = collection(db, 'users', user.uid, 'ledger');
        unsubLedger = onSnapshot(ledgerCol, (snapshot) => {
          ledger = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
          saveLocalData({ goals, ledger });
          renderAll();
        }, (err) => console.warn("Ledger snapshot note:", err.message));
      } catch (e) {
        console.warn("Sync warning:", e);
      }
    }

    function persistGoal(goalData) {
      const newGoal = {
        id: 'goal-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4),
        ...goalData,
        createdAt: new Date().toISOString()
      };
      goals.push(newGoal);
      saveLocalData({ goals, ledger });
      renderAll();

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const col = collection(db, 'users', currentUser.uid, 'goals');
        addDoc(col, { ...goalData, createdAt: serverTimestamp() }).catch(e => console.warn("Background goal save:", e));
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

      ledger.unshift(newEntry);

      const targetGoal = goals.find(g => g.id === entryData.goalId || g.name.toLowerCase() === (entryData.goalName || '').toLowerCase());
      if (targetGoal) {
        targetGoal.currentAmount = Math.max(0, (Number(targetGoal.currentAmount) || 0) + delta);
      }

      saveLocalData({ goals, ledger });
      renderAll();

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const col = collection(db, 'users', currentUser.uid, 'ledger');
        addDoc(col, { ...entryData, timestamp: serverTimestamp() }).catch(e => console.warn("Background ledger save:", e));

        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal update:", e));
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

      existing.amount = newAmount;
      existing.note = newNote;
      existing.date = newDate;

      if (targetGoal) {
        targetGoal.currentAmount = Math.max(0, (Number(targetGoal.currentAmount) || 0) + goalDelta);
      }

      saveLocalData({ goals, ledger });
      renderAll();

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const ref = doc(db, 'users', currentUser.uid, 'ledger', id);
        updateDoc(ref, { amount: newAmount, note: newNote, date: newDate }).catch(e => console.warn("Ledger update:", e));

        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal update:", e));
        }
      }
    }

    function deleteLedgerEntry(id) {
      const existing = ledger.find(item => item.id === id);
      if (!existing) return;

      const isAdd = existing.type === 'ADD';
      const reversalDelta = isAdd ? -Number(existing.amount) : Number(existing.amount);
      const targetGoal = goals.find(g => g.id === existing.goalId || g.name === existing.goalName);

      ledger = ledger.filter(item => item.id !== id);

      if (targetGoal) {
        targetGoal.currentAmount = Math.max(0, (Number(targetGoal.currentAmount) || 0) + reversalDelta);
      }

      saveLocalData({ goals, ledger });
      renderAll();

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const ref = doc(db, 'users', currentUser.uid, 'ledger', id);
        deleteDoc(ref).catch(e => console.warn("Ledger delete:", e));

        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal update:", e));
        }
      }
    }

    // ============================================================
    // RENDERING ENGINES ACROSS ALL 4 CORE VIEWS
    // ============================================================
    function renderAll() {
      renderCommandMetrics();
      renderHomeView();
      renderGoalsGrid();
      renderSavingsCalendar();
      renderLedger();
      renderGoalSelectors();
    }

    // View 1: Home Helpers
    function renderCommandMetrics() {
      let totalNet = 0;
      let monthSaved = 0;
      const curYear = new Date().getFullYear();
      const curMonth = new Date().getMonth();

      ledger.forEach(item => {
        const amt = Number(item.amount) || 0;
        const isAdd = item.type === 'ADD';
        if (isAdd) totalNet += amt;
        else totalNet -= amt;

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
      if (elVaults) elVaults.textContent = `${goals.length}`;

      const elMonth = document.getElementById('metric-month-saved');
      if (elMonth) elMonth.textContent = '\u20b9' + Math.max(0, monthSaved).toLocaleString('en-IN');

      const calStreak = document.getElementById('cal-streak-badge');
      if (calStreak) calStreak.textContent = `${streak} Days 🔥`;
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

    function renderHomeView() {
      renderCommandMetrics();

      // Render AI Pacing Guardrail Banner
      const banner = document.getElementById('ai-pacing-banner');
      const icon = document.getElementById('ai-pacing-icon');
      const headline = document.getElementById('ai-pacing-headline');
      const detail = document.getElementById('ai-pacing-detail');
      const elDaily = document.getElementById('ai-quota-daily');
      const elMonth = document.getElementById('ai-quota-monthly');
      const elDays = document.getElementById('ai-days-remaining');
      const elEta = document.getElementById('ai-projected-eta');

      const activeGoal = goals[0];
      if (!activeGoal) {
        if (banner) {
          banner.className = 'mt-4 p-4 rounded-2xl pacing-banner-optimal transition-all duration-300';
          icon.textContent = '🎯';
          headline.textContent = 'On schedule: No active goal bottlenecks';
          detail.textContent = 'Create your first target vault to activate precision pacing guardrails.';
        }
        if (elDaily) elDaily.textContent = '\u20b90 / day';
        if (elMonth) elMonth.textContent = '\u20b90 / mo';
        if (elDays) elDays.textContent = '0 Days';
        if (elEta) elEta.textContent = '--';
      } else {
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

        if (cur >= tgt) {
          banner.className = 'mt-4 p-4 rounded-2xl pacing-banner-optimal transition-all duration-300';
          icon.textContent = '🏆';
          headline.textContent = `Target Hit: "${activeGoal.name}" is 100% achieved!`;
          detail.textContent = `You reached \u20b9${tgt.toLocaleString('en-IN')}. Create a new target to maintain momentum.`;
        } else if (recentDailyVelocity >= dailyQuota && recentDailyVelocity > 0) {
          const earlyDays = Math.max(1, Math.round(daysLeft - (remain / recentDailyVelocity)));
          banner.className = 'mt-4 p-4 rounded-2xl pacing-banner-optimal transition-all duration-300';
          icon.textContent = '⚡';
          headline.textContent = `Pacing Optimal: Projected to hit "${activeGoal.name}" ${earlyDays} days early!`;
          detail.textContent = `Current velocity is \u20b9${recentDailyVelocity.toLocaleString('en-IN')}/day vs required \u20b9${dailyQuota.toLocaleString('en-IN')}/day.`;
        } else if (recentDailyVelocity < dailyQuota * 0.75 && recentSum > 0) {
          const gap = Math.max(30, dailyQuota - recentDailyVelocity);
          banner.className = 'mt-4 p-4 rounded-2xl pacing-banner-warning transition-all duration-300';
          icon.textContent = '⚠️';
          headline.textContent = `Pacing gap: Add \u20b9${gap.toLocaleString('en-IN')} today to retain schedule for "${activeGoal.name}".`;
          detail.textContent = `Target deadline is ${activeGoal.deadline || 'upcoming'}. Increasing daily stash closes the gap.`;
        } else {
          banner.className = 'mt-4 p-4 rounded-2xl pacing-banner-optimal transition-all duration-300';
          icon.textContent = '🎯';
          headline.textContent = `On schedule: Save \u20b9${dailyQuota.toLocaleString('en-IN')} / day for "${activeGoal.name}".`;
          detail.textContent = `Formula: \u20b9${remain.toLocaleString('en-IN')} remaining / ${daysLeft} days = \u20b9${dailyQuota.toLocaleString('en-IN')}/day.`;
        }

        if (elDaily) elDaily.textContent = `\u20b9${dailyQuota.toLocaleString('en-IN')} / day`;
        if (elMonth) elMonth.textContent = `\u20b9${monthlyQuota.toLocaleString('en-IN')} / mo`;
        if (elDays) elDays.textContent = `${daysLeft} Days`;

        const effVelocity = recentDailyVelocity > 0 ? recentDailyVelocity : dailyQuota;
        const projDays = effVelocity > 0 ? Math.ceil(remain / effVelocity) : daysLeft;
        const projDate = new Date(Date.now() + projDays * 86400000);
        if (elEta) elEta.textContent = projDate.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' });
      }

      // Render Recent Activity on Home
      const recentContainer = document.getElementById('home-recent-ledger');
      if (recentContainer) {
        const top3 = ledger.slice(0, 3);
        if (top3.length === 0) {
          recentContainer.innerHTML = '<div class="py-4 text-center text-xs text-coolslate">No entries logged yet. Tap [+ Add Saved] above.</div>';
        } else {
          recentContainer.innerHTML = top3.map(item => {
            const isAdd = item.type === 'ADD';
            const colorCls = isAdd ? 'text-cobalt' : 'text-crimson';
            const sign = isAdd ? '+' : '-';
            const badgeCls = isAdd ? 'ledger-badge-add' : 'ledger-badge-minus';
            return `
              <div class="glass-inner-tile p-3 flex items-center justify-between">
                <div class="flex items-center gap-2.5 min-w-0">
                  <span class="text-[9px] font-mono font-bold px-2 py-0.5 rounded-full ${badgeCls}">${isAdd ? '+ ADD' : '- MINUS'}</span>
                  <div class="truncate">
                    <div class="text-xs font-bold text-charcoal truncate">${item.goalName || 'General Stash'}</div>
                    <div class="text-[10px] text-coolslate">${item.date || 'Today'}</div>
                  </div>
                </div>
                <div class="font-mono font-extrabold ${colorCls} text-sm">${sign}&#8377;${Number(item.amount).toLocaleString('en-IN')}</div>
              </div>
            `;
          }).join('');
        }
      }
    }

    // View 2: Goal Vaults Helper
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
          <div class="metallic-card p-4 sm:p-5 flex flex-col justify-between">
            <div>
              <div class="flex items-start justify-between gap-2 mb-3">
                <div class="flex items-center gap-2.5">
                  <div class="w-8 h-8 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center text-cobalt flex-shrink-0 shadow-xs">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                  </div>
                  <div>
                    <h4 class="font-extrabold text-charcoal text-sm leading-tight">${g.name}</h4>
                    <span class="text-[10px] font-mono font-bold text-cobalt uppercase tracking-wide">${g.cadence || 'DAILY'} &bull; ${quotaStr}</span>
                  </div>
                </div>
                <span class="font-mono text-xs font-bold text-coolslate bg-slate-50 border border-slate-200 px-2 py-0.5 rounded-lg">${pct}%</span>
              </div>

              <!-- Metallic Liquid Shimmer Progress -->
              <div class="progress-track my-2.5">
                <div class="progress-fill-shimmer" style="width: ${pct}%;"></div>
              </div>

              <div class="flex items-baseline justify-between text-xs mb-2">
                <span class="font-mono font-extrabold text-charcoal text-base">&#8377;${cur.toLocaleString('en-IN')}</span>
                <span class="text-coolslate font-mono text-[11px]">of &#8377;${tgt.toLocaleString('en-IN')}</span>
              </div>

              <div class="text-[10px] font-mono text-coolslate flex items-center gap-1.5 mb-3.5">
                <span>⏳</span>
                <span>${daysLeft} days left &bull; Due ${g.deadline || 'Ongoing'}</span>
              </div>
            </div>

            <div class="pt-2.5 border-t border-slate-100">
              <button class="btn-primary-metallic text-xs min-h-[44px] py-2 px-3 w-full btn-quick-goal-stash" data-goal-id="${g.id}" data-goal-name="${g.name}" type="button">
                + Add Funds
              </button>
            </div>
          </div>
        `;
      }).join('');

      container.querySelectorAll('.btn-quick-goal-stash').forEach(btn => {
        btn.addEventListener('click', () => {
          openAddSavingsModal(btn.dataset.goalName);
        });
      });
    }

    // View 3: Savings Calendar Helper
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
          <div class="${classes}" data-date="${dateKey}" title="${hasSaved ? 'Saved: \u20b9' + savedAmount.toLocaleString('en-IN') : 'No deposit'}">
            <span class="cal-day-num ${isToday ? 'font-extrabold text-cobalt' : ''}">${d}</span>
            ${hasSaved ? `<span class="cal-day-badge">+\u20b9${savedAmount >= 1000 ? (savedAmount/1000).toFixed(savedAmount%1000===0?0:1) + 'k' : savedAmount}</span>` : '<span class="text-[8px] text-slate-300 leading-none">&bull;</span>'}
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
      const pct = Math.round((activeDaysCount / daysInMonth) * 100);
      if (rateEl) rateEl.textContent = `${pct}%`;

      grid.querySelectorAll('.cal-active-saved').forEach(cell => {
        cell.addEventListener('click', () => {
          const dateStr = cell.dataset.date;
          const dayEntries = ledger.filter(item => item.date === dateStr && item.type === 'ADD');
          const totalDay = dayEntries.reduce((s, e) => s + Number(e.amount), 0);
          showToast(`📅 ${dateStr}: \u20b9${totalDay.toLocaleString('en-IN')} deposited!`, 'info');
        });
      });
    }

    // View 4: Ledger & History Helper
    function renderLedger() {
      const mobileCards = document.getElementById('ledger-mobile-cards');
      const tbody = document.getElementById('ledger-table-body');
      const emptyState = document.getElementById('ledger-empty-state');

      let filtered = [...ledger];
      if (ledgerFilter === 'ADD') filtered = filtered.filter(i => i.type === 'ADD');
      if (ledgerFilter === 'MINUS') filtered = filtered.filter(i => i.type === 'MINUS');

      filtered.sort((a, b) => new Date(b.date || b.timestamp) - new Date(a.date || a.timestamp));

      if (filtered.length === 0) {
        if (mobileCards) mobileCards.innerHTML = '';
        if (tbody) tbody.innerHTML = '';
        if (emptyState) emptyState.classList.remove('hidden');
        return;
      }
      if (emptyState) emptyState.classList.add('hidden');

      // A. Mobile Stacked Cards
      if (mobileCards) {
        mobileCards.innerHTML = filtered.map(item => {
          const isAdd = item.type === 'ADD';
          const amt = Number(item.amount) || 0;
          const sign = isAdd ? '+' : '-';
          const colorCls = isAdd ? 'text-cobalt font-extrabold' : 'text-crimson font-extrabold';
          const badgeCls = isAdd ? 'ledger-badge-add' : 'ledger-badge-minus';
          const badgeLabel = isAdd ? '+ ADD' : '- WITHDRAW';

          return `
            <div class="glass-inner-tile p-3.5 flex flex-col gap-2 relative" data-id="${item.id}">
              <div class="flex items-center justify-between">
                <div class="text-[11px] font-mono text-coolslate">🗓️ ${item.date || 'Today'}</div>
                <span class="text-[9px] font-mono font-bold px-2.5 py-0.5 rounded-full ${badgeCls}">${badgeLabel}</span>
              </div>
              <div class="flex items-baseline justify-between gap-2">
                <div class="min-w-0 flex-1">
                  <div class="font-extrabold text-charcoal text-sm truncate">${item.goalName || 'General Stash'}</div>
                  ${item.note ? `<div class="text-[11px] text-coolslate truncate mt-0.5">${item.note}</div>` : ''}
                </div>
                <div class="font-mono ${colorCls} text-base font-extrabold flex-shrink-0">
                  ${sign}&#8377;${amt.toLocaleString('en-IN')}
                </div>
              </div>
              <div class="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                <button class="btn-edit-entry flex items-center gap-1 text-[11px] font-bold text-cobalt bg-blue-50 px-3 py-1.5 rounded-lg cursor-pointer min-h-[36px]" data-id="${item.id}" type="button">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
                  <span>Edit</span>
                </button>
                <button class="btn-del-entry flex items-center gap-1 text-[11px] font-bold text-crimson bg-rose-50 px-3 py-1.5 rounded-lg cursor-pointer min-h-[36px]" data-id="${item.id}" type="button">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                  <span>Delete</span>
                </button>
              </div>
            </div>
          `;
        }).join('');
      }

      // B. Desktop Table
      if (tbody) {
        tbody.innerHTML = filtered.map(item => {
          const isAdd = item.type === 'ADD';
          const amt = Number(item.amount) || 0;
          const sign = isAdd ? '+' : '-';
          const colorCls = isAdd ? 'text-cobalt font-extrabold' : 'text-crimson font-extrabold';
          const badgeCls = isAdd ? 'ledger-badge-add' : 'ledger-badge-minus';
          const badgeLabel = isAdd ? '+ ADD' : '- WITHDRAW';

          return `
            <tr class="hover:bg-slate-50 transition-colors">
              <td class="py-3 px-3 font-mono text-coolslate text-[11px] whitespace-nowrap">${item.date || 'Today'}</td>
              <td class="py-3 px-3 font-bold text-charcoal max-w-[140px] truncate">${item.goalName || 'General Stash'}</td>
              <td class="py-3 px-3">
                <span class="text-[9px] font-mono font-bold px-2.5 py-0.5 rounded-full ${badgeCls}">${badgeLabel}</span>
              </td>
              <td class="py-3 px-3 text-coolslate max-w-[180px] truncate">${item.note || '--'}</td>
              <td class="py-3 px-3 text-right font-mono ${colorCls} text-sm">${sign}&#8377;${amt.toLocaleString('en-IN')}</td>
              <td class="py-3 px-3 text-right whitespace-nowrap space-x-1">
                <button class="btn-edit-entry text-[11px] font-semibold text-cobalt hover:bg-blue-50 px-2.5 py-1 rounded-lg transition-colors cursor-pointer" data-id="${item.id}" type="button">Edit</button>
                <button class="btn-del-entry text-[11px] font-semibold text-crimson hover:bg-rose-50 px-2.5 py-1 rounded-lg transition-colors cursor-pointer" data-id="${item.id}" type="button">Delete</button>
              </td>
            </tr>
          `;
        }).join('');
      }

      document.querySelectorAll('.btn-edit-entry').forEach(btn => {
        btn.addEventListener('click', () => openEditLedgerModal(btn.dataset.id));
      });
      document.querySelectorAll('.btn-del-entry').forEach(btn => {
        btn.addEventListener('click', () => openDeleteLedgerModal(btn.dataset.id));
      });
    }

    function renderGoalSelectors() {
      const withSel = document.getElementById('withdrawal-vault-select');
      if (withSel) {
        if (goals.length === 0) {
          withSel.innerHTML = '<option value="">No vaults created yet</option>';
        } else {
          withSel.innerHTML = goals.map(g => `<option value="${g.id}">${g.name} (\u20b9${(g.currentAmount || 0).toLocaleString('en-IN')} available)</option>`).join('');
        }
      }
    }

    // ============================================================
    // MODAL DIALOGS & ANTI-SPAM SINGLE-CLICK FORMS
    // ============================================================
    function closeModals() {
      document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('open'));
    }
    document.querySelectorAll('.modal-close').forEach(btn => btn.addEventListener('click', closeModals));
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeModals();
      });
    });
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeModals();
    });

    // 1. Create Goal Vault Modal
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
        goalMathText.textContent = "Enter amount and deadline to compute your required quota: Remaining / Days.";
        return;
      }

      const diff = new Date(deadVal) - new Date();
      const days = Math.max(1, Math.ceil(diff / (1000 * 60 * 60 * 24)));
      const daily = Math.round(amt / days);
      const monthly = Math.round(daily * 30.4);

      goalMathText.innerHTML = `
        <div class="font-extrabold text-slate-900 text-xs">Save &#8377;${daily.toLocaleString('en-IN')} / day or &#8377;${monthly.toLocaleString('en-IN')} / month to hit goal on time.</div>
        <div class="text-[11px] text-cobalt mt-0.5 font-medium">Formula: &#8377;${amt.toLocaleString('en-IN')} target &divide; ${days} remaining days.</div>
      `;
    }

    goalInputAmount?.addEventListener('input', updateGoalLiveMath);
    goalInputDeadline?.addEventListener('input', updateGoalLiveMath);

    document.querySelectorAll('.btn-cadence-toggle').forEach(btn => {
      btn.addEventListener('click', () => {
        selectedGoalCadence = btn.dataset.cadence;
        document.querySelectorAll('.btn-cadence-toggle').forEach(b => {
          b.className = 'btn-cadence-toggle min-h-[48px] py-2 px-3 text-xs font-bold rounded-xl border border-slate-200 bg-white text-coolslate transition-all cursor-pointer';
        });
        btn.className = 'btn-cadence-toggle min-h-[48px] py-2 px-3 text-xs font-bold rounded-xl border border-cobalt bg-blue-50 text-cobalt transition-all cursor-pointer';
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

      lockBtn(btnCreateGoalSubmit, 'Locking...');

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
        showToast(`🎯 Goal Vault "${name}" created!`, 'success');
        switchTab('goals');
      }, 120);
    });

    const openCreateGoalModal = () => {
      modalCreateGoal.classList.add('open');
      setTimeout(() => goalInputName.focus(), 250);
    };

    document.getElementById('btn-quick-new-vault')?.addEventListener('click', openCreateGoalModal);
    document.getElementById('btn-grid-new-vault')?.addEventListener('click', openCreateGoalModal);
    document.getElementById('btn-empty-new-vault')?.addEventListener('click', openCreateGoalModal);

    // 2. Add Savings Modal (+ Deposit)
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
        addVaultInput.placeholder = 'e.g. MacBook Pro, Emergency Cash…';
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
      addVaultInput.placeholder = 'e.g. MacBook Pro, Emergency Cash…';
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
          <span>🎯</span>
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
        document.querySelectorAll('.btn-add-preset').forEach(b => b.classList.remove('border-cobalt', 'text-cobalt', 'bg-blue-50'));
        btn.classList.add('border-cobalt', 'text-cobalt', 'bg-blue-50');
      });
    });

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

      lockBtn(btnAddSavingsSubmit, 'Stashing...');

      const goalMatch = goals.find(g => g.name.toLowerCase() === vaultName.toLowerCase());
      const goalId = goalMatch ? goalMatch.id : 'custom-' + Date.now();

      persistLedgerEntry({
        goalId,
        goalName: vaultName,
        type: 'ADD',
        amount: amt,
        note,
        date
      });

      setTimeout(() => {
        modalAddSavings.classList.remove('open');
        clearAddChip();
        addAmountInput.value = '';
        addNoteInput.value = '';
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
      } else {
        clearAddChip();
      }
      setTimeout(() => addAmountInput.focus(), 250);
    }

    document.getElementById('btn-quick-add-savings')?.addEventListener('click', () => openAddSavingsModal());

    // 3. Record Emergency Withdrawal Modal (- Deduction)
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

      lockBtn(btnWithdrawalSubmit, 'Recording...');

      const goalMatch = goals.find(g => g.id === goalId);
      const goalName = goalMatch ? goalMatch.name : 'Vault';

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
        showToast(`-₹${amt.toLocaleString('en-IN')} withdrawal logged from "${goalName}".`, 'info');
      }, 120);
    });

    const openWithdrawalModal = () => {
      modalWithdrawal.classList.add('open');
      setTimeout(() => withAmountInput?.focus(), 250);
    };

    document.getElementById('btn-quick-withdrawal')?.addEventListener('click', openWithdrawalModal);

    // 4. Edit Ledger Entry Modal
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
      editEntryTypeBadge.textContent = entry.type === 'ADD' ? '+ ADD' : '- WITHDRAW';
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

      lockBtn(btnEditLedgerSubmit, 'Saving...');
      updateLedgerEntry(id, amt, note, date);

      setTimeout(() => {
        unlockBtn(btnEditLedgerSubmit);
        modalEditLedger.classList.remove('open');
        showToast('Entry updated!', 'success');
      }, 120);
    });

    // 5. Delete Ledger Confirmation Modal
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
      delPreviewAmount.className = entry.type === 'ADD' ? 'font-mono text-cobalt font-bold' : 'font-mono text-crimson font-bold';
      delPreviewNote.textContent = entry.note || '--';

      modalDeleteLedger.classList.add('open');
    }

    btnDeleteLedgerConfirm?.addEventListener('click', () => {
      const id = deleteEntryId.value;
      if (!id) return;

      lockBtn(btnDeleteLedgerConfirm, 'Deleting...');
      deleteLedgerEntry(id);

      setTimeout(() => {
        unlockBtn(btnDeleteLedgerConfirm);
        modalDeleteLedger.classList.remove('open');
        showToast('Entry deleted & balance reversed.', 'info');
      }, 120);
    });

    // Calendar Navigation
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

    // Ledger Filters
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
        if (!btn) return;
        if (id === activeId) {
          btn.className = 'text-xs font-bold px-3 py-1.5 rounded-lg bg-white text-charcoal shadow-xs transition-all cursor-pointer min-h-[34px]';
        } else {
          btn.className = 'text-xs font-bold px-3 py-1.5 rounded-lg text-coolslate hover:text-charcoal transition-all cursor-pointer min-h-[34px]';
        }
      });
    }

    // ============================================================
    // AUTHENTICATION TRANSITION
    // ============================================================
    function enterDashboard(userData) {
      const name = userData.displayName || userData.email?.split('@')[0] || "Saver";
      if (dashUserName) dashUserName.textContent = name;
      if (userData.photoURL) {
        if (dashUserAvatar) dashUserAvatar.innerHTML = `<img src="${userData.photoURL}" alt="${name}" class="w-full h-full object-cover rounded-xl" />`;
        if (dashUserAvatarMobile) dashUserAvatarMobile.innerHTML = `<img src="${userData.photoURL}" alt="${name}" class="w-full h-full object-cover rounded-full" />`;
      } else {
        const initial = (name[0] || 'S').toUpperCase();
        if (dashUserAvatar) dashUserAvatar.textContent = initial;
        if (dashUserAvatarMobile) dashUserAvatarMobile.textContent = initial;
      }

      initDataSync(userData);

      authView.style.display = 'none';
      dashboardView.classList.remove('hidden');
      switchTab('home');
      showToast(`Welcome back, ${name}. Cockpit online.`, 'success');
    }

    function exitToAuth() {
      dashboardView.classList.add('hidden');
      authView.style.display = 'flex';
      showToast('Signed out of session.', 'info');
    }

    btnDemoEnter?.addEventListener('click', () => {
      enterDashboard({
        uid: 'demo-user',
        displayName: 'Saver',
        email: 'user@vault.fi',
        photoURL: null
      });
    });

    btnGoogleAuth?.addEventListener('click', async () => {
      btnGoogleAuth.disabled = true;
      btnAuthLabel.textContent = "Connecting...";
      btnAuthSpinner.classList.remove('hidden');

      try {
        await signInWithPopup(auth, provider);
      } catch (err) {
        console.error("Auth error:", err);
        let msg = "Could not authenticate with Google.";
        if (err.code === 'auth/popup-closed-by-user') msg = "Popup closed.";
        authFeedback.textContent = msg;
        authFeedback.classList.remove('hidden');
      } finally {
        btnGoogleAuth.disabled = false;
        btnAuthLabel.textContent = "Sign In with Google";
        btnAuthSpinner.classList.add('hidden');
      }
    });

    btnDashSignout?.addEventListener('click', async () => {
      try { await signOut(auth); } catch (e) {}
      exitToAuth();
    });
    btnDashSignoutMobile?.addEventListener('click', async () => {
      try { await signOut(auth); } catch (e) {}
      exitToAuth();
    });

    onAuthStateChanged(auth, (user) => {
      if (user) {
        enterDashboard(user);
      }
    });

    // Auto-enter demo if previously in session
    if (localStorage.getItem(STORAGE_KEY)) {
      enterDashboard({
        uid: 'demo-user',
        displayName: 'Saver',
        email: 'user@vault.fi',
        photoURL: null
      });
    }

  