"""
Script to fix Google login immediate transition to backend/dashboard:
1. enterDashboard immediately hides auth-view and reveals dashboard-view with display: flex
2. window.handleGoogleLogin immediately calls enterDashboard(user) and mounts realtime listeners without waiting
3. onAuthStateChanged also calls enterDashboard(user) immediately
4. exitToAuth cleanly reverses view visibility
"""
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update enterDashboard and exitToAuth
old_enter_exit = """    function enterDashboard(userData) {
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
    }"""

new_enter_exit = """    function enterDashboard(userData) {
      currentUser = userData;
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

      // Initialize real-time backend Firestore synchronization
      initDataSync(userData);

      // Instant View Transition: Hide Auth View, Reveal Dashboard Cockpit
      const authContainer = document.getElementById("auth-view") || document.getElementById("authContainer") || authView;
      const dashboardContainer = document.getElementById("dashboard-view") || document.getElementById("dashboardContainer") || dashboardView;

      if (authContainer) {
        authContainer.classList.add('hidden');
        authContainer.style.display = 'none';
      }
      if (dashboardContainer) {
        dashboardContainer.classList.remove('hidden');
        dashboardContainer.style.display = 'flex';
      }

      switchTab('home');
      showToast(`Welcome back, ${name}. Cockpit online.`, 'success');
    }

    function exitToAuth() {
      const authContainer = document.getElementById("auth-view") || document.getElementById("authContainer") || authView;
      const dashboardContainer = document.getElementById("dashboard-view") || document.getElementById("dashboardContainer") || dashboardView;

      if (dashboardContainer) {
        dashboardContainer.classList.add('hidden');
        dashboardContainer.style.display = 'none';
      }
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

assert old_enter_exit in content, "Could not find old_enter_exit in index.html"
content = content.replace(old_enter_exit, new_enter_exit, 1)
print("1. Updated enterDashboard and exitToAuth")

# 2. Update window.handleGoogleLogin to immediately transition to backend
old_login_handler = """    // ── Google One-Click Sign-In Handler ──────────────────────────
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
          userMsg = "Domain not authorized in Firebase Console.";
        }
        showAuthError(userMsg);
      } finally {
        if (btn) btn.disabled = false;
        if (label) label.textContent = "Continue with Google";
        if (arrow) arrow.classList.remove("hidden");
        if (spinner) spinner.classList.add("hidden");
      }
    };"""

new_login_handler = """    // ── Google One-Click Sign-In Handler ──────────────────────────
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

        // Immediate Transition to backend / dashboard
        currentUser = user;
        enterDashboard(user);
        if (typeof window.__sgInit === 'function') window.__sgInit(user);

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
          userMsg = "Domain not authorized in Firebase Console.";
        }
        showAuthError(userMsg);
      } finally {
        if (btn) btn.disabled = false;
        if (label) label.textContent = "Continue with Google";
        if (arrow) arrow.classList.remove("hidden");
        if (spinner) spinner.classList.add("hidden");
      }
    };"""

assert old_login_handler in content, "Could not find old_login_handler in index.html"
content = content.replace(old_login_handler, new_login_handler, 1)
print("2. Updated window.handleGoogleLogin to immediately enterDashboard on success")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved index.html successfully!")
