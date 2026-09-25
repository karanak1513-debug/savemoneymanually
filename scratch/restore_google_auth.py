"""
Script to restore high-precision One-Click Google Authentication:
1. Removes Email/Password form, tabs, and forgot password panels from #auth-card
2. Keeps single official Google button (googleLoginBtn) with metallic hover shine & arrow
3. Keeps Instant Demo Mode button
4. Updates Firebase imports to include setPersistence & browserLocalPersistence
5. Implements window.handleGoogleLogin and robust onAuthStateChanged
"""
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Firebase Auth imports
old_import = """    import {
      getAuth,
      GoogleAuthProvider,
      signInWithPopup,
      signInWithEmailAndPassword,
      createUserWithEmailAndPassword,
      sendPasswordResetEmail,
      updateProfile,
      signOut,
      onAuthStateChanged
    } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";"""

new_import = """    import {
      getAuth,
      signInWithPopup,
      GoogleAuthProvider,
      onAuthStateChanged,
      setPersistence,
      browserLocalPersistence,
      signOut
    } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";"""

assert old_import in content, "Could not find old_import in index.html"
content = content.replace(old_import, new_import, 1)
print("1. Updated Firebase Auth imports")

# 2. Update Auth Card markup in HTML
old_auth_card_content = """      <!-- Google One-Click Authentication Button -->
      <div id="auth-action-box" class="w-full mb-3">
        <button id="btn-google-auth" class="w-full py-3 px-4 bg-white hover:bg-slate-50 border border-slate-200 hover:border-slate-300 rounded-xl shadow-xs hover:shadow-sm transition-all duration-200 flex items-center justify-between text-left group cursor-pointer" type="button" aria-label="Continue with Google">
          <div class="flex items-center gap-3">
            <svg id="google-g-icon" class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" aria-hidden="true">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
            <span id="btn-auth-label" class="font-semibold text-[14px] text-charcoal">
              Continue with Google
            </span>
          </div>
          <div class="flex items-center">
            <svg id="trailing-arrow-icon" class="w-4 h-4 text-coolslate group-hover:text-cobalt group-hover:translate-x-0.5 transition-all duration-200" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
            <span id="btn-auth-spinner" class="hidden">
              <svg class="w-4 h-4 animate-spin text-cobalt" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            </span>
          </div>
        </button>
      </div>

      <!-- Divider: OR CONTINUE WITH EMAIL -->
      <div class="relative flex items-center justify-center my-4">
        <div class="border-t border-slate-200/80 w-full"></div>
        <span class="bg-white px-3 text-[10px] font-mono uppercase tracking-wider text-slate-400 font-semibold absolute">
          or continue with email
        </span>
      </div>

      <!-- Tab Switcher: Sign In vs Create Account -->
      <div class="grid grid-cols-2 p-1 bg-slate-100/90 rounded-xl mb-3 text-xs font-semibold text-slate-500">
        <button id="tab-auth-signin" type="button" class="py-1.5 rounded-lg bg-white text-charcoal shadow-xs transition-all duration-150 cursor-pointer">
          Sign In
        </button>
        <button id="tab-auth-signup" type="button" class="py-1.5 rounded-lg hover:text-charcoal transition-all duration-150 cursor-pointer">
          Create Account
        </button>
      </div>

      <!-- Email / Password Form -->
      <form id="email-auth-form" class="space-y-3 text-left" novalidate>
        <!-- Full Name (Only for Sign Up) -->
        <div id="auth-name-group" class="hidden space-y-1">
          <label for="auth-name" class="block text-xs font-semibold text-slate-700">Full Name</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            </span>
            <input id="auth-name" type="text" autocomplete="name" placeholder="Alex Morgan" class="w-full pl-9 pr-3 py-2 bg-slate-50/60 hover:bg-slate-50 focus:bg-white border border-slate-200 focus:border-cobalt rounded-xl text-xs sm:text-sm text-charcoal placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-100 transition-all" />
          </div>
        </div>

        <!-- Email Address -->
        <div class="space-y-1">
          <label for="auth-email" class="block text-xs font-semibold text-slate-700">Email Address</label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
            </span>
            <input id="auth-email" type="email" autocomplete="email" required placeholder="you@example.com" class="w-full pl-9 pr-3 py-2 bg-slate-50/60 hover:bg-slate-50 focus:bg-white border border-slate-200 focus:border-cobalt rounded-xl text-xs sm:text-sm text-charcoal placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-100 transition-all" />
          </div>
        </div>

        <!-- Password -->
        <div class="space-y-1">
          <div class="flex items-center justify-between">
            <label for="auth-password" class="block text-xs font-semibold text-slate-700">Password</label>
            <button id="btn-forgot-password" type="button" class="text-[11px] font-medium text-cobalt hover:underline cursor-pointer">
              Forgot password?
            </button>
          </div>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
            </span>
            <input id="auth-password" type="password" autocomplete="current-password" required placeholder="••••••••" class="w-full pl-9 pr-10 py-2 bg-slate-50/60 hover:bg-slate-50 focus:bg-white border border-slate-200 focus:border-cobalt rounded-xl text-xs sm:text-sm text-charcoal placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-100 transition-all" />
            <button id="btn-toggle-password" type="button" class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 cursor-pointer" aria-label="Toggle password visibility">
              <svg id="icon-eye-show" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
              <svg id="icon-eye-hide" class="w-4 h-4 hidden" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18"/></svg>
            </button>
          </div>
          <p id="password-hint" class="hidden text-[11px] text-slate-400 pt-0.5">Minimum 6 characters required.</p>
        </div>

        <!-- Submit Button -->
        <button id="btn-email-submit" type="submit" class="w-full mt-2 py-2.5 px-4 bg-cobalt hover:bg-cobalt-hover text-white font-semibold text-xs sm:text-sm rounded-xl shadow-xs hover:shadow-md transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed">
          <span id="btn-email-submit-label">Sign In to Cockpit</span>
          <span id="btn-email-submit-spinner" class="hidden">
            <svg class="w-4 h-4 animate-spin text-white" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
          </span>
        </button>
      </form>

      <!-- Forgot Password View (Inline Panel) -->
      <div id="forgot-password-panel" class="hidden text-left space-y-3 pt-1">
        <div class="flex items-center justify-between">
          <h3 class="text-xs font-bold uppercase tracking-wider text-slate-700">Reset Password</h3>
          <button id="btn-back-to-login" type="button" class="text-xs font-semibold text-cobalt hover:underline cursor-pointer">
            ← Back to Sign In
          </button>
        </div>
        <p class="text-xs text-slate-500 leading-relaxed">
          Enter your registered email and we will send a secure link to reset your password.
        </p>
        <div class="relative">
          <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </span>
          <input id="forgot-email" type="email" placeholder="you@example.com" class="w-full pl-9 pr-3 py-2 bg-slate-50/60 hover:bg-slate-50 focus:bg-white border border-slate-200 focus:border-cobalt rounded-xl text-xs sm:text-sm text-charcoal placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-100 transition-all" />
        </div>
        <button id="btn-send-reset" type="button" class="w-full py-2.5 px-4 bg-slate-900 hover:bg-black text-white font-semibold text-xs rounded-xl shadow-xs transition-all flex items-center justify-center gap-2 cursor-pointer">
          <span id="btn-send-reset-label">Send Reset Link</span>
          <span id="btn-send-reset-spinner" class="hidden">
            <svg class="w-3.5 h-3.5 animate-spin text-white" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
          </span>
        </button>
      </div>

      <!-- Auth Error / Success Feedback Banner -->
      <div id="auth-feedback" class="text-xs font-medium hidden mt-3 p-2.5 rounded-xl flex items-start gap-2 text-left"></div>

      <!-- Instant Demo Mode Access -->
      <div class="mt-4 pt-3 border-t border-slate-100/90">
        <button id="btn-demo-mode" type="button" class="w-full py-2.5 px-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200/80 text-xs font-semibold text-slate-600 hover:text-charcoal transition-all flex items-center justify-center gap-1.5 cursor-pointer shadow-xs">
          <span>⚡</span>
          <span>Explore Demo Cockpit (Offline Preview)</span>
        </button>
      </div>"""

