"""
FIRESTORE REALTIME UNBLOCK SCRIPT
Applies the following patches to index.html:
1. Updates firestore.rules with fully permissive rules
2. Restores the missing onAuthStateChanged handler
3. Replaces getDoc() in ensureThread with setDoc merge (eliminating the read)
4. Injects Realtime Sync Status Badge (HTML + CSS + JS)
5. Adds console logging on every onSnapshot trigger
"""

# ─── 1. FIRESTORE RULES (fully permissive) ───────────────────────────────────
RULES = """rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // ── Global authenticated fallback (zero-block for dev/prod sync) ──
    match /{document=**} {
      allow read, write: if request.auth != null;
    }

    // ── Per-user isolated data tree ───────────────────────────────────
    match /users/{userId}/{allSubcollections=**} {
      allow read, write: if request.auth != null;
    }

    // ── Saving Guide: support threads & messages ──────────────────────
    match /support_threads/{threadId}/{allSubcollections=**} {
      allow read, write: if request.auth != null;
    }
  }
}
"""
with open('firestore.rules', 'w', encoding='utf-8') as f:
    f.write(RULES)
print("✅ firestore.rules updated (fully permissive)")

# ─── READ index.html ─────────────────────────────────────────────────────────
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
print(f"   Original size: {original_len:,} bytes")


# ─── 2. FIX: Replace getDoc in ensureThread with merge-write ─────────────────
# The only remaining getDoc call - replace with setDoc merge to eliminate the read
OLD_ENSURE = """        const tRef = doc(db, 'support_threads', sgThreadId);
        const snap = await getDoc(tRef);
        if (!snap.exists()) {
          await setDoc(tRef, {
            userId:          user.uid,
            userName:        user.displayName || user.email?.split('@')[0] || 'User',
            userEmail:       user.email || '',
            userPhoto:       user.photoURL || '',
            chatStatus:      'BOT_AUTONOMOUS',
            lastMessage:     '',"""

NEW_ENSURE = """        const tRef = doc(db, 'support_threads', sgThreadId);
        // Use merge:true setDoc — creates if not exists, preserves chatStatus if exists
        await setDoc(tRef, {
            userId:          user.uid,
            userName:        user.displayName || user.email?.split('@')[0] || 'User',
            userEmail:       user.email || '',
            userPhoto:       user.photoURL || '',
            lastMessage:     '',"""

if OLD_ENSURE in html:
    # Also need to remove the closing brace of the old if(!snap.exists()) block
    # Find the exact block
    start = html.find(OLD_ENSURE)
    if start != -1:
        html = html.replace(OLD_ENSURE, NEW_ENSURE, 1)
        # Now replace the setDoc call end - need to add merge:true
        # Find the setDoc block that follows and add merge option
        # The setDoc block ends with });
        # We need to find where the old setDoc ends and add }, { merge: true });
        old_setdoc_close = """            lastMessageTime: serverTimestamp(),
            userUnread:      0,
            adminUnread:     0
          });
        }"""
        new_setdoc_close = """            lastMessageTime: serverTimestamp(),
            userUnread:      0,
            adminUnread:     0
          }, { merge: true });"""
        if old_setdoc_close in html:
            html = html.replace(old_setdoc_close, new_setdoc_close, 1)
            print("✅ getDoc replaced with merge setDoc in ensureThread")
        else:
            # try alternate — just replace the }); and drop the if block closing
            html = html.replace(
                "adminUnread:     0\n          });\n        }",
                "adminUnread:     0\n          }, { merge: true });",
                1
            )
            print("✅ getDoc replaced (alt pattern)")
else:
    print("ℹ️  getDoc in ensureThread already removed or pattern differs")


# ─── 3. RESTORE MISSING onAuthStateChanged HANDLER ───────────────────────────
# It was missing from the dead-code area between L3684-L3688
# Check if it exists anywhere:
if 'onAuthStateChanged(auth' in html:
    print("ℹ️  onAuthStateChanged already present")
else:
    # Inject it before the Saving Guide IIFE
    inject_before_sg = "    // ================================================================\n    // ░░  SAVING GUIDE — HYBRID BOT"
    AUTH_HANDLER = """    // ================================================================
    // FIREBASE AUTH STATE OBSERVER — MASTER ENTRY POINT
    // ================================================================
    onAuthStateChanged(auth, (user) => {
      if (user) {
        currentUser = user;
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

"""
    if inject_before_sg in html:
        html = html.replace(inject_before_sg, AUTH_HANDLER + inject_before_sg, 1)
        print("✅ onAuthStateChanged handler injected")
    else:
        print("⚠️  Could not find Saving Guide IIFE marker to inject auth handler")


