
    import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
    import {
      getAuth,
      signInWithPopup,
      GoogleAuthProvider,
      onAuthStateChanged,
      setPersistence,
      browserLocalPersistence,
      signOut
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
      getDocs, onSnapshot,
      query,
      orderBy, limit,
      serverTimestamp,
      increment
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

    // Storage key & resilience (User-isolated with legacy fallback)
    function getStorageKey() {
      const uid = currentUser?.uid || (isDemoMode ? 'demo-user' : 'guest');
      return `smm_store_${uid}`;
    }
    function getLocalData() {
      try {
        const userKey = getStorageKey();
        const raw = localStorage.getItem(userKey);
        if (raw) return JSON.parse(raw);
        // Fallback to legacy global key
        const legacy = localStorage.getItem('vaultfi_spa_clean_store_v1');
        return legacy ? JSON.parse(legacy) : null;
      } catch (e) {
        return null;
      }
    }
    function saveLocalData(data) {
      try {
        localStorage.setItem(getStorageKey(), JSON.stringify(data));
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
    // DATA PERSISTENCE & REAL-TIME FIRESTORE SYNC (onSnapshot PIPELINE)
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

      if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('connecting');
      try {
        if (unsubGoals) unsubGoals();
        if (unsubLedger) unsubLedger();

        // 1. Real-time Goals onSnapshot Listener
        const goalsCol = collection(db, 'users', user.uid, 'goals');
        unsubGoals = onSnapshot(goalsCol, (snapshot) => {
          console.log("Realtime Sync Triggered [Goals]:", snapshot.size, "records");
          if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('active', 'Firestore Realtime Active');
          goals = snapshot.docs.map(docSnap => ({ id: docSnap.id, ...docSnap.data() }));
          saveLocalData({ goals, ledger });
          renderAll();
        }, (err) => {
          console.error("Firestore Goals onSnapshot error:", err);
          if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('error', 'Goals Sync Failed: ' + err.code);
        });

        // 2. Real-time Ledger onSnapshot Listener (ordered by timestamp desc)
        const ledgerCol = collection(db, 'users', user.uid, 'ledger');
        const ledgerQuery = query(ledgerCol, orderBy('timestamp', 'desc'));

        const handleLedgerSnapshot = (snapshot) => {
          console.log("Realtime Sync Triggered [Ledger]:", snapshot.size, "records");
          if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('active', 'Firestore Realtime Active');
          ledger = snapshot.docs.map(docSnap => {
            const data = docSnap.data();
            return {
              id: docSnap.id,
              ...data,
              amount: Number(data.amount) || 0,
              timestamp: data.timestamp?.toDate ? data.timestamp.toDate().toISOString() : (data.timestamp || new Date().toISOString())
            };
          });

          // Sort descending by date & timestamp
          ledger.sort((a, b) => new Date(b.date || b.timestamp) - new Date(a.date || a.timestamp));

          // Calculate current net capital: ADD adds, MINUS subtracts
          let runningTotal = 0;
          ledger.forEach(entry => {
            const amt = Number(entry.amount) || 0;
            if (entry.type === 'ADD') runningTotal += amt;
            else if (entry.type === 'MINUS') runningTotal -= amt;
          });
          if (runningTotal < 0) runningTotal = 0;

          // Immediately update #totalStashedDisplay with formatted sum
          const elTotal = document.getElementById('totalStashedDisplay') || document.getElementById('metric-total-capital');
          if (elTotal) elTotal.textContent = '₹' + runningTotal.toLocaleString('en-IN');

          saveLocalData({ goals, ledger });
          renderAll();
        };

        unsubLedger = onSnapshot(ledgerQuery, handleLedgerSnapshot, (err) => {
          console.error("Firestore Ledger onSnapshot error:", err);
          if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('error', 'Ledger Sync Failed: ' + (err.code || err.message));
          // Resilient fallback without order clause if index is building
          if (err.code === 'failed-precondition' || err.message?.includes('index')) {
            console.warn("Retrying ledger onSnapshot with base collection fallback...");
            unsubLedger = onSnapshot(ledgerCol, handleLedgerSnapshot, (fallbackErr) => {
              console.error("Firestore Ledger fallback onSnapshot error:", fallbackErr);
              if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('error', 'Fallback Sync Failed');
            });
          }
        });
      } catch (e) {
        console.error("Firestore sync initialization error:", e);
      }
    }

    async function persistGoal(goalData) {
      const localId = 'goal-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4);
      const newGoal = {
        id: localId,
        ...goalData,
        createdAt: new Date().toISOString()
      };
      goals.push(newGoal);
      saveLocalData({ goals, ledger });
      renderAll();

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const col = collection(db, 'users', currentUser.uid, 'goals');
        const docRef = await addDoc(col, { ...goalData, createdAt: serverTimestamp() });
        return { ...newGoal, id: docRef.id };
      }
      return newGoal;
    }

    async function persistLedgerEntry(entryData) {
      const isAdd = entryData.type === 'ADD';
      const amt = Number(entryData.amount) || 0;
      const delta = isAdd ? amt : -amt;

      // Optimistic local update
      const localId = 'tx-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4);
      const newEntry = {
        id: localId,
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

      // Real-time atomic Firestore write
      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        const ledgerCol = collection(db, 'users', currentUser.uid, 'ledger');
        const docRef = await addDoc(ledgerCol, {
          type: entryData.type,
          amount: amt,
          note: entryData.note || '',
          date: entryData.date || new Date().toISOString().split('T')[0],
          goalId: entryData.goalId || '',
          goalName: entryData.goalName || '',
          timestamp: serverTimestamp()
        });

        // Atomically update /users/{uid} field totalSaved using increment(delta)
        const userRef = doc(db, 'users', currentUser.uid);
        await setDoc(userRef, { totalSaved: increment(delta) }, { merge: true });

        // Update goal balance in Firestore
        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-') && !targetGoal.id.startsWith('goal-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          await updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal amount sync:", e));
        }

        return docRef.id;
      }
      return localId;
    }

    async function updateLedgerEntry(id, newAmount, newNote, newDate) {
      const existing = ledger.find(item => item.id === id);
      if (!existing) return;

      const oldAmount = Number(existing.amount) || 0;
      const amountDiff = newAmount - oldAmount;
      const isAdd = existing.type === 'ADD';
      const delta = isAdd ? amountDiff : -amountDiff;
      const targetGoal = goals.find(g => g.id === existing.goalId || g.name === existing.goalName);

      // Optimistic local update
      existing.amount = newAmount;
      existing.note = newNote;
      existing.date = newDate;

      if (targetGoal) {
        targetGoal.currentAmount = Math.max(0, (Number(targetGoal.currentAmount) || 0) + delta);
      }

      saveLocalData({ goals, ledger });
      renderAll();

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        if (!id.startsWith('tx-')) {
          const ref = doc(db, 'users', currentUser.uid, 'ledger', id);
          await updateDoc(ref, { amount: newAmount, note: newNote, date: newDate });
        }

        if (delta !== 0) {
          const userRef = doc(db, 'users', currentUser.uid);
          await setDoc(userRef, { totalSaved: increment(delta) }, { merge: true });
        }

        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-') && !targetGoal.id.startsWith('goal-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          await updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal update:", e));
        }
      }
    }

    async function deleteGoal(goalId) {
      const target = goals.find(g => g.id === goalId);
      if (!target) return;
      if (!confirm(`Delete goal vault "${target.name}"?`)) return;

      goals = goals.filter(g => g.id !== goalId);
      saveLocalData({ goals, ledger });
      renderAll();
      showToast(`Goal vault "${target.name}" deleted.`, 'info');

      if (!isDemoMode && db && currentUser && currentUser.uid !== 'demo-user') {
        if (!goalId.startsWith('goal-') && !goalId.startsWith('custom-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', goalId);
          await deleteDoc(gRef).catch(e => console.warn("Goal delete warning:", e));
        }
      }
    }

    async function deleteLedgerEntry(id) {
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
        if (!id.startsWith('tx-')) {
          const ref = doc(db, 'users', currentUser.uid, 'ledger', id);
          await deleteDoc(ref);
        }

        const userRef = doc(db, 'users', currentUser.uid);
        await setDoc(userRef, { totalSaved: increment(reversalDelta) }, { merge: true });

        if (targetGoal && targetGoal.id && !targetGoal.id.startsWith('custom-') && !targetGoal.id.startsWith('goal-')) {
          const gRef = doc(db, 'users', currentUser.uid, 'goals', targetGoal.id);
          await updateDoc(gRef, { currentAmount: targetGoal.currentAmount }).catch(e => console.warn("Goal update:", e));
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

      const elTotal = document.getElementById('totalStashedDisplay') || document.getElementById('metric-total-capital');
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

            <div class="pt-2.5 border-t border-slate-100 flex items-center gap-2">
              <button class="btn-primary-metallic text-xs min-h-[44px] py-2 px-3 flex-1 btn-quick-goal-stash" data-goal-id="${g.id}" data-goal-name="${g.name}" type="button">
                + Add Funds
              </button>
              <button class="h-[44px] px-3 rounded-xl border border-slate-200 text-slate-400 hover:text-rose-600 hover:border-rose-200 hover:bg-rose-50 transition-all flex items-center justify-center cursor-pointer btn-delete-goal" data-goal-id="${g.id}" title="Delete Goal" aria-label="Delete goal">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
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
      container.querySelectorAll('.btn-delete-goal').forEach(btn => {
        btn.addEventListener('click', () => {
          const gid = btn.dataset.goalId;
          if (gid) deleteGoal(gid);
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

    formCreateGoal?.addEventListener('submit', async (e) => {
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

      try {
        await persistGoal({
          name,
          targetAmount: amt,
          currentAmount: 0,
          deadline,
          cadence: selectedGoalCadence
        });

        modalCreateGoal.classList.remove('open');
        goalInputName.value = '';
        goalInputAmount.value = '';
        goalInputDeadline.value = '';
        showToast(`🎯 Goal Vault "${name}" created!`, 'success');
        switchTab('goals');
      } catch (err) {
        console.error("Create goal error:", err);
        showToast('Error creating goal: ' + err.message, 'error');
      } finally {
        unlockBtn(btnCreateGoalSubmit);
      }
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

    formAddSavings?.addEventListener('submit', async (e) => {
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

      // Anti-Spam Single Click Lock
      lockBtn(btnAddSavingsSubmit, 'Stashing...');

      try {
        const goalMatch = goals.find(g => g.name.toLowerCase() === vaultName.toLowerCase());
        const goalId = goalMatch ? goalMatch.id : 'custom-' + Date.now();

        await persistLedgerEntry({
          goalId,
          goalName: vaultName,
          type: 'ADD',
          amount: amt,
          note,
          date
        });

        modalAddSavings.classList.remove('open');
        clearAddChip();
        addAmountInput.value = '';
        addNoteInput.value = '';
        showToast(`+₹${amt.toLocaleString('en-IN')} added to "${vaultName}"! ⚡`, 'success');
      } catch (err) {
        console.error("Add savings submission error:", err);
        showToast('Error saving deposit: ' + err.message, 'error');
      } finally {
        unlockBtn(btnAddSavingsSubmit);
      }
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

    formWithdrawal?.addEventListener('submit', async (e) => {
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

      // Anti-Spam Single Click Lock
      lockBtn(btnWithdrawalSubmit, 'Recording...');

      try {
        const goalMatch = goals.find(g => g.id === goalId);
        const goalName = goalMatch ? goalMatch.name : 'Vault';

        await persistLedgerEntry({
          goalId,
          goalName,
          type: 'MINUS',
          amount: amt,
          note,
          date
        });

        modalWithdrawal.classList.remove('open');
        withAmountInput.value = '';
        withNoteInput.value = '';
        showToast(`-₹${amt.toLocaleString('en-IN')} withdrawal logged from "${goalName}".`, 'info');
      } catch (err) {
        console.error("Withdrawal submission error:", err);
        showToast('Error recording withdrawal: ' + err.message, 'error');
      } finally {
        unlockBtn(btnWithdrawalSubmit);
      }
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

    formEditLedger?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const id = editEntryId.value;
      const amt = Number(editEntryAmount.value) || 0;
      const note = editEntryNote.value.trim();
      const date = editEntryDate.value;

      if (!id || amt <= 0) return;

      lockBtn(btnEditLedgerSubmit, 'Saving...');

      try {
        await updateLedgerEntry(id, amt, note, date);
        modalEditLedger.classList.remove('open');
        showToast('Entry updated in real-time!', 'success');
      } catch (err) {
        console.error("Edit entry error:", err);
        showToast('Error updating entry: ' + err.message, 'error');
      } finally {
        unlockBtn(btnEditLedgerSubmit);
      }
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

    btnDeleteLedgerConfirm?.addEventListener('click', async () => {
      const id = deleteEntryId.value;
      if (!id) return;

      lockBtn(btnDeleteLedgerConfirm, 'Deleting...');

      try {
        await deleteLedgerEntry(id);
        modalDeleteLedger.classList.remove('open');
        showToast('Entry deleted & balance reversed.', 'info');
      } catch (err) {
        console.error("Delete entry error:", err);
        showToast('Error deleting entry: ' + err.message, 'error');
      } finally {
        unlockBtn(btnDeleteLedgerConfirm);
      }
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
      const authContainer = document.getElementById("authContainer") || authView;
      const dashboardContainer = document.getElementById("dashboardContainer") || dashboardView;

      if (dashboardContainer) dashboardContainer.classList.add('hidden');
      if (authContainer) {
        authContainer.classList.remove('hidden');
        authContainer.style.display = 'flex';
      }

      if (typeof clearAuthError === 'function') clearAuthError();

      const btn = document.getElementById("googleLoginBtn") || document.getElementById("btn-google-auth");
      const label = document.getElementById("btn-auth-label");
      const arrow = document.getElementById("trailing-arrow-icon");
      const spinner = document.getElementById("btn-auth-spinner");

      if (btn) btn.disabled = false;
      if (label) label.textContent = "Continue with Google";
      if (arrow) arrow.classList.remove('hidden');
      if (spinner) spinner.classList.add('hidden');

      showToast('Signed out of session.', 'info');
    }

        // ============================================================
    // COLLAPSIBLE SIDEBAR CONTROLLER WITH SMOOTH SLIDE ANIMATION
    // ============================================================
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebarToggleBtn');
    let isCollapsed = false;

    function applySidebarState(collapsed) {
      isCollapsed = !!collapsed;
      if (!sidebar || !toggleBtn) return;

      sidebar.classList.toggle('w-64', !isCollapsed);
      sidebar.classList.toggle('w-20', isCollapsed);
      document.querySelectorAll('.sidebar-text').forEach(el => {
        el.classList.toggle('hidden', isCollapsed);
      });

      const chevron = toggleBtn.querySelector('svg');
      if (chevron) {
        chevron.classList.toggle('rotate-180', isCollapsed);
      }
      toggleBtn.setAttribute('title', isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar');
      toggleBtn.setAttribute('aria-expanded', String(!isCollapsed));

      try {
        localStorage.setItem('smm_sidebar_collapsed', isCollapsed ? 'true' : 'false');
      } catch (e) {}
    }

    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        applySidebarState(!isCollapsed);
      });

      // Restore persisted collapsed state from localStorage
      try {
        const savedSidebarState = localStorage.getItem('smm_sidebar_collapsed');
        if (savedSidebarState === 'true') {
          applySidebarState(true);
        }
      } catch (e) {}
    }

    const trailingArrowIcon = document.getElementById('trailing-arrow-icon');

    // ── Google Provider Setup with select_account prompt ─────────
    provider.setCustomParameters({ prompt: 'select_account' });

    // Ensure session persistence across refreshes
    setPersistence(auth, browserLocalPersistence).catch(e => console.warn("Persistence init notice:", e));

    // User-facing Visual Error Alert Display
    function showAuthError(msg) {
      let errBox = document.getElementById("authErrorBadge") || document.getElementById("auth-feedback");
      if (!errBox) {
        errBox = document.createElement("div");
        errBox.id = "authErrorBadge";
        errBox.className = "mt-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-600 text-xs font-semibold text-center";
        const card = document.getElementById("auth-card") || document.getElementById("authCard");
        if (card) card.appendChild(errBox);
      }
      errBox.innerHTML = `⚠️ <span>Login Alert: ${msg}</span>`;
      errBox.classList.remove("hidden");
    }

    function clearAuthError() {
      const errBox = document.getElementById("authErrorBadge") || document.getElementById("auth-feedback");
      if (errBox) {
        errBox.classList.add("hidden");
        errBox.innerHTML = '';
      }
    }

    // ── Google One-Click Sign-In Handler ──────────────────────────
    window.handleGoogleLogin = async function() {
      const btn = document.getElementById("googleLoginBtn") || document.getElementById("btn-google-auth");
      const label = document.getElementById("btn-auth-label");
      const spinner = document.getElementById("btn-auth-spinner");
      const arrow = document.getElementById("trailing-arrow-icon");

      clearAuthError();

      if (btn) btn.disabled = true;
      if (label) label.textContent = "Connecting to Vault...";
      if (arrow) arrow.classList.add("hidden");
      if (spinner) spinner.classList.remove("hidden");

      try {
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        console.log("Authentication Successful:", user.displayName, user.uid);
        // onAuthStateChanged will handle immediate UI transition and real-time listeners
      } catch (error) {
        console.error("Auth Failure Error Code:", error.code, error.message);
        let userMsg = error.message || "Could not authenticate with Google.";
        if (error.code === 'auth/popup-blocked') {
          userMsg = "Popup was blocked by your browser. Please allow popups for this site, or use Instant Demo Mode.";
        } else if (error.code === 'auth/popup-closed-by-user') {
          userMsg = "Google sign-in popup was closed before completion.";
        } else if (error.code === 'auth/cancelled-popup-request') {
          userMsg = "Sign-in request was cancelled.";
        } else if (error.code === 'auth/unauthorized-domain') {
          userMsg = "Domain is not authorized in Firebase Console.";
        }
        showAuthError(userMsg);
      } finally {
        if (btn) btn.disabled = false;
        if (label) label.textContent = "Continue with Google";
        if (arrow) arrow.classList.remove("hidden");
        if (spinner) spinner.classList.add("hidden");
      }
    };

    // Attach click listener to Google Auth Button
    const googleBtn = document.getElementById("googleLoginBtn") || document.getElementById("btn-google-auth");
    googleBtn?.addEventListener('click', window.handleGoogleLogin);

    // Instant Demo Mode Handler
    document.getElementById('btn-demo-mode')?.addEventListener('click', () => {
      enterDashboard({
        uid: 'demo-user',
        displayName: 'Kai Sterling',
        email: 'demo@savemoneymanually.com',
        isDemo: true
      });
      showToast('Entered Instant Demo Cockpit. Full preview mode active.', 'info');
    });

    // ── Sign Out Handlers ─────────────────────────────────────────
    btnDashSignout?.addEventListener('click', async () => {
      try { await signOut(auth); } catch (e) {}
      exitToAuth();
    });
    btnDashSignoutMobile?.addEventListener('click', async () => {
      try { await signOut(auth); } catch (e) {}
      exitToAuth();
    });

    // Directly transitions to main dashboard when user is logged in




    // ================================================================
    // FIREBASE AUTH STATE OBSERVER — MASTER ENTRY POINT
    // ================================================================
    // Immediate state transition listener
    onAuthStateChanged(auth, async (user) => {
      const authContainer = document.getElementById("authContainer") || authView;
      const dashboardContainer = document.getElementById("dashboardContainer") || dashboardView;

      if (user) {
        currentUser = user;
        // Hide Login Card, Reveal Dashboard
        if (authContainer) {
          authContainer.classList.add("hidden");
          authContainer.style.display = "none";
        }
        if (dashboardContainer) {
          dashboardContainer.classList.remove("hidden");
        }

        // Upsert user profile record in Firestore
        if (db) {
          try {
            const userDocRef = doc(db, 'users', user.uid);
            await setDoc(userDocRef, {
              uid: user.uid,
              email: user.email || '',
              displayName: user.displayName || user.email?.split('@')[0] || 'Saver',
              photoURL: user.photoURL || null,
              lastLogin: serverTimestamp()
            }, { merge: true });
          } catch (upsertErr) {
            console.warn("Firestore profile sync notice:", upsertErr);
          }
        }

        enterDashboard(user);
        if (typeof window.__sgInit === 'function') window.__sgInit(user);
      } else {
        currentUser = null;
        exitToAuth();
        // Tear down Saving Guide subscriptions
        if (typeof window.__sgInit === 'function') window.__sgInit(null);
        // Tear down data subscriptions
        if (typeof unsubGoals  === 'function') { unsubGoals();  unsubGoals  = null; }
        if (typeof unsubLedger === 'function') { unsubLedger(); unsubLedger = null; }
      }
    });


    // ================================================================
    // FIRESTORE REALTIME SYNC STATUS BADGE
    // ================================================================
    (function initSyncBadge() {
      const badge = document.getElementById('fs-sync-badge');
      const dot   = document.getElementById('fs-sync-dot');
      const label = document.getElementById('fs-sync-label');
      if (!badge) return;

      let hideTimer = null;

      window.__fsSyncStatus = function(state, detail) {
        // state: 'active' | 'error' | 'connecting'
        badge.className = state + ' visible';
        const labels = {
          active:     'Firestore Realtime Active',
          error:      'Firestore Connection Dropped',
          connecting: 'Connecting to Firestore…'
        };
        if (label) label.textContent = detail || labels[state] || state;

        clearTimeout(hideTimer);
        if (state === 'active') {
          // Auto-hide after 4s when active (show briefly on each sync)
          hideTimer = setTimeout(() => badge.classList.remove('visible'), 4000);
        }
      };

      // Show connecting immediately
      window.__fsSyncStatus('connecting');
    })();

    // ================================================================
    // ░░  SAVING GUIDE — HYBRID BOT & LIVE ADMIN DESK ENGINE  ░░
    // ================================================================
    (() => {
      const ADMIN_EMAIL     = 'karanak1513@gmail.com';
      const PRESENCE_PATH   = 'system/admin_presence';
      const TYPING_MIN      = 600;   // ms min typing delay
      const TYPING_MAX      = 1200;  // ms max typing delay

      // ── State ────────────────────────────────────────────────────
      let sgThreadId        = null;
      let sgWindowOpen      = false;
      let sgSendLock        = false;
      let sgBotLock         = false;      // prevents concurrent bot replies
      let sgBotQueue        = [];         // pending user messages while bot is typing
      let sgUnsubMsgs       = null;
      let sgUnsubThread     = null;
      let sgUnsubAdmin      = null;       // admin threads stream
      let sgUnsubAdminMsgs  = null;       // admin selected thread messages
      let sgUnsubPresence   = null;       // admin presence listener
      let sgActiveThread    = null;       // admin: selected threadId
      let sgAdminSendLock   = false;
      let sgChatStatus      = 'BOT_AUTONOMOUS';
      let sgAdminOnline     = false;      // tracks live admin presence
      let sgConvContext     = {           // multi-turn memory
        lastIntent:   null,
        lastAmount:   null,
        lastDuration: null,
        lastGoal:     null,
        turnCount:    0
      };

      // ── DOM ──────────────────────────────────────────────────────
      const elLauncher     = document.getElementById('sg-launcher');
      const elBadge        = document.getElementById('sg-unread-badge');
      const elWindow       = document.getElementById('sg-window');
      const elMessages     = document.getElementById('sg-messages');
      const elTyping       = document.getElementById('sg-typing-indicator');
      const elInput        = document.getElementById('sg-text-input');
      const elSendBtn      = document.getElementById('sg-send-btn');
      const elAgentName    = document.getElementById('sg-agent-name');
      const elStatusDot    = document.getElementById('sg-status-dot');
      const elStatusLabel  = document.getElementById('sg-status-label');
      const elAdminOverlay = document.getElementById('sg-admin-overlay');
      const elAdminClose   = document.getElementById('sg-admin-close');
      const elThreadsList  = document.getElementById('sg-threads-list');
      const elThreadCount  = document.getElementById('sg-thread-count');
      const elAdminSelUser = document.getElementById('sg-admin-sel-user');
      const elAdminMsgs    = document.getElementById('sg-admin-messages');
      const elAdminInput   = document.getElementById('sg-admin-input');
      const elAdminSend    = document.getElementById('sg-admin-send');
      const elTakeover     = document.getElementById('sg-admin-takeover');
      const elHandback     = document.getElementById('sg-admin-handback');
      const elResolve      = document.getElementById('sg-admin-resolve');

      // ── Tick Helpers ─────────────────────────────────────────────
      function tickHTML(status) {
        if (status === 'SEEN')      return '<span class="sg-ticks seen">✓✓</span>';
        if (status === 'DELIVERED') return '<span class="sg-ticks delivered">✓✓</span>';
        return '<span class="sg-ticks sent">✓</span>';
      }

      function updateMessageTick(msgEl, status) {
        const tick = msgEl?.querySelector('.sg-ticks');
        if (!tick) return;
        tick.className = 'sg-ticks ' + status.toLowerCase();
        tick.textContent = (status === 'SENT') ? '✓' : '✓✓';
      }

      // ── Format timestamp ─────────────────────────────────────────
      function fmtTime(ts) {
        if (!ts) return '';
        const d = ts.toDate ? ts.toDate() : new Date(ts);
        return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      }

      // ── Render a message in user chat window ─────────────────────
      function renderMsg(msgId, sender, text, status, ts) {
        const isUser  = sender === 'USER';
        const isAdmin = sender === 'ADMIN';
        const isBot   = sender === 'SAVING_GUIDE';

        const wrap = document.createElement('div');
        wrap.className = 'sg-msg-wrap ' + (isUser ? 'user-wrap' : 'bot-wrap');
        wrap.dataset.msgid = msgId || '';

        // Sender tag (only for bot/admin)
        if (!isUser) {
          const tag = document.createElement('div');
          tag.className = 'sg-sender-tag' + (isAdmin ? ' admin-tag' : '');
          tag.textContent = isAdmin ? '● Official Support' : '🛡 Saving Guide';
          wrap.appendChild(tag);
        }

        const bubble = document.createElement('div');
        bubble.className = 'sg-bubble ' + (isUser ? 'sg-bubble-user' : isAdmin ? 'sg-bubble-admin' : 'sg-bubble-bot');
        bubble.innerHTML = text;
        wrap.appendChild(bubble);

        // Timestamp + ticks row (only for user msgs)
        if (isUser) {
          const meta = document.createElement('div');
          meta.style.cssText = 'display:flex;align-items:center;gap:3px;padding-right:2px;';
          const timeEl = document.createElement('span');
          timeEl.style.cssText = 'font-size:0.58rem;color:#94A3B8;font-family:monospace;';
          timeEl.textContent = fmtTime(ts);
          meta.appendChild(timeEl);
          meta.insertAdjacentHTML('beforeend', tickHTML(status || 'SENT'));
          wrap.appendChild(meta);
        } else {
          const timeEl = document.createElement('div');
          timeEl.style.cssText = 'font-size:0.58rem;color:#CBD5E1;font-family:monospace;padding-left:4px;';
          timeEl.textContent = fmtTime(ts);
          wrap.appendChild(timeEl);
        }

        // Insert before typing indicator
        elMessages?.insertBefore(wrap, elTyping);
        scrollToBottom(elMessages);
        return wrap;
      }

      function scrollToBottom(el) {
        if (el) el.scrollTop = el.scrollHeight;
      }

      // ── Typing indicator ─────────────────────────────────────────
      function showTyping(label) {
        const lbl = elTyping?.querySelector('.sg-typing-label');
        if (lbl) lbl.textContent = label || 'Saving Guide is typing…';
        elTyping?.classList.add('visible');
        scrollToBottom(elMessages);
      }
      function hideTyping() { elTyping?.classList.remove('visible'); }

      // ── Quick Pills ──────────────────────────────────────────────
      const DEFAULT_PILLS = [
        { label: '💰 How to save?',      text: 'How do I log my savings?' },
        { label: '🎯 Set a goal',        text: 'How to set a savings target?' },
        { label: '🔒 Is it secure?',     text: 'Is real money collected?' },
        { label: '📒 View ledger',       text: 'How do I see my history?' },
        { label: '🤝 Speak to human',    text: 'I want to talk to a human agent' },
      ];

      function renderPills(pills) {
        const div = document.createElement('div');
        div.className = 'sg-pills';
        pills.forEach(p => {
          const btn = document.createElement('button');
          btn.className = 'sg-pill';
          btn.type = 'button';
          btn.textContent = p.label;
          btn.addEventListener('click', () => {
            div.remove();
            handleUserSend(p.text);
          });
          div.appendChild(btn);
        });
        elMessages?.insertBefore(div, elTyping);
        scrollToBottom(elMessages);
      }

      // ── Update header state ──────────────────────────────────────
      function setHeaderState(state) {
        // state: 'bot' | 'requesting' | 'live' | 'resolved'
        const states = {
          bot:        { name: 'Saving Guide',          dot: '',      label: 'Online · Auto-reply active',       dotClass: '' },
          requesting: { name: 'Connecting to Agent…',  dot: 'busy',  label: 'Agent will join shortly',           dotClass: 'busy' },
          live:       { name: 'Live Support Agent',    dot: 'live',  label: 'Connected to live operator',        dotClass: 'live' },
          resolved:   { name: 'Saving Guide',          dot: '',      label: 'Conversation resolved ✓',           dotClass: '' },
        };
        const s = states[state] || states.bot;
        if (elAgentName)   elAgentName.textContent = s.name;
        if (elStatusLabel) elStatusLabel.textContent = s.label;
        if (elStatusDot)   elStatusDot.className = 'sg-status-dot' + (s.dotClass ? ' ' + s.dotClass : '');
      }

      // ================================================================
      // ░░  SAVING GUIDE — CONTINUOUS AUTONOMOUS BRAIN ENGINE  ░░
      // ================================================================

      // ── Admin Presence Tracking ──────────────────────────────────
      function heartbeatAdminPresence(isOnline) {
        if (!db || !currentUser || currentUser.email !== ADMIN_EMAIL) return;
        setDoc(doc(db, 'system/admin_presence'), {
          isOnline, lastSeen: serverTimestamp(), email: ADMIN_EMAIL
        }, { merge: true }).catch(() => {});
      }

      function watchAdminPresence() {
        if (!db) return;
        if (sgUnsubPresence) sgUnsubPresence();
        sgUnsubPresence = onSnapshot(doc(db, 'system', 'admin_presence'), (snap) => {
          sgAdminOnline = snap.exists() ? (snap.data().isOnline === true) : false;
        }, () => { sgAdminOnline = false; });
      }

      // ── Number / Duration Extractor ──────────────────────────────
      function extractNumbers(text) {
        const nums = [];
        const lower = text.toLowerCase();
        const lakhM = lower.match(/(\d+\.?\d*)\s*lakh/);
        if (lakhM) nums.push(Math.round(parseFloat(lakhM[1]) * 100000));
        const kM = lower.match(/(\d+\.?\d*)\s*k\b/);
        if (kM) nums.push(Math.round(parseFloat(kM[1]) * 1000));
        const plain = [...lower.matchAll(/(\d{1,3}(?:,\d{3})*|\d{2,})/g)];
        plain.forEach(m => {
          const n = parseInt(m[1].replace(/,/g, ''));
          if (n > 0 && !nums.includes(n)) nums.push(n);
        });
        return nums;
      }

      function extractDuration(text) {
        const l = text.toLowerCase();
        let m;
        m = l.match(/(\d+)\s*(din|day|days)/);
        if (m) return { days: +m[1], label: m[1] + ' din' };
        m = l.match(/(\d+)\s*(week|hafte)/);
        if (m) return { days: +m[1] * 7, label: m[1] + ' hafte' };
        m = l.match(/(\d+)\s*(month|mahine|mahina|mah)/);
        if (m) return { days: +m[1] * 30, label: m[1] + ' mahine' };
        m = l.match(/(\d+)\s*(year|sal|saal)/);
        if (m) return { days: +m[1] * 365, label: m[1] + ' saal' };
        return null;
      }

      // ── NLP Intent Classifier ────────────────────────────────────
      const INTENTS = [
        { name:'SAVINGS_MATH',   keys:['bachana','bacha','bachat','jama','calculate','plan','kitna save','how much save','lakh','₹'] },
        { name:'HOW_TO_LOG',     keys:['log kaise','add kaise','add karun','deposit','how to save','save kaise','paisa add','entry kaise','kaise add','record kaise'] },
        { name:'GOAL_CREATE',    keys:['goal banana','target banana','vault create','naya goal','new goal','goal kaise','target set','goal set','create goal','goal banao','vault banana'] },
        { name:'WITHDRAWAL',     keys:['withdraw','nikalna','nikalo','paisa nikalna','wapas lena','remove','minus karo'] },
        { name:'SECURITY',       keys:['real money','real paisa','bank connect','account link','secure','safe','data safe','kya data','privacy','encrypted'] },
        { name:'LEDGER',         keys:['ledger','history','record dekho','purana','transactions','pichle','all entries','dekho entries'] },
        { name:'CALENDAR',       keys:['calendar','streak','discipline','consistency','aaj ka','kitne din','how many days','din baad'] },
        { name:'PROGRESS',       keys:['progress','kitna bacha','how much saved','total','balance','kitna hai','current','abhi tak','total amount'] },
        { name:'MOTIVATION',     keys:['motivation','mushkil','difficult','hard','nahi ho raha','fail','chod dun','quit','boring','kya fayda','why save','importance','zaruri'] },
        { name:'GREETING',       keys:['hello','hi','hey','hii','helo','namaste','namaskar','kya haal','sup','good morning','good evening','shubh'] },
        { name:'THANKS',         keys:['thank','thanks','shukriya','dhanyawad','bahut acha','bohot acha','amazing','perfect','helpful','great','superb','brilliant','wah'] },
        { name:'HUMAN_AGENT',    keys:['human','agent chahiye','karan ko','operator','live support','speak karna','baat karo','talk to human','real person','insaan se'] },
        { name:'BUG_REPORT',     keys:['bug','error','crash','not working','problem','issue','kaam nahi','broken','glitch','fix karo'] },
        { name:'AFFIRM',         keys:['haan','ha ','yes','ok ','okay','sure','bilkul','zaroor','theek hai','sahi hai','correct','right','done'] },
        { name:'NEGATE',         keys:['nahi','no ','nope','mat ','band karo','stop','skip','baad mein','later','abhi nahi'] },
      ];

      function classifyIntent(text) {
        const lower = text.toLowerCase().trim();
        const nums  = extractNumbers(text);
        const dur   = extractDuration(text);
        // Math intent: amount + duration together
        if (nums.length > 0 && (dur || /din|day|month|mahine|week|hafte|year|saal/.test(lower))) {
          return { name: 'SAVINGS_MATH', nums, dur };
        }
        // Math intent: continuing context
        if (nums.length > 0 && sgConvContext.lastIntent === 'SAVINGS_MATH') {
          return { name: 'SAVINGS_MATH', nums, dur: dur || sgConvContext.lastDuration };
        }
        for (const intent of INTENTS) {
          if (intent.keys.some(k => lower.includes(k))) return { name: intent.name, nums, dur };
        }
        return { name: 'UNKNOWN', nums, dur };
      }

      // ── Reply Generator ──────────────────────────────────────────
      function generateReply(intent, userText) {
        const ctx = sgConvContext;
        ctx.turnCount++;
        const { name, nums, dur } = intent;
        const inr = n => '\u20b9' + Number(n).toLocaleString('en-IN');

        if (name === 'SAVINGS_MATH') {
          const amount   = nums[0] || ctx.lastAmount;
          const duration = dur || ctx.lastDuration || { days: 30, label: '1 mahine' };
          if (amount) {
            ctx.lastAmount = amount; ctx.lastDuration = duration; ctx.lastIntent = 'SAVINGS_MATH';
            const perDay = Math.ceil(amount / duration.days);
            return `<strong>\u2728 Aapka Savings Plan:</strong><br><br>\u2022 <strong>Target:</strong> ${inr(amount)}<br>\u2022 <strong>Samay:</strong> ${duration.label}<br>\u2022 <strong>Rozana chahiye:</strong> <span style="color:#2563EB;font-weight:800;">${inr(perDay)}/din</span><br>\u2022 <strong>Hafte mein:</strong> ${inr(perDay*7)}/week<br>\u2022 <strong>Mahine mein:</strong> ${inr(perDay*30)}/month<br><br>Kya aap iske liye <strong>Goal set karna chahenge?</strong> Main step-by-step guide karunga. \ud83c\udfaf`;
          }
          ctx.lastIntent = 'SAVINGS_MATH';
          if (dur) { ctx.lastDuration = dur; return `\ud83d\udcb0 ${dur.label} mein kitna save karna hai? <strong>Amount bataiye</strong> (jaise "50000" ya "1 lakh") — main daily quota calculate kar dunga. \ud83e\uddee`; }
          return `\ud83d\udcb0 <strong>Savings plan banate hain!</strong> Kitna amount bachana hai aur kitne din/mahine mein? Jaise: <em>"50,000 in 3 mahine"</em>`;
        }

        if (name === 'AFFIRM' && ctx.lastIntent === 'SAVINGS_MATH') {
          ctx.lastIntent = 'GOAL_CREATE';
          return `\ud83c\udfaf <strong>Chalo goal set karte hain:</strong><br><br>1. <strong>Goals tab</strong> (bottom navigation)<br>2. <strong>"+ Create Target Vault"</strong> tap karo<br>3. Amount: <strong>${ctx.lastAmount ? inr(ctx.lastAmount) : 'apna amount'}</strong><br>4. Deadline set karo<br><br>App apne aap daily quota calculate kar dega! \u2705<br><br><em>Kya koi specific goal naam hai? Jaise "Emergency Fund", "Phone", "Trip"?</em>`;
        }

        if (name === 'NEGATE' && ctx.lastIntent === 'SAVINGS_MATH') {
          return `No problem! \ud83d\ude0a Jab bhi savings plan banana ho — main yahan hoon.<br><br>Aur kuch puchna hai? Deposits, goals, ledger, ya kuch bhi?`;
        }

        if (name === 'GREETING') {
          ctx.lastIntent = 'GREETING';
          const gs = [
            `\ud83d\udc4b <strong>Namaste!</strong> Main Saving Guide hoon \ud83d\udee1\ufe0f — aapka personal savings discipline assistant.<br><br>Aaj main aapki kya madad kar sakta hoon?<br>\u2022 \ud83d\udcb0 Savings plan calculate karna<br>\u2022 \ud83c\udfaf New goal set karna<br>\u2022 \ud83d\udcd2 Records check karna<br>\u2022 \ud83d\udd12 Security questions<br><br><em>Bas type karein!</em>`,
            `\ud83d� <strong>Namaste ji!</strong> Saving Guide hazir hai. Aapka savings safar kaisa chal raha hai?<br><br>Kya aaj kuch save kiya? Ya koi naya goal set karna hai?`
          ];
          return gs[Math.floor(Math.random() * gs.length)];
        }

        if (name === 'THANKS') { ctx.lastIntent = 'THANKS'; return `\ud83d\ude0a <strong>Bahut khushi hui!</strong> Aapka savings safar inspiring hai.<br><br>Kuch aur help chahiye? Main hamesha yahan hoon. \ud83d\udcaa<br><br><em>Aaj kitna save karne ka plan hai?</em>`; }
        if (name === 'HOW_TO_LOG') { ctx.lastIntent = 'HOW_TO_LOG'; return `\ud83d\udcb0 <strong>Savings log karna easy hai:</strong><br><br>1. Dashboard pe <strong>"+ Add Saved"</strong> button tap karo<br>2. Amount enter karo (cash ya UPI)<br>3. Goal select karo (optional)<br>4. Confirm — vault instantly update! \u26a1<br><br><em>Koi bank link nahi hota. Aap sirf track karte ho.</em><br><br>Abhi kitna save karna chahte hain?`; }
        if (name === 'GOAL_CREATE') { ctx.lastIntent = 'GOAL_CREATE'; return `\ud83c\udfaf <strong>Goal create karna:</strong><br><br>1. <strong>Goals tab</strong> (bottom nav)<br>2. <strong>"+ Create Target Vault"</strong><br>3. Naam, amount, deadline set karo<br>4. Cadence: Daily/Monthly/Yearly<br><br>App auto-calculate karta hai: <em>\u20b910,000 in 30 din = \u20b9334/din</em> \ud83d\udcca<br><br>Kaunsa goal banana hai? Amount bataiye — main plan bana deta hoon!`; }
        if (name === 'WITHDRAWAL') { ctx.lastIntent = 'WITHDRAWAL'; return `\ud83c\udfe6 <strong>Withdrawal record karna:</strong><br><br>1. Home pe <strong>"\u2212 Record Withdrawal"</strong><br>2. Vault choose karo<br>3. Amount enter karo<br>4. Reason (optional)<br><br>Balance instantly update. \u2705<br><br>Kitna withdraw karna chahte hain?`; }
        if (name === 'SECURITY') { ctx.lastIntent = 'SECURITY'; return `\ud83d\udd12 <strong>100% Safe — Koi real paisa collect nahi hota.</strong><br><br>\u274c Koi bank link nahi hota<br>\u274c Koi payment gateway nahi<br>\u2705 Aap khud apni savings alag rakhte ho<br>\u2705 Yahan sirf track karte ho<br>\u2705 Firebase 256-bit encrypted \ud83d�\ufe0f<br><br>Aur koi security sawaal?`; }
        if (name === 'LEDGER') { ctx.lastIntent = 'LEDGER'; return `\ud83d\udcd2 <strong>Ledger / History:</strong><br><br>Bottom nav mein <strong>Ledger tab</strong> tapein.<br><br>Wahan aap deposits, withdrawals chronologically dekhenge, edit/delete kar sakte hain. Real-time sync. \u26a1<br><br>Koi specific entry dhundh rahe hain?`; }
        if (name === 'CALENDAR') { ctx.lastIntent = 'CALENDAR'; return `\ud83d\udcc5 <strong>Calendar Streak:</strong><br><br>Bottom nav mein <strong>Calendar tab</strong>.<br><br>Saving log ki din — Electric Blue se highlight. Research: <strong>66 din ki streak</strong> = permanent habit. \ud83d\udd25<br><br>Aaj ki saving log ki? Abhi kitne din ka streak hai?`; }
        if (name === 'PROGRESS') { ctx.lastIntent = 'PROGRESS'; return `\ud83d\udcca <strong>Progress live dashboard pe hai!</strong><br><br>Home screen pe:<br>\u2022 <strong>Total Capital</strong> — ab tak ki savings<br>\u2022 <strong>This Month</strong> — is mahine<br>\u2022 <strong>Active Goals</strong> — har vault ka %<br><br>Real-time Firestore sync. \u26a1<br><br>Kya kisi specific goal ka progress chahiye?`; }
        if (name === 'MOTIVATION') {
          ctx.lastIntent = 'MOTIVATION';
          const ms = [
            `\ud83d\udcaa <strong>Mushkil lagta hai — bilkul normal!</strong><br><br>Try this: <em>"Pay yourself first"</em> — income aate hi 10% side rakh do, baaki kharch karo.<br><br>Aap daily realistically kitna afford kar sakte hain? Main achievable plan banata hoon. \ud83c\udfaf`,
            `\ud83c\udf1f <strong>Har badi savings choti starting se hoti hai.</strong><br><br>Sirf \u20b9100/din = \u20b936,500/saal. Bina kuch extra kiye.<br><br>Aap abhi kahan hain — naya shuru ya pehle se chal raha hai?`
          ];
          return ms[Math.floor(Math.random() * ms.length)];
        }
        if (name === 'HUMAN_AGENT') { ctx.lastIntent = 'HUMAN_AGENT'; return `\ud83d� <strong>Samajh gaya!</strong> Maine Karan ko notify kar diya.<br><br>Wo jald join karenge. Tab tak — aapka original sawaal kya tha? Main koshish karunga help karne ki. \ud83d�`; }
        if (name === 'BUG_REPORT') { ctx.lastIntent = 'BUG_REPORT'; return `\ud83d� <strong>Issue report kiya — shukriya!</strong><br><br>1. Page <strong>refresh</strong> karein (Ctrl+R)<br>2. Cache clear karein<br>3. Doosre browser mein try karein<br><br>Phir bhi nahi chala? <strong>Kya exactly ho raha hai?</strong> Main Karan tak pahuncha dunga. \ud83d�`; }
        if (name === 'AFFIRM') { return `\ud83d\udc4d <strong>Bilkul!</strong> ${ctx.lastIntent === 'HOW_TO_LOG' ? 'Dashboard pe jaiye — "+Add Saved" tapein. Kitna amount?' : ctx.lastIntent === 'GOAL_CREATE' ? 'Goals tab mein "+Create Target Vault" tapein. Kaunsa goal banana hai?' : 'Toh batao — aur kuch help chahiye?'}`; }
        if (name === 'NEGATE') { return `No problem! \ud83d\ude0a Kab bhi zarurat ho — main yahan hoon. Aur kuch sawaal hai?`; }

        // UNKNOWN — smart fallback (never a dead-end)
        ctx.lastIntent = 'UNKNOWN';
        const fallbacks = [
          `\ud83e\udd14 <strong>Interesting!</strong> Thoda aur detail mein bataiye?<br><br>Ya in mein se batao kya chahiye:`,
          `\ud83d\udcad Main samajhna chahta hoon. <strong>Seedha bata dein:</strong> savings add karni hai, goal banana hai, ya koi aur sawaal?`,
          `\ud83d�\ufe0f Yeh mujhse thoda bahar hai — lekin yeh cheezein main <strong>zaroor guide kar sakta hoon:</strong>`
        ];
        return fallbacks[Math.floor(Math.random() * fallbacks.length)];
      }

      // ── Typing delay (realism) ────────────────────────────────────
      function typingDelay(plainText) {
        const base  = 600;
        const extra = Math.min(plainText.length * 3, 600);
        return base + extra * Math.random();
      }

      // ── Core bot respond (continuous loop) ──────────────────────
      async function botRespond(userText) {
        if (sgChatStatus === 'ADMIN_LIVE') return;
        if (sgBotLock) { sgBotQueue.push(userText); return; }
        sgBotLock = true;

        // Instantly upgrade user's last message to SEEN (tick turns blue)
        if (db && sgThreadId) {
          try {
            const lastQ = query(
              collection(db, 'support_threads', sgThreadId, 'messages'),
              orderBy('timestamp', 'desc'), limit(1)
            );
            const snp = await getDocs(lastQ);
            snp.forEach(d => { if (d.data().sender === 'USER') updateDoc(d.ref, { status: 'SEEN' }).catch(() => {}); });
          } catch (e) {}
        }

        showTyping('Saving Guide is typing\u2026');
        const intent    = classifyIntent(userText);
        const replyText = generateReply(intent, userText);
        const delay     = typingDelay(replyText.replace(/<[^>]*>/g, ''));

        await new Promise(res => setTimeout(res, delay));
        hideTyping();

        if (db && sgThreadId) {
          try {
            await addDoc(collection(db, 'support_threads', sgThreadId, 'messages'),
              { sender: 'SAVING_GUIDE', text: replyText, status: 'DELIVERED', timestamp: serverTimestamp() });
            await updateDoc(doc(db, 'support_threads', sgThreadId), {
              lastMessage: replyText.replace(/<[^>]*>/g, '').substring(0, 80),
              lastMessageTime: serverTimestamp()
            });
          } catch (e) { console.warn('Bot write error:', e); }
        }

        if (intent.name === 'HUMAN_AGENT') {
          if (db && sgThreadId) updateDoc(doc(db, 'support_threads', sgThreadId), { chatStatus: 'ADMIN_LIVE' }).catch(() => {});
          sgChatStatus = 'ADMIN_LIVE';
          setHeaderState('requesting');
        } else if (intent.name === 'UNKNOWN') {
          setTimeout(() => { if (sgChatStatus === 'BOT_AUTONOMOUS') renderPills(DEFAULT_PILLS); }, 350);
        }

        sgBotLock = false;
        // Drain queue — multi-turn continuous
        if (sgBotQueue.length > 0 && sgChatStatus === 'BOT_AUTONOMOUS') {
          const next = sgBotQueue.shift();
          botRespond(next);
        }
      }


      // ── Firestore: ensure thread ───────────────────────────────────
        {
          keys: ['log', 'add', 'deposit', 'how to save', 'save kaise', 'paisa add'],
          reply: '💰 <strong>Saving karna bohot simple hai!</strong><br><br>Dashboard pe <strong>\"+ Add Saved\"</strong> button tapein → amount enter karein (cash ya UPI) → confirm karein. Aapka vault instantly update ho jayega. ⚡<br><br>Koi bank link nahi hota — sirf aap track karte ho!'
        },
        {
          keys: ['goal', 'target', 'vault create', 'savings goal', 'lakshy'],
          reply: '🎯 <strong>Goal/Target banana:</strong><br><br>1. <strong>Goals</strong> tab open karo (bottom navigation)<br>2. <strong>\"+ Create Target Vault\"</strong> tap karo<br>3. Deadline set karo aur cadence choose karo (Daily / Monthly / Yearly)<br><br>App automatically calculate karega ki aapko rozana kitna bachana hai. 📊'
        },
        {
          keys: ['withdraw', 'nikalna', 'remove', 'paise nikalo'],
          reply: '🏦 <strong>Withdrawal record karna:</strong><br><br>Home screen pe <strong>\"− Record Withdrawal\"</strong> tapein → vault choose karein → amount enter karein → reason optional mein likho.<br><br>Balance instantly update ho jayega. ✅'
        },
        {
          keys: ['secure', 'safe', 'real money', 'bank connect', 'collect', 'real paisa'],
          reply: '🔒 <strong>100% Safe — Koi real paisa collect nahi hota.</strong><br><br>SaveMoneyManually kisi bhi bank account se connect nahi karta. Ye ek <em>discipline tracker</em> hai — aap apni savings khud apne paas rakhte ho, sirf yahan track karte ho. Firebase 256-bit encrypted hai. 🛡'
        },
        {
          keys: ['ledger', 'history', 'record', 'transactions', 'purana'],
          reply: '📒 <strong>Ledger / History dekhna:</strong><br><br>Bottom navigation mein <strong>Ledger</strong> tab tapein. Wahan aapke saare deposits, withdrawals, aur changes chronologically dikh jaenge. Koi bhi entry edit ya delete kar sakte ho instantly.'
        },
        {
          keys: ['calendar', 'streak', 'discipline', 'consistency'],
          reply: '📅 <strong>Calendar / Streak:</strong><br><br>Bottom navigation mein <strong>Calendar</strong> tab tapein. Jis din aapne saving log ki, woh Electric Cobalt Blue mein highlight hoga. Streak build karo — consistency sabse badi wealth building habit hai!'
        },
        {
          keys: ['hello', 'hi', 'hey', 'hii', 'namaste', 'start', 'help me', 'kya kar sakte'],
          reply: '👋 <strong>Namaste! Main Saving Guide hoon.</strong><br><br>SaveMoneyManually ka aapka personal savings assistant. Main aapki madad kar sakta hoon:<br>• Savings log karna<br>• Goals set karna<br>• Ledger dekhna<br>• Security questions<br><br>Kya chahiye aapko?'
        },
        {
          keys: ['human', 'agent', 'karan', 'operator', 'live support', 'manav', 'speak', 'baat', 'agent chahiye', 'talk to human'],
          reply: '🔗 <strong>Maine Karan ko notification bhej di hai.</strong><br><br>Wo jald hi join karenge. Tab tak aapka kya sawal hai? Main koshish karunga help karne ki. 🙏',
          action: 'REQUEST_AGENT'
        },
        {
          keys: ['bug', 'error', 'crash', 'not working', 'problem', 'issue', 'kaam nahi', 'broken'],
          reply: '🛠 Isko sunte hue dukh hua! Pehle page refresh karke try karein.<br><br>Agar problem continue kare, to main aapko live agent se connect kar deta hoon. 👇',
          action: 'SUGGEST_AGENT'
        }
      ];

      function botMatch(text) {
        const lower = text.toLowerCase();
        for (const rule of BOT_KB) {
          if (rule.keys.some(k => lower.includes(k))) return rule;
        }
        return null;
      }

      async function botRespond(userText) {
        if (sgBotLock) return;
        sgBotLock = true;

        // 5-second wait: if admin replies in time, skip bot
        await new Promise(res => { sgBotTimer = setTimeout(res, BOT_TIMEOUT); });
        sgBotTimer = null;

        // Re-check status after waiting
        const stillBot = sgChatStatus === 'BOT_AUTONOMOUS';
        if (!stillBot) { sgBotLock = false; return; }

        const rule = botMatch(userText);
        showTyping();

        await new Promise(res => setTimeout(res, 900 + Math.random() * 500));
        hideTyping();

        const replyText = rule ? rule.reply
          : '🤔 Hmm, main exactly samajh nahi paya. Neeche se ek option choose karein ya aur detail mein batayein:';

        // Save bot msg to Firestore
        if (db && sgThreadId) {
          try {
            const msgRef = await addDoc(
              collection(db, 'support_threads', sgThreadId, 'messages'),
              { sender: 'SAVING_GUIDE', text: replyText, status: 'DELIVERED', timestamp: serverTimestamp() }
            );
            await updateDoc(doc(db, 'support_threads', sgThreadId), {
              lastMessage: replyText.replace(/<[^>]*>/g,'').substring(0,80),
              lastMessageTime: serverTimestamp()
            });
          } catch (e) { console.warn('Bot Firestore write error:', e); }
        }

        if (rule?.action === 'REQUEST_AGENT') {
          if (db && sgThreadId) {
            await updateDoc(doc(db, 'support_threads', sgThreadId), { chatStatus: 'ADMIN_LIVE' })
              .catch(() => {});
          }
          sgChatStatus = 'ADMIN_LIVE';
          setHeaderState('requesting');
        } else if (rule?.action === 'SUGGEST_AGENT') {
          setTimeout(() => renderPills([{ label: '🤝 Connect to Live Agent', text: 'I want to talk to a human agent' }]), 200);
        } else if (!rule) {
          setTimeout(() => renderPills(DEFAULT_PILLS), 200);
        }

        sgBotLock = false;
      }

      // ── Firestore: ensure thread ─────────────────────────────────
      async function ensureThread(user) {
        if (!db || !user) return;
        sgThreadId = user.uid;

        const tRef = doc(db, 'support_threads', sgThreadId);
        // Use merge:true setDoc — creates if not exists, preserves chatStatus if exists
        await setDoc(tRef, {
            userId:          user.uid,
            userName:        user.displayName || user.email?.split('@')[0] || 'User',
            userEmail:       user.email || '',
            userPhoto:       user.photoURL || '',
            lastMessage:     '',
            lastMessageTime: serverTimestamp(),
            userUnread:      0,
            adminUnread:     0
          }, { merge: true });

        // Watch thread status
        if (sgUnsubThread) sgUnsubThread();
        sgUnsubThread = onSnapshot(tRef, (s) => {
          if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('active', 'Firestore Realtime Active');
          if (!s.exists()) return;
          const d = s.data();
          sgChatStatus = d.chatStatus || 'BOT_AUTONOMOUS';
          if (sgChatStatus === 'ADMIN_LIVE') setHeaderState('live');
          else if (sgChatStatus === 'BOT_AUTONOMOUS') setHeaderState('bot');

          // Clear user unread badge when window is open
          if (sgWindowOpen && d.userUnread > 0) {
            updateDoc(tRef, { userUnread: 0 }).catch(() => {});
            elBadge?.classList.add('hidden');
          } else if (!sgWindowOpen && d.userUnread > 0) {
            elBadge && (elBadge.textContent = d.userUnread);
            elBadge?.classList.remove('hidden');
          }
        });

        // Watch messages with resilient sorting & index fallback
        if (sgUnsubMsgs) sgUnsubMsgs();
        const msgCol = collection(db, 'support_threads', sgThreadId, 'messages');
        const qry = query(msgCol, orderBy('timestamp', 'asc'));

        const handleMsgsSnapshot = (snap) => {
          if (!elMessages) return;
          elMessages.querySelectorAll('.sg-msg-wrap, .sg-pills, .sg-date-sep').forEach(n => n.remove());

          if (snap.empty) {
            renderWelcome();
            return;
          }
          const msgs = [];
          snap.forEach(ds => {
            msgs.push({ id: ds.id, ref: ds.ref, ...ds.data() });
          });
          // Resilient client-side ascending sort
          msgs.sort((a, b) => {
            const ta = a.timestamp?.toDate ? a.timestamp.toDate() : new Date(a.timestamp || 0);
            const tb = b.timestamp?.toDate ? b.timestamp.toDate() : new Date(b.timestamp || 0);
            return ta - tb;
          });
          msgs.forEach(d => {
            renderMsg(d.id, d.sender, d.text, d.status, d.timestamp);
          });

          // Auto-mark DELIVERED msgs as SEEN if window is open
          if (sgWindowOpen) {
            msgs.forEach(d => {
              if (d.sender !== 'USER' && d.status !== 'SEEN') {
                updateDoc(d.ref, { status: 'SEEN' }).catch(() => {});
              }
            });
          }

          // Also update user msg ticks if admin has seen them
          if (sgChatStatus === 'ADMIN_LIVE') {
            msgs.forEach(d => {
              if (d.sender === 'USER' && d.status === 'DELIVERED') {
                updateDoc(d.ref, { status: 'SEEN' }).catch(() => {});
              }
            });
          }
        };

        sgUnsubMsgs = onSnapshot(qry, handleMsgsSnapshot, (err) => {
          console.warn('sg-msgs ordered snapshot error, using base collection fallback:', err);
          sgUnsubMsgs = onSnapshot(msgCol, handleMsgsSnapshot, (err2) => {
            console.error('sg-msgs fallback snapshot error:', err2);
          });
        });
      }

      function renderWelcome() {
        renderMsg(null, 'SAVING_GUIDE',
          '👋 <strong>Namaste! Main Saving Guide hoon.</strong><br>SaveMoneyManually ka aapka personal savings discipline assistant. Kya madad chahiye?',
          'DELIVERED', null);
        renderPills(DEFAULT_PILLS);
      }

      // ── Handle user send ─────────────────────────────────────────
      async function handleUserSend(overrideText) {
        if (sgSendLock) return;
        const text = (overrideText || elInput?.value || '').trim();
        if (!text || !currentUser) return;
        sgSendLock = true;
        if (elInput && !overrideText) elInput.value = '';

        // Render optimistic bubble immediately (SENT = ✓ gray)
        const optimisticWrap = renderMsg(null, 'USER', text, 'SENT', new Date());

        // Enable send button immediately after optimistic render
        sgSendLock = false;

        // Write to Firestore: SENT → DELIVERED in rapid succession
        if (db && sgThreadId) {
          try {
            const ref = await addDoc(
              collection(db, 'support_threads', sgThreadId, 'messages'),
              { sender: 'USER', text, status: 'SENT', timestamp: serverTimestamp() }
            );

            // Immediately upgrade to DELIVERED (✓✓ gray)
            await updateDoc(ref, { status: 'DELIVERED' });
            updateMessageTick(optimisticWrap, 'DELIVERED');

            await updateDoc(doc(db, 'support_threads', sgThreadId), {
              lastMessage: text.substring(0, 80),
              lastMessageTime: serverTimestamp(),
              adminUnread: increment(1)
            });
          } catch (e) {
            console.warn('User msg write error:', e);
          }
        }

        // Bot responds immediately — no timer delay needed
        // Admin presence check: if admin online and ADMIN_LIVE, skip bot
        if (sgChatStatus === 'BOT_AUTONOMOUS' && !sgAdminOnline) {
          botRespond(text);
        } else if (sgChatStatus === 'BOT_AUTONOMOUS' && sgAdminOnline) {
          // Admin is online but hasn't taken over — bot still responds after short pause
          setTimeout(() => {
            if (sgChatStatus === 'BOT_AUTONOMOUS') botRespond(text);
          }, 2000);
        }
        // If ADMIN_LIVE: admin replies via desk — bot stays silent
      }

      // ── Open / Close window ──────────────────────────────────────
      function openWindow() {
        sgWindowOpen = true;
        elWindow?.classList.add('open');
        elInput?.removeAttribute('disabled');
        elSendBtn?.removeAttribute('disabled');
        setTimeout(() => elInput?.focus(), 200);
        // Mark messages seen
        if (db && sgThreadId) {
          updateDoc(doc(db, 'support_threads', sgThreadId), { userUnread: 0 }).catch(() => {});
        }
        elBadge?.classList.add('hidden');
      }
      function closeWindow() {
        sgWindowOpen = false;
        elWindow?.classList.remove('open');
      }

      // ── Launcher click ───────────────────────────────────────────
      elLauncher?.addEventListener('click', () => {
        if (sgWindowOpen) { closeWindow(); return; }
        if (!currentUser) {
          showToast('Please sign in first to use Saving Guide.', 'info');
          return;
        }
        openWindow();
        if (!sgThreadId) ensureThread(currentUser);
        else if (!elMessages?.querySelector('.sg-msg-wrap')) renderWelcome();
      });

      document.getElementById('sg-close-btn')?.addEventListener('click', closeWindow);
      document.getElementById('sg-minimize-btn')?.addEventListener('click', closeWindow);

      // ── Input handlers ───────────────────────────────────────────
      elInput?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleUserSend(); }
      });
      elInput?.addEventListener('input', () => {
        if (elSendBtn) elSendBtn.disabled = !elInput.value.trim();
      });
      elSendBtn?.addEventListener('click', handleUserSend);

      // ── ░░ ADMIN DESK ░░ ─────────────────────────────────────────
      function isAdmin(user) { return user?.email === ADMIN_EMAIL; }

      function initAdminDesk(user) {
        if (!isAdmin(user) || !db) return;

        // Add admin button to sidebar
        const signoutBtn = document.getElementById('btn-dash-signout');
        if (signoutBtn && !document.getElementById('btn-sg-admin')) {
          const ab = document.createElement('button');
          ab.id   = 'btn-sg-admin';
          ab.type = 'button';
          ab.title = 'Saving Guide Admin Desk';
          ab.className = 'w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl text-xs font-bold text-cobalt hover:bg-blue-50 border border-blue-200 transition-colors cursor-pointer mt-2';
          ab.innerHTML = '<svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4"/></svg><span class="sidebar-text">Admin Desk</span>';
          ab.addEventListener('click', () => {
            elAdminOverlay?.classList.add('open');
            heartbeatAdminPresence(true);
            // Keep presence alive every 30s
            if (window._adminHeartbeatInterval) clearInterval(window._adminHeartbeatInterval);
            window._adminHeartbeatInterval = setInterval(() => {
              if (elAdminOverlay?.classList.contains('open')) heartbeatAdminPresence(true);
              else { clearInterval(window._adminHeartbeatInterval); heartbeatAdminPresence(false); }
            }, 30000);
          });
          signoutBtn.parentNode?.insertBefore(ab, signoutBtn);
        }

        // Stream all threads
        if (sgUnsubAdmin) sgUnsubAdmin();
        const tQuery = query(
          collection(db, 'support_threads'),
          orderBy('lastMessageTime', 'desc')
        );
        sgUnsubAdmin = onSnapshot(tQuery, snap => {
          renderThreadList(snap.docs);
        }, err => console.error('Admin threads error', err));
      }

      function renderThreadList(docs) {
        if (!elThreadsList) return;
        const empty = document.getElementById('sg-threads-empty');

        if (docs.length === 0) {
          if (empty) empty.style.display = 'flex';
          // Remove all rows
          elThreadsList.querySelectorAll('.sg-thread-row').forEach(n => n.remove());
          if (elThreadCount) elThreadCount.textContent = '0 threads';
          return;
        }
        if (empty) empty.style.display = 'none';
        if (elThreadCount) elThreadCount.textContent = `${docs.length} thread${docs.length !== 1 ? 's' : ''}`;

        // Rebuild
        elThreadsList.querySelectorAll('.sg-thread-row').forEach(n => n.remove());

        docs.forEach(ds => {
          const d = ds.data();
          const tid = ds.id;

          const row = document.createElement('div');
          row.className = 'sg-thread-row' + (sgActiveThread === tid ? ' active-thread' : '');
          row.dataset.tid = tid;

          const chipMap = {
            BOT_AUTONOMOUS: 'sg-chip-bot',
            ADMIN_LIVE:     'sg-chip-live',
            RESOLVED:       'sg-chip-resolved'
          };
          const chipClass = chipMap[d.chatStatus] || 'sg-chip-bot';
          const chipLabel = {
            BOT_AUTONOMOUS: 'Bot',
            ADMIN_LIVE: 'Live',
            RESOLVED: 'Done'
          }[d.chatStatus] || 'Bot';

          const avatarHtml = d.userPhoto
            ? `<img src="${d.userPhoto}" class="sg-thread-avatar" alt="${d.userName}" loading="lazy">`
            : `<div class="sg-thread-initials">${(d.userName || 'U')[0].toUpperCase()}</div>`;

          const unreadHtml = (d.adminUnread > 0)
            ? `<span class="sg-unread-pill">${d.adminUnread}</span>` : '';

          row.innerHTML = `
            ${avatarHtml}
            <span class="sg-thread-online-dot ${d.chatStatus !== 'RESOLVED' ? 'online' : 'offline'}"></span>
            <div class="min-w-0 flex-1">
              <div class="flex items-center justify-between gap-1 mb-0.5">
                <span class="text-xs font-bold truncate" style="color:#0F172A;max-width:110px;">${d.userName || 'User'}</span>
                <div class="flex items-center gap-1">${unreadHtml}<span class="sg-chip ${chipClass}">${chipLabel}</span></div>
              </div>
              <div class="truncate" style="font-size:0.68rem;color:#94A3B8;max-width:95%;">${d.lastMessage || 'No messages yet'}</div>
            </div>`;

          row.addEventListener('click', () => selectAdminThread(tid, d));
          elThreadsList.appendChild(row);
        });
      }

      function selectAdminThread(tid, threadData) {
        sgActiveThread = tid;

        // Highlight row
        document.querySelectorAll('.sg-thread-row').forEach(r => {
          r.classList.toggle('active-thread', r.dataset.tid === tid);
        });

        // Update toolbar
        if (elAdminSelUser) {
          elAdminSelUser.innerHTML = `<span class="font-bold" style="color:#0F172A;">${threadData.userName || 'User'}</span>&nbsp;<span style="color:#94A3B8;">${threadData.userEmail || ''}</span>`;
        }
        [elTakeover, elHandback, elResolve].forEach(b => b?.classList.remove('hidden'));

        // Enable reply
        if (elAdminInput) elAdminInput.disabled = false;
        if (elAdminSend)  elAdminSend.disabled  = false;
        elAdminInput?.focus();

        // Clear admin unread
        updateDoc(doc(db, 'support_threads', tid), { adminUnread: 0 }).catch(() => {});

        // Stream messages for this thread
        if (sgUnsubAdminMsgs) sgUnsubAdminMsgs();
        const mQuery = query(
          collection(db, 'support_threads', tid, 'messages'),
          orderBy('timestamp', 'asc')
        );
        sgUnsubAdminMsgs = onSnapshot(mQuery, snap => {
          const placeholder = document.getElementById('sg-admin-placeholder');
          if (placeholder) placeholder.remove();
          if (!elAdminMsgs) return;

          // Clear old msgs
          elAdminMsgs.querySelectorAll('.sg-admin-msg-row').forEach(n => n.remove());

          snap.forEach(ds => {
            const d = ds.data();
            const row = document.createElement('div');
            row.className = 'sg-admin-msg-row';
            const isUser  = d.sender === 'USER';
            const isAdmin = d.sender === 'ADMIN';
            row.style.cssText = 'display:flex;flex-direction:column;align-items:' + (isUser ? 'flex-end' : 'flex-start') + ';gap:2px;margin-bottom:6px;animation:sgfadein 0.18s ease both;';

            const label = document.createElement('div');
            label.style.cssText = 'font-size:0.58rem;font-family:monospace;color:#94A3B8;font-weight:700;padding:0 4px;text-transform:uppercase;letter-spacing:0.04em;';
            label.textContent = (d.senderName || d.sender) + (d.sender === 'SAVING_GUIDE' ? ' · Bot' : d.sender === 'ADMIN' ? ' · Agent' : ' · User');

            const bubble = document.createElement('div');
            bubble.style.cssText = 'max-width:76%;padding:8px 12px;border-radius:14px;font-size:0.78rem;font-family:Inter,sans-serif;line-height:1.5;word-break:break-word;' +
              (isUser ? 'background:#EFF6FF;color:#1E3A5F;border:1px solid #BFDBFE;border-bottom-right-radius:3px;' :
               isAdmin ? 'background:linear-gradient(135deg,#0B0F19,#1E293B);color:#F1F5F9;border-bottom-left-radius:3px;' :
               'background:#F8FAFC;color:#0F172A;border:1px solid #E2E8F0;border-bottom-left-radius:3px;');
            bubble.innerHTML = d.text;

            // Tick row for user messages
            if (isUser) {
              const tickRow = document.createElement('div');
              tickRow.style.cssText = 'display:flex;align-items:center;gap:3px;padding-right:2px;';
              tickRow.innerHTML = `<span style="font-size:0.56rem;color:#94A3B8;font-family:monospace;">${fmtTime(d.timestamp)}</span>${tickHTML(d.status || 'SENT')}`;
              row.appendChild(label);
              row.appendChild(bubble);
              row.appendChild(tickRow);
            } else {
              const timeEl = document.createElement('div');
              timeEl.style.cssText = 'font-size:0.56rem;color:#CBD5E1;font-family:monospace;padding-left:4px;';
              timeEl.textContent = fmtTime(d.timestamp);
              row.appendChild(label);
              row.appendChild(bubble);
              row.appendChild(timeEl);
            }

            elAdminMsgs.appendChild(row);
          });
          elAdminMsgs.scrollTop = elAdminMsgs.scrollHeight;

          // Mark user msgs as SEEN when admin has this thread open
          snap.forEach(ds => {
            const d = ds.data();
            if (d.sender === 'USER' && d.status !== 'SEEN') {
              updateDoc(ds.ref, { status: 'SEEN' }).catch(() => {});
            }
          });
        }, err => console.error('Admin msgs error', err));
      }

      // Admin Takeover
      elTakeover?.addEventListener('click', async () => {
        if (!sgActiveThread || !db) return;
        await updateDoc(doc(db, 'support_threads', sgActiveThread), {
          chatStatus: 'ADMIN_LIVE', lastMessageTime: serverTimestamp()
        }).catch(() => {});
        showToast('You have taken over this chat.', 'success');
      });

      // Admin Hand Back
      elHandback?.addEventListener('click', async () => {
        if (!sgActiveThread || !db) return;
        await updateDoc(doc(db, 'support_threads', sgActiveThread), {
          chatStatus: 'BOT_AUTONOMOUS', lastMessageTime: serverTimestamp()
        }).catch(() => {});
        showToast('Chat handed back to Saving Guide bot.', 'success');
      });

      // Admin Resolve
      elResolve?.addEventListener('click', async () => {
        if (!sgActiveThread || !db) return;
        await addDoc(collection(db, 'support_threads', sgActiveThread, 'messages'), {
          sender: 'ADMIN', senderName: 'Support Agent',
          text: '✅ This support session has been marked as <strong>resolved</strong>. Thank you for reaching out to SaveMoneyManually! 🙏',
          status: 'DELIVERED', timestamp: serverTimestamp()
        }).catch(() => {});
        await updateDoc(doc(db, 'support_threads', sgActiveThread), {
          chatStatus: 'RESOLVED', lastMessageTime: serverTimestamp(), adminUnread: 0
        }).catch(() => {});
        showToast('Thread resolved.', 'success');
      });

      // Admin send message
      async function adminSend() {
        if (sgAdminSendLock || !sgActiveThread || !db) return;
        const text = elAdminInput?.value?.trim();
        if (!text) return;
        sgAdminSendLock = true;
        if (elAdminInput) elAdminInput.value = '';

        try {
          await addDoc(collection(db, 'support_threads', sgActiveThread, 'messages'), {
            sender: 'ADMIN',
            senderName: currentUser?.displayName || 'Support Agent',
            text,
            status: 'DELIVERED',
            timestamp: serverTimestamp()
          });
          await updateDoc(doc(db, 'support_threads', sgActiveThread), {
            lastMessage: text.substring(0,80),
            lastMessageTime: serverTimestamp(),
            chatStatus: 'ADMIN_LIVE',
            userUnread: increment(1)
          });
        } catch (e) {
          console.error('Admin send error:', e);
          showToast('Failed to send reply.', 'error');
        } finally {
          sgAdminSendLock = false;
          elAdminInput?.focus();
        }
      }

      elAdminSend?.addEventListener('click', adminSend);
      elAdminInput?.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); adminSend(); }
      });

      // Close overlay on backdrop click
      elAdminOverlay?.addEventListener('click', (e) => {
        if (e.target === elAdminOverlay) {
          elAdminOverlay.classList.remove('open');
          heartbeatAdminPresence(false);
        }
      });
      elAdminClose?.addEventListener('click', () => {
        elAdminOverlay?.classList.remove('open');
        heartbeatAdminPresence(false);
      });

      // ── Hook into auth state ─────────────────────────────────────
      // Expose init function globally for onAuthStateChanged
      window.__sgInit = function(user) {
        if (!user) {
          sgThreadId = null;
          sgWindowOpen = false;
          closeWindow();
          if (sgUnsubMsgs)      { sgUnsubMsgs();      sgUnsubMsgs      = null; }
          if (sgUnsubThread)    { sgUnsubThread();    sgUnsubThread    = null; }
          if (sgUnsubAdmin)     { sgUnsubAdmin();     sgUnsubAdmin     = null; }
          if (sgUnsubAdminMsgs) { sgUnsubAdminMsgs(); sgUnsubAdminMsgs = null; }
          return;
        }
        watchAdminPresence();
        ensureThread(user);
        if (isAdmin(user)) initAdminDesk(user);
      };

    })(); // IIFE end

  