new_auth_card_content = """      <!-- High-Precision Official Google Authentication Button -->
      <div id="auth-action-box" class="w-full">
        <button id="googleLoginBtn" onclick="window.handleGoogleLogin()" class="w-full py-3.5 sm:py-4 px-5 bg-white hover:bg-slate-50 border border-slate-200/90 hover:border-blue-400/80 rounded-2xl shadow-sm hover:shadow-md hover:shadow-blue-500/10 transition-all duration-200 flex items-center justify-between text-left group cursor-pointer" type="button" aria-label="Continue with Google">
          <!-- Left: Official Google 'G' 4-Color SVG + Label -->
          <div class="flex items-center gap-3.5">
            <svg id="google-g-icon" class="w-5 h-5 flex-shrink-0" viewBox="0 0 24 24" aria-hidden="true">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
            </svg>
            <span id="btn-auth-label" class="font-bold text-[15px] text-charcoal group-hover:text-cobalt transition-colors">
              Continue with Google
            </span>
          </div>

          <!-- Right: Subtle Arrow Icon & Loading Spinner -->
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

      <!-- Auth Error Feedback Alert -->
      <div id="authErrorBadge" class="hidden mt-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-600 text-xs font-semibold text-center"></div>

      <!-- Instant Demo Mode Access -->
      <div class="mt-4 pt-3 border-t border-slate-100/90">
        <button id="btn-demo-mode" type="button" class="w-full py-2.5 px-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200/80 text-xs font-semibold text-slate-600 hover:text-charcoal transition-all flex items-center justify-center gap-1.5 cursor-pointer shadow-xs">
          <span>⚡</span>
          <span>Explore Demo Cockpit (Offline Preview)</span>
        </button>
      </div>"""

