# -*- coding: utf-8 -*-
"""
Applies Critical Fix & Reset to index.html:
1. Brand Name: Replace 'Vault.fi' with 'SaveMoneyManually' everywhere.
2. Hero screen layout:
   - Top Pill Badge: ANTIGRAVITY AUTONOMOUS ENGINE
   - Headline: Autonomous Wealth. Zero Spreadsheets.
   - Subtitle: Continuous spare change round-ups, impulse cooldown locks, and background leakage prevention.
   - Single Action Button Only: Clean, white Continue with Google with official 4-color Google G icon.
   - DELETE "Enter Cockpit Instant" button completely.
   - Footnote: Firebase 256-bit Encrypted • v2.4.0-PROD
3. Preserve 3D Background & Canvas:
   - Pure white canvas with 24px subtle dot-matrix texture.
   - Three.js 3D wireframe mesh in Electric Cobalt Blue (#2563EB, opacity: 0.12) with cursor mouse-tracking.
4. Authenticated State:
   - When onAuthStateChanged triggers with logged-in user -> smoothly transition to main dashboard.
   - Main dashboard has LOWER navigation dock (Mobile bottom bar / Desktop lower rail) with 4 tabs: Home, Goals, Calendar, Ledger.
   - 0 Terms & Privacy links or mentions.
   - Full real-time Firestore sync (onSnapshot) with single-click debounced buttons.
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Title
html = html.replace(
    '<title>Vault.fi | Discipline Ledger &amp; Manual Wealth Cockpit</title>',
    '<title>SaveMoneyManually | Discipline Ledger &amp; Manual Wealth Cockpit</title>'
)

# 2. Update Desktop Sidebar Logo text
html = html.replace(
    '<div class="text-lg font-extrabold text-charcoal tracking-tight">Vault.fi</div>',
    '<div class="text-lg font-extrabold text-charcoal tracking-tight">SaveMoneyManually</div>'
)

# 3. Update Mobile Header Logo text
html = html.replace(
    '<div class="text-sm font-extrabold text-charcoal">Vault.fi</div>',
    '<div class="text-sm font-extrabold text-charcoal">SaveMoneyManually</div>'
)

# 4. Replace any fallback email user@vault.fi
html = html.replace("email: 'user@vault.fi'", "email: 'user@savemoneymanually.com'")

# 5. Rebuild Hero Screen (#auth-view)
idx_auth_start = html.find('<!-- 0. AUTHENTICATION')
if idx_auth_start == -1:
    idx_auth_start = html.find('<div id="auth-view"')
else:
    idx_auth_start = html.rfind('<!--', 0, idx_auth_start)

idx_auth_end = html.find('<!-- ============================================================ -->\n  <!-- 1. FULL AUTONOMOUS SPA COCKPIT')
if idx_auth_end == -1:
    idx_auth_end = html.find('<div id="dashboard-view"')

hero_html = """<!-- ============================================================ -->
  <!-- 0. AUTHENTICATION & HERO GATEWAY VIEW                        -->
  <!-- ============================================================ -->
  <div id="auth-view" class="relative z-10 min-h-screen flex items-center justify-center p-4">
    <div id="auth-card" class="metallic-card w-full max-w-[480px] p-8 sm:p-10 text-center relative overflow-hidden">
      
      <!-- Subtle top refraction highlight -->
      <div class="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-transparent via-blue-500/30 to-transparent"></div>

      <!-- Top Pill Badge -->
      <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-mono font-bold tracking-wider text-cobalt bg-blue-50 border border-blue-200/80 mb-6 uppercase">
        <span>✨</span> ANTIGRAVITY AUTONOMOUS ENGINE
      </div>

      <!-- Headline -->
      <h1 class="text-3xl sm:text-[36px] font-extrabold text-charcoal tracking-tight leading-[1.16] mb-3">
        Autonomous Wealth.<br />
        <span class="text-cobalt">Zero Spreadsheets.</span>
      </h1>

      <!-- Subtitle -->
      <p class="text-[14px] sm:text-[15px] leading-relaxed text-coolslate font-normal max-w-[380px] mx-auto mb-8">
        Continuous spare change round-ups, impulse cooldown locks, and background leakage prevention.
      </p>

      <!-- Single Action Button Only: Clean, White Continue with Google -->
      <div id="auth-action-box" class="w-full">
        <button id="btn-google-auth" class="w-full py-3.5 sm:py-4 px-5 bg-white hover:bg-slate-50 border border-slate-200/90 hover:border-slate-300 rounded-2xl shadow-sm hover:shadow-md transition-all duration-200 flex items-center justify-between text-left group cursor-pointer" type="button" aria-label="Continue with Google">
          <!-- Left: Official Google 'G' 4-Color SVG + Label -->
          <div class="flex items-center gap-3.5">
            <svg id="google-g-icon" class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" aria-hidden="true">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
            <span id="btn-auth-label" class="font-semibold text-[15px] text-charcoal">
              Continue with Google
            </span>
          </div>

          <!-- Right: Trailing Arrow Icon & Loading Spinner -->
          <div class="flex items-center">
            <svg id="trailing-arrow-icon" class="w-4 h-4 text-coolslate group-hover:text-cobalt group-hover:translate-x-1 transition-all duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
            <span id="btn-auth-spinner" class="hidden">
              <svg class="w-4 h-4 animate-spin text-cobalt" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            </span>
          </div>
        </button>
      </div>

      <!-- Auth Error Feedback -->
      <div id="auth-feedback" class="text-xs text-rose-600 font-medium hidden mt-3"></div>

      <!-- Footnote -->
      <div class="mt-8 pt-4 border-t border-slate-100 text-[11px] font-mono text-coolslate flex items-center justify-center gap-1.5">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
        <span>Firebase 256-bit Encrypted • v2.4.0-PROD</span>
      </div>
    </div>
  </div>

  """

html = html[:idx_auth_start] + hero_html + html[idx_auth_end:]
print("Replaced Auth View with exact original Hero Screen.")

# 6. Update JS Auth handling: Remove btnDemoEnter, update btnGoogleAuth logic & onAuthStateChanged
old_auth_js_marker = "btnDemoEnter?.addEventListener('click'"
idx_js_auth = html.find(old_auth_js_marker)
if idx_js_auth != -1:
    # Find the end of script tag
    idx_script_end = html.find('</script>', idx_js_auth)
    
    new_auth_js = """const trailingArrowIcon = document.getElementById('trailing-arrow-icon');

    btnGoogleAuth?.addEventListener('click', async () => {
      btnGoogleAuth.disabled = true;
      btnAuthLabel.textContent = "Connecting...";
      trailingArrowIcon?.classList.add('hidden');
      btnAuthSpinner?.classList.remove('hidden');
      authFeedback.classList.add('hidden');

      try {
        await signInWithPopup(auth, provider);
        // onAuthStateChanged will fire automatically with the authenticated user
      } catch (err) {
        console.error("Auth error:", err);
        let msg = "Could not authenticate with Google.";
        if (err.code === 'auth/popup-closed-by-user') msg = "Popup closed.";
        else if (err.code === 'auth/cancelled-popup-request') msg = "Popup request cancelled.";
        else if (err.code === 'auth/unauthorized-domain') {
          msg = "Domain not authorized in Firebase Console.";
        } else if (err.message) {
          msg = err.message;
        }
        authFeedback.textContent = msg;
        authFeedback.classList.remove('hidden');
      } finally {
        btnGoogleAuth.disabled = false;
        btnAuthLabel.textContent = "Continue with Google";
        trailingArrowIcon?.classList.remove('hidden');
        btnAuthSpinner?.classList.add('hidden');
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

    // Directly transitions to main dashboard when user is logged in
    onAuthStateChanged(auth, (user) => {
      if (user) {
        enterDashboard(user);
      } else {
        exitToAuth();
      }
    });
"""
    html = html[:idx_js_auth] + new_auth_js + '\n  ' + html[idx_script_end:]
    print("Replaced JS Auth handling with clean onAuthStateChanged and Google-only flow.")

# 7. Update exitToAuth to reset button state
old_exit = """    function exitToAuth() {
      dashboardView.classList.add('hidden');
      authView.style.display = 'flex';
      showToast('Signed out of session.', 'info');
    }"""
new_exit = """    function exitToAuth() {
      dashboardView.classList.add('hidden');
      authView.style.display = 'flex';
      if (btnGoogleAuth) {
        btnGoogleAuth.disabled = false;
        if (btnAuthLabel) btnAuthLabel.textContent = "Continue with Google";
        if (trailingArrowIcon) trailingArrowIcon.classList.remove('hidden');
        if (btnAuthSpinner) btnAuthSpinner.classList.add('hidden');
      }
      showToast('Signed out of session.', 'info');
    }"""
html = html.replace(old_exit, new_exit)

# Save updated index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved index.html successfully! Total length:", len(html))