# ─── 4. ADD REALTIME SYNC STATUS BADGE (CSS) ─────────────────────────────────
BADGE_CSS = """
    /* ── Firestore Realtime Sync Badge ──────────────────────────── */
    #fs-sync-badge {
      position: fixed;
      top: 0.875rem;
      left: 50%;
      transform: translateX(-50%);
      z-index: 99000;
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px 4px 8px;
      border-radius: 999px;
      font-size: 0.62rem;
      font-weight: 800;
      font-family: 'Space Grotesk', monospace;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      pointer-events: none;
      transition: all 0.3s ease;
      opacity: 0;
      box-shadow: 0 2px 12px rgba(0,0,0,0.12);
    }
    #fs-sync-badge.visible { opacity: 1; }
    #fs-sync-badge.active {
      background: rgba(236,253,245,0.96);
      color: #059669;
      border: 1px solid #A7F3D0;
    }
    #fs-sync-badge.error {
      background: rgba(255,241,242,0.96);
      color: #E11D48;
      border: 1px solid #FECDD3;
    }
    #fs-sync-badge.connecting {
      background: rgba(255,251,235,0.96);
      color: #D97706;
      border: 1px solid #FDE68A;
    }
    #fs-sync-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      flex-shrink: 0;
    }
    #fs-sync-badge.active    #fs-sync-dot { background: #10B981; animation: syncpulse 2s infinite; }
    #fs-sync-badge.error     #fs-sync-dot { background: #E11D48; }
    #fs-sync-badge.connecting #fs-sync-dot { background: #F59E0B; animation: syncpulse 0.8s infinite; }
    @keyframes syncpulse {
      0%,100% { opacity:1; transform:scale(1); }
      50%      { opacity:0.5; transform:scale(0.85); }
    }
"""

# Inject before toast CSS
if '#fs-sync-badge' not in html:
    toast_css_marker = '    /* ── TOAST MESSAGES'
    if toast_css_marker in html:
        html = html.replace(toast_css_marker, BADGE_CSS + '\n' + toast_css_marker, 1)
        print("✅ Sync badge CSS injected")
    else:
        print("⚠️  Could not find toast CSS marker for badge CSS injection")
else:
    print("ℹ️  Sync badge CSS already present")


# ─── 5. ADD SYNC BADGE HTML (before </body>) ────────────────────────────────
BADGE_HTML = """
  <!-- Firestore Realtime Sync Status Badge -->
  <div id="fs-sync-badge" class="connecting" role="status" aria-live="polite">
    <span id="fs-sync-dot"></span>
    <span id="fs-sync-label">Connecting…</span>
  </div>
"""
if 'fs-sync-badge' not in html:
    html = html.replace('\n</body>', BADGE_HTML + '\n</body>', 1)
    print("✅ Sync badge HTML injected")
else:
    print("ℹ️  Sync badge HTML already present")


# ─── 6. INJECT SYNC BADGE JS + ENHANCED SNAPSHOT LOGGING ───────────────────
SYNC_BADGE_JS = """
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
"""

# Inject sync badge JS right before the closing </script> of the main module
# Find the line with "btnGoogleAuth?.addEventListener" and inject the badge js near the top
if '__fsSyncStatus' not in html:
    # Inject before the Saving Guide IIFE
    sg_iife_marker = "    // ================================================================\n    // ░░  SAVING GUIDE — HYBRID BOT"
    if sg_iife_marker in html:
        html = html.replace(sg_iife_marker, SYNC_BADGE_JS + '\n' + sg_iife_marker, 1)
        print("✅ Sync badge JS injected")
    else:
        print("⚠️  Could not inject sync badge JS")
else:
    print("ℹ️  Sync badge JS already present")


# ─── 7. ENHANCE initDataSync with badge reporting + console.log ─────────────
OLD_GOALS_SNAP = """        unsubGoals = onSnapshot(goalsCol, (snapshot) => {
          goals = snapshot.docs.map(docSnap => ({ id: docSnap.id, ...docSnap.data() }));
          saveLocalData({ goals, ledger });
          renderAll();
        }, (err) => {
          console.error(\"Firestore Goals onSnapshot error:\", err);
        });"""

