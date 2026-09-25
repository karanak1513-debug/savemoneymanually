// ============================================================
// VAULT.FI — Firestore Data Layer
// Exact Schema Implementation:
// users/{userId}: { uid, email, displayName, photoURL, hourlyWage, streakCount, totalSaved, createdAt }
// users/{userId}/vaults/{vaultId}: { vaultId, title, targetAmount, currentAmount, deadline, category, isLocked, color, createdAt }
// users/{userId}/transactions/{txId}: { txId, amount, type ('DEPOSIT'|'EXPENSE'|'ROUNDUP'), category, vaultId, roundUpAmount, timestamp }
// users/{userId}/ai_insights/{insightId}: { insightId, type, severity ('CRITICAL'|'MODERATE'|'REWARD'), title, message, createdAt, dismissed }
// users/{userId}/cooldowns/{cooldownId}: { cooldownId, itemName, itemPrice, workHours, lockedUntil, durationHours, status, createdAt }
// ============================================================

import { db } from "../firebase-config.js";
import {
  collection,
  doc,
  addDoc,
  setDoc,
  updateDoc,
  deleteDoc,
  getDoc,
  getDocs,
  query,
  orderBy,
  limit,
  onSnapshot,
  serverTimestamp,
  increment,
  writeBatch,
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// ── References ───────────────────────────────────────────────
const userRef       = (uid) => doc(db, "users", uid);
const vaultsCol     = (uid) => collection(db, "users", uid, "vaults");
const vaultRef      = (uid, vid) => doc(db, "users", uid, "vaults", vid);
const txsCol        = (uid) => collection(db, "users", uid, "transactions");
const insightsCol   = (uid) => collection(db, "users", uid, "ai_insights");
const insightRef    = (uid, iid) => doc(db, "users", uid, "ai_insights", iid);
const cooldownsCol  = (uid) => collection(db, "users", uid, "cooldowns");
const cooldownRef   = (uid, cid) => doc(db, "users", uid, "cooldowns", cid);

// Local fallback memory store (used for demo mode or offline resilience)
const LOCAL_STORAGE_KEY = "vaultfi_local_state";
function getLocalStore() {
  try {
    const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (e) {
    return null;
  }
}
function saveLocalStore(data) {
  try {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(data));
  } catch (e) {}
}

// ── USER PROFILE ─────────────────────────────────────────────

export async function getUserProfile(uid) {
  try {
    const snap = await getDoc(userRef(uid));
    if (snap.exists()) {
      return { id: snap.id, ...snap.data() };
    }
  } catch (e) {
    console.warn("[Firestore] getUserProfile error, checking local store", e);
  }
  const local = getLocalStore();
  return local?.user || null;
}

export function subscribeUserProfile(uid, callback) {
  try {
    return onSnapshot(userRef(uid), (snap) => {
      if (snap.exists()) {
        callback({ id: snap.id, ...snap.data() });
      } else {
        const local = getLocalStore();
        if (local?.user) callback(local.user);
      }
    }, (err) => {
      console.warn("[Firestore] userProfile onSnapshot error, falling back to local:", err.message);
      const local = getLocalStore();
      if (local?.user) callback(local.user);
    });
  } catch (e) {
    const local = getLocalStore();
    if (local?.user) callback(local.user);
    return () => {};
  }
}

export async function updateUserProfile(uid, data) {
  try {
    await updateDoc(userRef(uid), {
      ...data,
      updatedAt: serverTimestamp(),
    });
  } catch (e) {
    console.warn("[Firestore] updateUserProfile error, updating local store", e);
  }
  const local = getLocalStore() || {};
  local.user = { ...(local.user || {}), ...data };
  saveLocalStore(local);
}

// ── SMART 3D VAULTS ──────────────────────────────────────────

export function subscribeVaults(uid, callback) {
  try {
    const q = query(vaultsCol(uid), orderBy("createdAt", "desc"));
    return onSnapshot(q, (snap) => {
      const vaults = snap.docs.map((d) => ({ vaultId: d.id, id: d.id, ...d.data() }));
      callback(vaults);
    }, (err) => {
      console.warn("[Firestore] subscribeVaults error, falling back to local:", err.message);
      const local = getLocalStore();
      callback(local?.vaults || []);
    });
  } catch (e) {
    const local = getLocalStore();
    callback(local?.vaults || []);
    return () => {};
  }
}

export async function createVault(uid, vaultData) {
  const payload = {
    title: vaultData.title || "New Vault",
    targetAmount: Number(vaultData.targetAmount) || 10000,
    currentAmount: Number(vaultData.currentAmount) || 0,
    deadline: vaultData.deadline || new Date(Date.now() + 30 * 86400000).toISOString().split("T")[0],
    category: (vaultData.category || "TECH").toUpperCase(),
    color: vaultData.color || "#00FFA3",
    isLocked: Boolean(vaultData.isLocked),
    createdAt: serverTimestamp(),
  };

  try {
    const docRef = await addDoc(vaultsCol(uid), payload);
    return docRef.id;
  } catch (e) {
    console.warn("[Firestore] createVault fallback to local", e);
    const local = getLocalStore() || {};
    local.vaults = local.vaults || [];
    const id = "v_" + Date.now();
    local.vaults.unshift({ vaultId: id, id, ...payload, createdAt: new Date().toISOString() });
    saveLocalStore(local);
    return id;
  }
}

export async function updateVault(uid, vaultId, data) {
  try {
    await updateDoc(vaultRef(uid, vaultId), data);
  } catch (e) {
    console.warn("[Firestore] updateVault fallback to local", e);
    const local = getLocalStore() || {};
    if (local.vaults) {
      const idx = local.vaults.findIndex((v) => v.vaultId === vaultId || v.id === vaultId);
      if (idx !== -1) {
        local.vaults[idx] = { ...local.vaults[idx], ...data };
        saveLocalStore(local);
      }
    }
  }
}

export async function deleteVault(uid, vaultId) {
  try {
    await deleteDoc(vaultRef(uid, vaultId));
  } catch (e) {
    console.warn("[Firestore] deleteVault fallback to local", e);
    const local = getLocalStore() || {};
    if (local.vaults) {
      local.vaults = local.vaults.filter((v) => v.vaultId !== vaultId && v.id !== vaultId);
      saveLocalStore(local);
    }
  }
}

/**
 * Deposit funds to a vault and update totalSaved and log transaction
 */
export async function depositToVault(uid, vaultId, amount, note = "Vault Deposit") {
  const num = Math.max(1, Number(amount) || 0);
  try {
    const batch = writeBatch(db);
    // 1. Update Vault
    const vRef = vaultRef(uid, vaultId);
    batch.update(vRef, {
      currentAmount: increment(num),
      updatedAt: serverTimestamp(),
    });
    // 2. Update User totalSaved
    const uRef = userRef(uid);
    batch.update(uRef, {
      totalSaved: increment(num),
    });
    // 3. Create Transaction
    const newTxRef = doc(txsCol(uid));
    batch.set(newTxRef, {
      txId: newTxRef.id,
      amount: num,
      type: "DEPOSIT",
      category: "SAVINGS",
      vaultId,
      roundUpAmount: 0,
      note,
      timestamp: serverTimestamp(),
    });
    await batch.commit();
  } catch (e) {
    console.warn("[Firestore] depositToVault fallback to local", e);
    const local = getLocalStore() || {};
    if (local.vaults) {
      const v = local.vaults.find((item) => item.vaultId === vaultId || item.id === vaultId);
      if (v) v.currentAmount = (v.currentAmount || 0) + num;
    }
    if (local.user) {
      local.user.totalSaved = (local.user.totalSaved || 0) + num;
    }
    local.transactions = local.transactions || [];
    local.transactions.unshift({
      txId: "tx_" + Date.now(),
      amount: num,
      type: "DEPOSIT",
      category: "SAVINGS",
      vaultId,
      roundUpAmount: 0,
      note,
      timestamp: new Date().toISOString(),
    });
    saveLocalStore(local);
  }
}

/**
 * Withdraw funds from a vault (if not locked)
 */
export async function withdrawFromVault(uid, vaultId, amount, note = "Vault Withdrawal") {
  const num = Math.max(1, Number(amount) || 0);
  try {
    const batch = writeBatch(db);
    const vRef = vaultRef(uid, vaultId);
    batch.update(vRef, {
      currentAmount: increment(-num),
      updatedAt: serverTimestamp(),
    });
    const uRef = userRef(uid);
    batch.update(uRef, {
      totalSaved: increment(-num),
    });
    const newTxRef = doc(txsCol(uid));
    batch.set(newTxRef, {
      txId: newTxRef.id,
      amount: num,
      type: "EXPENSE",
      category: "WITHDRAWAL",
      vaultId,
      roundUpAmount: 0,
      note,
      timestamp: serverTimestamp(),
    });
    await batch.commit();
  } catch (e) {
    console.warn("[Firestore] withdrawFromVault fallback to local", e);
    const local = getLocalStore() || {};
    if (local.vaults) {
      const v = local.vaults.find((item) => item.vaultId === vaultId || item.id === vaultId);
      if (v) v.currentAmount = Math.max(0, (v.currentAmount || 0) - num);
    }
    if (local.user) {
      local.user.totalSaved = Math.max(0, (local.user.totalSaved || 0) - num);
    }
    local.transactions = local.transactions || [];
    local.transactions.unshift({
      txId: "tx_" + Date.now(),
      amount: num,
      type: "EXPENSE",
      category: "WITHDRAWAL",
      vaultId,
      roundUpAmount: 0,
      note,
      timestamp: new Date().toISOString(),
    });
    saveLocalStore(local);
  }
}

// ── TRANSACTIONS ─────────────────────────────────────────────

export function subscribeTransactions(uid, callback) {
  try {
    const q = query(txsCol(uid), orderBy("timestamp", "desc"), limit(40));
    return onSnapshot(q, (snap) => {
      const txs = snap.docs.map((d) => ({ txId: d.id, id: d.id, ...d.data() }));
      callback(txs);
    }, (err) => {
      console.warn("[Firestore] subscribeTransactions error, using local:", err.message);
      const local = getLocalStore();
      callback(local?.transactions || []);
    });
  } catch (e) {
    const local = getLocalStore();
    callback(local?.transactions || []);
    return () => {};
  }
}

export async function createTransaction(uid, data) {
  const payload = {
    amount: Number(data.amount) || 0,
    type: data.type || "EXPENSE", // 'DEPOSIT' | 'EXPENSE' | 'ROUNDUP'
    category: data.category || "GENERAL",
    vaultId: data.vaultId || null,
    roundUpAmount: Number(data.roundUpAmount) || 0,
    note: data.note || "",
    timestamp: serverTimestamp(),
  };

  try {
    const docRef = await addDoc(txsCol(uid), payload);
    // If there is roundUpAmount and auto-save enabled, increment totalSaved
    if (payload.roundUpAmount > 0) {
      try {
        await updateDoc(userRef(uid), {
          totalSaved: increment(payload.roundUpAmount),
        });
      } catch (err) {}
    }
    return docRef.id;
  } catch (e) {
    console.warn("[Firestore] createTransaction fallback to local", e);
    const local = getLocalStore() || {};
    local.transactions = local.transactions || [];
    const id = "tx_" + Date.now();
    local.transactions.unshift({ txId: id, id, ...payload, timestamp: new Date().toISOString() });
    if (payload.roundUpAmount > 0 && local.user) {
      local.user.totalSaved = (local.user.totalSaved || 0) + payload.roundUpAmount;
    }
    saveLocalStore(local);
    return id;
  }
}

// ── AI INSIGHTS & LEAKAGE AUDIT ──────────────────────────────

export function subscribeInsights(uid, callback) {
  try {
    const q = query(insightsCol(uid), orderBy("createdAt", "desc"));
    return onSnapshot(q, (snap) => {
      const insights = snap.docs.map((d) => ({ insightId: d.id, id: d.id, ...d.data() }));
      callback(insights.filter((i) => !i.dismissed));
    }, (err) => {
      console.warn("[Firestore] subscribeInsights error, using local:", err.message);
      const local = getLocalStore();
      callback((local?.insights || []).filter((i) => !i.dismissed));
    });
  } catch (e) {
    const local = getLocalStore();
    callback((local?.insights || []).filter((i) => !i.dismissed));
    return () => {};
  }
}

export async function dismissInsight(uid, insightId) {
  try {
    await updateDoc(insightRef(uid, insightId), { dismissed: true });
  } catch (e) {
    console.warn("[Firestore] dismissInsight fallback to local", e);
    const local = getLocalStore() || {};
    if (local.insights) {
      const item = local.insights.find((i) => i.insightId === insightId || i.id === insightId);
      if (item) item.dismissed = true;
      saveLocalStore(local);
    }
  }
}

export async function cutExpenseAndAddToVault(uid, insightId, savingsAmount, targetVaultId = null) {
  try {
    // 1. Mark insight as dismissed/acted
    await dismissInsight(uid, insightId);
    // 2. Deposit the reclaimed amount
    if (targetVaultId) {
      await depositToVault(uid, targetVaultId, savingsAmount, "Reclaimed via AI Leak Cut");
    } else {
      // General savings
      await updateDoc(userRef(uid), {
        totalSaved: increment(savingsAmount),
      });
      await addDoc(txsCol(uid), {
        amount: savingsAmount,
        type: "ROUNDUP",
        category: "LEAK_CUT",
        roundUpAmount: savingsAmount,
        note: "AI Expense Leak Reclaimed",
        timestamp: serverTimestamp(),
      });
    }
  } catch (e) {
    console.warn("[Firestore] cutExpenseAndAddToVault fallback", e);
  }
}

// ── IMPULSE BUY COOLDOWN CHAMBER ─────────────────────────────

export function subscribeCooldowns(uid, callback) {
  try {
    const q = query(cooldownsCol(uid), orderBy("createdAt", "desc"));
    return onSnapshot(q, (snap) => {
      const cooldowns = snap.docs.map((d) => ({ cooldownId: d.id, id: d.id, ...d.data() }));
      callback(cooldowns);
    }, (err) => {
      console.warn("[Firestore] subscribeCooldowns error, using local:", err.message);
      const local = getLocalStore();
      callback(local?.cooldowns || []);
    });
  } catch (e) {
    const local = getLocalStore();
    callback(local?.cooldowns || []);
    return () => {};
  }
}

export async function createCooldown(uid, data) {
  const hours = Number(data.durationHours) || 24;
  const lockedUntil = new Date(Date.now() + hours * 3600 * 1000).toISOString();
  const payload = {
    itemName: data.itemName || "Impulse Item",
    itemPrice: Number(data.itemPrice) || 0,
    workHours: Number(data.workHours) || 0,
    durationHours: hours,
    lockedUntil,
    status: "ACTIVE", // 'ACTIVE' | 'EXPIRED' | 'SAVED' | 'BOUGHT'
    createdAt: serverTimestamp(),
  };

  try {
    const docRef = await addDoc(cooldownsCol(uid), payload);
    return docRef.id;
  } catch (e) {
    console.warn("[Firestore] createCooldown fallback to local", e);
    const local = getLocalStore() || {};
    local.cooldowns = local.cooldowns || [];
    const id = "cd_" + Date.now();
    local.cooldowns.unshift({ cooldownId: id, id, ...payload, createdAt: new Date().toISOString() });
    saveLocalStore(local);
    return id;
  }
}

export async function resolveCooldown(uid, cooldownId, action, vaultId = null) {
  // action: 'SAVED' (send to vault) | 'BOUGHT' (logged as expense) | 'CANCELLED' (walk away)
  try {
    await updateDoc(cooldownRef(uid, cooldownId), {
      status: action,
      resolvedAt: serverTimestamp(),
    });
  } catch (e) {
    console.warn("[Firestore] resolveCooldown fallback", e);
    const local = getLocalStore() || {};
    if (local.cooldowns) {
      const item = local.cooldowns.find((c) => c.cooldownId === cooldownId || c.id === cooldownId);
      if (item) item.status = action;
      saveLocalStore(local);
    }
  }
}

// ── INITIAL SEED DATA GENERATOR ──────────────────────────────
export async function seedInitialUserData(uid, user) {
  const initialUser = {
    uid,
    email: user.email || "genz.saver@vault.fi",
    displayName: user.displayName || "Alex Rivers",
    photoURL: user.photoURL || null,
    hourlyWage: 520, // default ₹520/hr
    monthlyIncome: 90000,
    streakCount: 7,
    totalSaved: 48650,
    roundUpMultiplier: 50, // nearest ₹50
    createdAt: serverTimestamp(),
  };

  const sampleVaults = [
    {
      title: "MacBook Pro M3 Max",
      targetAmount: 180000,
      currentAmount: 135000,
      deadline: "2026-11-15",
      category: "TECH",
      color: "#00FFA3",
      isLocked: false,
    },
    {
      title: "Tokyo Cyberpunk Trip 2026",
      targetAmount: 120000,
      currentAmount: 78000,
      deadline: "2026-12-31",
      category: "TRAVEL",
      color: "#00D2FF",
      isLocked: false,
    },
    {
      title: "Emergency F*** Off Fund",
      targetAmount: 100000,
      currentAmount: 62500,
      deadline: "2027-03-31",
      category: "EMERGENCY",
      color: "#FF007A",
      isLocked: true,
    },
    {
      title: "Acronym Streetwear Grails",
      targetAmount: 45000,
      currentAmount: 45000, // 100% Celebration demo!
      deadline: "2026-10-01",
      category: "LIFESTYLE",
      color: "#A855F7",
      isLocked: false,
    },
  ];

  const sampleTransactions = [
    {
      amount: 450,
      type: "EXPENSE",
      category: "FOOD",
      roundUpAmount: 50,
      note: "Third Wave Coffee Cold Brew",
      timestamp: new Date(Date.now() - 3600 * 1000 * 2).toISOString(),
    },
    {
      amount: 50,
      type: "ROUNDUP",
      category: "ROUNDUP",
      vaultId: null,
      roundUpAmount: 50,
      note: "Spare Change Stash",
      timestamp: new Date(Date.now() - 3600 * 1000 * 2).toISOString(),
    },
    {
      amount: 5000,
      type: "DEPOSIT",
      category: "SAVINGS",
      vaultId: "seed_v1",
      roundUpAmount: 0,
      note: "Freelance UI Project Payday",
      timestamp: new Date(Date.now() - 86400 * 1000 * 1).toISOString(),
    },
    {
      amount: 1450,
      type: "EXPENSE",
      category: "ENTERTAINMENT",
      roundUpAmount: 50,
      note: "Weekend Swiggy Late Feast",
      timestamp: new Date(Date.now() - 86400 * 1000 * 2).toISOString(),
    },
    {
      amount: 2500,
      type: "DEPOSIT",
      category: "SAVINGS",
      vaultId: "seed_v2",
      roundUpAmount: 0,
      note: "Weekly disciplined transfer",
      timestamp: new Date(Date.now() - 86400 * 1000 * 4).toISOString(),
    },
  ];

  const sampleInsights = [
    {
      type: "LEAK",
      severity: "CRITICAL",
      title: "Late-Night Delivery Drain",
      message: "You dropped ₹1,450 on fast food this weekend. Your iPhone goal was pushed back by 4 days. Was that soggy burger really worth it?",
      createdAt: new Date().toISOString(),
      dismissed: false,
    },
    {
      type: "SUBSCRIPTION",
      severity: "MODERATE",
      title: "Zombie OTT Subscriptions",
      message: "You're paying for 3 streaming platforms. Unless you have 6 eyes, cancel two and put ₹1,299/mo straight into your Tokyo vault.",
      createdAt: new Date(Date.now() - 86400 * 1000).toISOString(),
      dismissed: false,
    },
    {
      type: "STREAK",
      severity: "REWARD",
      title: "7-Day Discipline Crown 👑",
      message: "Zero impulse purchases logged this week! You dodged 3 spontaneous checkouts. That's ₹4,200 kept in your pocket.",
      createdAt: new Date(Date.now() - 86400 * 1000 * 3).toISOString(),
      dismissed: false,
    },
  ];

  const sampleCooldowns = [
    {
      itemName: "Sony WH-1000XM5 Headphones",
      itemPrice: 26990,
      workHours: 51.9,
      durationHours: 48,
      lockedUntil: new Date(Date.now() + 3600 * 1000 * 18).toISOString(),
      status: "ACTIVE",
      createdAt: new Date(Date.now() - 3600 * 1000 * 30).toISOString(),
    },
    {
      itemName: "Mechanical Custom Keyboard",
      itemPrice: 12500,
      workHours: 24.0,
      durationHours: 24,
      lockedUntil: new Date(Date.now() - 3600 * 1000 * 2).toISOString(),
      status: "EXPIRED",
      createdAt: new Date(Date.now() - 3600 * 1000 * 26).toISOString(),
    }
  ];

  // Try writing to Firestore
  try {
    const userDocSnap = await getDoc(userRef(uid));
    if (!userDocSnap.exists()) {
      await setDoc(userRef(uid), initialUser);

      // Add sample vaults
      for (const v of sampleVaults) {
        await addDoc(vaultsCol(uid), { ...v, createdAt: serverTimestamp() });
      }
      // Add sample transactions
      for (const t of sampleTransactions) {
        await addDoc(txsCol(uid), { ...t, timestamp: serverTimestamp() });
      }
      // Add sample insights
      for (const i of sampleInsights) {
        await addDoc(insightsCol(uid), { ...i, createdAt: serverTimestamp() });
      }
      // Add sample cooldowns
      for (const c of sampleCooldowns) {
        await addDoc(cooldownsCol(uid), { ...c, createdAt: serverTimestamp() });
      }
    }
  } catch (e) {
    console.warn("[Firestore] seed error, writing to localStorage fallback", e);
  }

  // Also prime local store for instant rendering
  const local = {
    user: { ...initialUser, uid },
    vaults: sampleVaults.map((v, i) => ({ vaultId: "seed_v" + i, id: "seed_v" + i, ...v })),
    transactions: sampleTransactions.map((t, i) => ({ txId: "seed_tx" + i, id: "seed_tx" + i, ...t })),
    insights: sampleInsights.map((ins, i) => ({ insightId: "seed_i" + i, id: "seed_i" + i, ...ins })),
    cooldowns: sampleCooldowns.map((c, i) => ({ cooldownId: "seed_c" + i, id: "seed_c" + i, ...c })),
  };
  saveLocalStore(local);
  return local;
}