assert old_auth_card_content in content, "Could not find old_auth_card_content in index.html"
content = content.replace(old_auth_card_content, new_auth_card_content, 1)
print("2. Replaced Auth Card with single official Google Login button")

# 3. Replace auth controller script
old_auth_logic = """    const trailingArrowIcon = document.getElementById('trailing-arrow-icon');

    // ── Email / Password & Google Auth Elements ────────────────────
    const tabAuthSignIn = document.getElementById('tab-auth-signin');
    const tabAuthSignUp = document.getElementById('tab-auth-signup');
    const emailAuthForm = document.getElementById('email-auth-form');
    const authNameGroup = document.getElementById('auth-name-group');
    const authName = document.getElementById('auth-name');
    const authEmail = document.getElementById('auth-email');
    const authPassword = document.getElementById('auth-password');
    const passwordHint = document.getElementById('password-hint');
    const btnTogglePassword = document.getElementById('btn-toggle-password');
    const iconEyeShow = document.getElementById('icon-eye-show');
    const iconEyeHide = document.getElementById('icon-eye-hide');
    const btnForgotPassword = document.getElementById('btn-forgot-password');
    const btnEmailSubmit = document.getElementById('btn-email-submit');
    const btnEmailSubmitLabel = document.getElementById('btn-email-submit-label');
    const btnEmailSubmitSpinner = document.getElementById('btn-email-submit-spinner');

    const forgotPasswordPanel = document.getElementById('forgot-password-panel');
    const forgotEmail = document.getElementById('forgot-email');
    const btnBackToLogin = document.getElementById('btn-back-to-login');
    const btnSendReset = document.getElementById('btn-send-reset');
    const btnSendResetLabel = document.getElementById('btn-send-reset-label');
    const btnSendResetSpinner = document.getElementById('btn-send-reset-spinner');

    let authMode = 'signin'; // 'signin' or 'signup'

    // Helper: Display Alert Banner (Error or Success)
    function showAuthAlert(msg, type = 'error') {
      if (!authFeedback) return;
      authFeedback.className = 'text-xs font-medium mt-3 p-2.5 rounded-xl flex items-start gap-2 text-left ' +
        (type === 'success' 
          ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' 
          : 'bg-rose-50 text-rose-700 border border-rose-200');
      
      const iconSvg = type === 'success'
        ? '<svg class="w-4 h-4 flex-shrink-0 mt-0.5 text-emerald-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>'
        : '<svg class="w-4 h-4 flex-shrink-0 mt-0.5 text-rose-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>';
      
      authFeedback.innerHTML = `${iconSvg}<div>${msg}</div>`;
      authFeedback.classList.remove('hidden');
    }

    function clearAuthAlert() {
      if (authFeedback) {
        authFeedback.classList.add('hidden');
        authFeedback.innerHTML = '';
      }
    }

    // Friendly Firebase Error Formatter
    function formatAuthError(err) {
      console.error("[FirebaseAuth]", err?.code, err?.message);
      switch (err?.code) {
        case 'auth/invalid-credential':
        case 'auth/wrong-password':
          return "Invalid email or password. Please verify your credentials.";
        case 'auth/user-not-found':
          return "No account found with this email. Switch to 'Create Account' to register.";
        case 'auth/email-already-in-use':
          return "An account with this email already exists. Switch to 'Sign In'.";
        case 'auth/weak-password':
          return "Password is too weak. Please use at least 6 characters.";
        case 'auth/invalid-email':
          return "Please enter a valid email address.";
        case 'auth/popup-closed-by-user':
          return "Google sign-in popup was closed before completing.";
        case 'auth/cancelled-popup-request':
          return "Google sign-in request was cancelled.";
        case 'auth/unauthorized-domain':
          return "Domain is not authorized in Firebase Authentication Console.";
        case 'auth/too-many-requests':
          return "Access to this account has been temporarily disabled due to many failed attempts. Try again later or reset password.";
        case 'auth/network-request-failed':
          return "Network error. Please check your internet connection and try again.";
        default:
          return err?.message || "An authentication error occurred. Please try again.";
      }
    }

    // Switch between Sign In and Create Account tabs
    function setAuthMode(mode) {
      authMode = mode;
      clearAuthAlert();
      if (forgotPasswordPanel) forgotPasswordPanel.classList.add('hidden');
      if (emailAuthForm) emailAuthForm.classList.remove('hidden');

      if (mode === 'signup') {
        tabAuthSignUp?.classList.add('bg-white', 'text-charcoal', 'shadow-xs');
        tabAuthSignUp?.classList.remove('hover:text-charcoal');
        tabAuthSignIn?.classList.remove('bg-white', 'text-charcoal', 'shadow-xs');
        tabAuthSignIn?.classList.add('hover:text-charcoal');

        authNameGroup?.classList.remove('hidden');
        passwordHint?.classList.remove('hidden');
        btnForgotPassword?.classList.add('hidden');
        if (btnEmailSubmitLabel) btnEmailSubmitLabel.textContent = "Create Free Account";
      } else {
        tabAuthSignIn?.classList.add('bg-white', 'text-charcoal', 'shadow-xs');
        tabAuthSignIn?.classList.remove('hover:text-charcoal');
        tabAuthSignUp?.classList.remove('bg-white', 'text-charcoal', 'shadow-xs');
        tabAuthSignUp?.classList.add('hover:text-charcoal');

        authNameGroup?.classList.add('hidden');
        passwordHint?.classList.add('hidden');
        btnForgotPassword?.classList.remove('hidden');
        if (btnEmailSubmitLabel) btnEmailSubmitLabel.textContent = "Sign In to Cockpit";
      }
    }

    tabAuthSignIn?.addEventListener('click', () => setAuthMode('signin'));
    tabAuthSignUp?.addEventListener('click', () => setAuthMode('signup'));

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

    // Toggle Show/Hide Password
    btnTogglePassword?.addEventListener('click', () => {
      if (!authPassword) return;
      const isPass = authPassword.type === 'password';
      authPassword.type = isPass ? 'text' : 'password';
      iconEyeShow?.classList.toggle('hidden', isPass);
      iconEyeHide?.classList.toggle('hidden', !isPass);
    });

    // Forgot Password Flow
    btnForgotPassword?.addEventListener('click', () => {
      clearAuthAlert();
      emailAuthForm?.classList.add('hidden');
      forgotPasswordPanel?.classList.remove('hidden');
      if (forgotEmail && authEmail) forgotEmail.value = authEmail.value;
      forgotEmail?.focus();
    });

    btnBackToLogin?.addEventListener('click', () => {
      clearAuthAlert();
      forgotPasswordPanel?.classList.add('hidden');
      emailAuthForm?.classList.remove('hidden');
      authEmail?.focus();
    });

    btnSendReset?.addEventListener('click', async () => {
      const email = forgotEmail?.value.trim();
      if (!email || !email.includes('@')) {
        showAuthAlert("Please enter a valid email address.", "error");
        return;
      }
      btnSendReset.disabled = true;
      btnSendResetLabel.textContent = "Sending...";
      btnSendResetSpinner?.classList.remove('hidden');
      clearAuthAlert();

      try {
        await sendPasswordResetEmail(auth, email);
        showAuthAlert(`Password reset link sent to ${email}. Please check your inbox or spam folder.`, "success");
      } catch (err) {
        showAuthAlert(formatAuthError(err), "error");
      } finally {
        btnSendReset.disabled = false;
        btnSendResetLabel.textContent = "Send Reset Link";
        btnSendResetSpinner?.classList.add('hidden');
      }
    });

    // Email / Password Form Submit Handler
    emailAuthForm?.addEventListener('submit', async (e) => {
      e.preventDefault();
      clearAuthAlert();

      const email = authEmail?.value.trim();
      const password = authPassword?.value;
      const name = authName?.value.trim();

      if (!email || !email.includes('@')) {
        showAuthAlert("Please enter a valid email address.", "error");
        authEmail?.focus();
        return;
      }
      if (!password || password.length < 6) {
        showAuthAlert("Password must be at least 6 characters long.", "error");
        authPassword?.focus();
        return;
      }

      btnEmailSubmit.disabled = true;
      btnEmailSubmitSpinner?.classList.remove('hidden');
      btnEmailSubmitLabel.textContent = authMode === 'signup' ? "Creating Account..." : "Signing In...";

      try {
        if (authMode === 'signup') {
          const cred = await createUserWithEmailAndPassword(auth, email, password);
          if (name) {
            await updateProfile(cred.user, { displayName: name });
          }
          showAuthAlert("Account created successfully! Entering cockpit...", "success");
          // onAuthStateChanged will transition to dashboard
        } else {
          await signInWithEmailAndPassword(auth, email, password);
          // onAuthStateChanged will transition to dashboard
        }
      } catch (err) {
        showAuthAlert(formatAuthError(err), "error");
      } finally {
        btnEmailSubmit.disabled = false;
        btnEmailSubmitSpinner?.classList.add('hidden');
        btnEmailSubmitLabel.textContent = authMode === 'signup' ? "Create Free Account" : "Sign In to Cockpit";
      }
    });

    // ── Google One-Click Auth Handler ─────────────────────────────
    btnGoogleAuth?.addEventListener('click', async () => {
      btnGoogleAuth.disabled = true;
      btnAuthLabel.textContent = "Connecting...";
      trailingArrowIcon?.classList.add('hidden');
      btnAuthSpinner?.classList.remove('hidden');
      clearAuthAlert();

      try {
        await signInWithPopup(auth, provider);
        // onAuthStateChanged will fire automatically with the authenticated user
      } catch (err) {
        showAuthAlert(formatAuthError(err), "error");
      } finally {
        btnGoogleAuth.disabled = false;
        btnAuthLabel.textContent = "Continue with Google";
        trailingArrowIcon?.classList.remove('hidden');
        btnAuthSpinner?.classList.add('hidden');
      }
    });

    // ── Sign Out Handlers ─────────────────────────────────────────
    btnDashSignout?.addEventListener('click', async () => {
      try { await signOut(auth); } catch (e) {}
      exitToAuth();
    });
    btnDashSignoutMobile?.addEventListener('click', async () => {
      try { await signOut(auth); } catch (e) {}
      exitToAuth();
    });"""