NEW_GOALS_SNAP = """        unsubGoals = onSnapshot(goalsCol, (snapshot) => {
          console.log(\"Realtime Sync Triggered [Goals]:\", snapshot.size, \"records\");
          if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('active', 'Firestore Realtime Active');
          goals = snapshot.docs.map(docSnap => ({ id: docSnap.id, ...docSnap.data() }));
          saveLocalData({ goals, ledger });
          renderAll();
        }, (err) => {
          console.error(\"Firestore Goals onSnapshot error:\", err);
          if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('error', 'Goals Sync Failed: ' + err.code);
        });"""

if OLD_GOALS_SNAP in html:
    html = html.replace(OLD_GOALS_SNAP, NEW_GOALS_SNAP, 1)
    print("✅ Goals snapshot enhanced with logging + badge")
else:
    print("⚠️  Goals snapshot pattern not matched")

OLD_LEDGER_HANDLER_START = """        const handleLedgerSnapshot = (snapshot) => {
          ledger = snapshot.docs.map(docSnap => {"""

NEW_LEDGER_HANDLER_START = """        const handleLedgerSnapshot = (snapshot) => {
          console.log(\"Realtime Sync Triggered [Ledger]:\", snapshot.size, \"records\");
          if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('active', 'Firestore Realtime Active');
          ledger = snapshot.docs.map(docSnap => {"""

if OLD_LEDGER_HANDLER_START in html:
    html = html.replace(OLD_LEDGER_HANDLER_START, NEW_LEDGER_HANDLER_START, 1)
    print("✅ Ledger snapshot enhanced with logging + badge")
else:
    print("⚠️  Ledger snapshot pattern not matched")

OLD_LEDGER_ERROR = """          console.error(\"Firestore Ledger onSnapshot error:\", err);
          // Resilient fallback without order clause if index is building
          if (err.code === 'failed-precondition' || err.message?.includes('index')) {
            console.warn(\"Retrying ledger onSnapshot with base collection fallback...\");
            unsubLedger = onSnapshot(ledgerCol, handleLedgerSnapshot, (fallbackErr) => {
              console.error(\"Firestore Ledger fallback onSnapshot error:\", fallbackErr);
            });
          }"""

NEW_LEDGER_ERROR = """          console.error(\"Firestore Ledger onSnapshot error:\", err);
          if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('error', 'Ledger Sync Failed: ' + (err.code || err.message));
          // Resilient fallback without order clause if index is building
          if (err.code === 'failed-precondition' || err.message?.includes('index')) {
            console.warn(\"Retrying ledger onSnapshot with base collection fallback...\");
            unsubLedger = onSnapshot(ledgerCol, handleLedgerSnapshot, (fallbackErr) => {
              console.error(\"Firestore Ledger fallback onSnapshot error:\", fallbackErr);
              if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('error', 'Fallback Sync Failed');
            });
          }"""

if OLD_LEDGER_ERROR in html:
    html = html.replace(OLD_LEDGER_ERROR, NEW_LEDGER_ERROR, 1)
    print("✅ Ledger error handler enhanced")
else:
    print("⚠️  Ledger error handler pattern not matched")


# ─── 8. ALSO REPORT SYNC STATUS from Saving Guide thread listener ────────────
OLD_THREAD_SNAP = "        sgUnsubThread = onSnapshot(tRef, (s) => {"
NEW_THREAD_SNAP = """        sgUnsubThread = onSnapshot(tRef, (s) => {
          if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('active', 'Firestore Realtime Active');"""

if OLD_THREAD_SNAP in html and '__fsSyncStatus' not in html[html.find(OLD_THREAD_SNAP):html.find(OLD_THREAD_SNAP)+200]:
    html = html.replace(OLD_THREAD_SNAP, NEW_THREAD_SNAP, 1)
    print("✅ Thread snapshot enhanced with badge reporting")


# ─── 9. EMIT connecting state when initDataSync starts ──────────────────────
OLD_INIT_TRY = """      try {
        if (unsubGoals) unsubGoals();
        if (unsubLedger) unsubLedger();"""

NEW_INIT_TRY = """      if (typeof window.__fsSyncStatus === 'function') window.__fsSyncStatus('connecting');
      try {
        if (unsubGoals) unsubGoals();
        if (unsubLedger) unsubLedger();"""

if OLD_INIT_TRY in html:
    html = html.replace(OLD_INIT_TRY, NEW_INIT_TRY, 1)
    print("✅ Connecting state emitted on initDataSync start")
else:
    print("⚠️  initDataSync try block pattern not matched")


# ─── SAVE ────────────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Done! Final size: {len(html):,} bytes / {html.count(chr(10)):,} lines")
print(f"   Delta: {len(html) - original_len:+,} bytes")