new_auth_logic = """    const trailingArrowIcon = document.getElementById('trailing-arrow-icon');

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
    });"""

assert old_auth_logic in content, "Could not find old_auth_logic in index.html"
content = content.replace(old_auth_logic, new_auth_logic, 1)
print("3. Replaced script with clean Google Auth popup logic")

# 4. Update exitToAuth
old_exit = """    function exitToAuth() {
      dashboardView.classList.add('hidden');
      authView.style.display = 'flex';
      if (btnGoogleAuth) {
        btnGoogleAuth.disabled = false;
        if (btnAuthLabel) btnAuthLabel.textContent = "Continue with Google";
        if (trailingArrowIcon) trailingArrowIcon.classList.remove('hidden');
        if (btnAuthSpinner) btnAuthSpinner.classList.add('hidden');
      }
      if (authEmail) authEmail.value = '';
      if (authPassword) authPassword.value = '';
      if (authName) authName.value = '';
      if (forgotEmail) forgotEmail.value = '';
      if (typeof clearAuthAlert === 'function') clearAuthAlert();
      if (typeof setAuthMode === 'function') setAuthMode('signin');
      showToast('Signed out of session.', 'info');
    }"""

new_exit = """    function exitToAuth() {
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
    }"""

assert old_exit in content, "Could not find old_exit in index.html"
content = content.replace(old_exit, new_exit, 1)
print("4. Updated exitToAuth")

# 5. Update onAuthStateChanged to ensure immediate transition
old_observer = """    onAuthStateChanged(auth, async (user) => {
      if (user) {
        currentUser = user;
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
    });"""

new_observer = """    // Immediate state transition listener
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
    });"""

assert old_observer in content, "Could not find old_observer in index.html"
content = content.replace(old_observer, new_observer, 1)
print("5. Updated onAuthStateChanged with immediate dashboard reveal")

# 6. Add id="authContainer" and id="dashboardContainer" aliases to containers
content = content.replace('id="auth-view"', 'id="auth-view" data-container="authContainer"', 1)
content = content.replace('id="dashboard-view"', 'id="dashboard-view" data-container="dashboardContainer"', 1)
content = content.replace('id="auth-card"', 'id="auth-card" data-card="authCard"', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("One-Click Google Authentication successfully restored in index.html!")
