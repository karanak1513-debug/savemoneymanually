"""
Comprehensive Fix Script:
1. Injects fs-sync-badge HTML
2. Injects Saving Guide & Admin Desk HTML (sg-launcher, sg-window, sg-admin-overlay)
3. Adds Instant Demo Mode button & listener to Auth Card
"""
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add btn-demo-mode to Auth Card
demo_btn_target = """      <!-- Auth Error / Success Feedback Banner -->
      <div id="auth-feedback" class="text-xs font-medium hidden mt-3 p-2.5 rounded-xl flex items-start gap-2 text-left"></div>

      <!-- Footnote -->"""

demo_btn_replacement = """      <!-- Auth Error / Success Feedback Banner -->
      <div id="auth-feedback" class="text-xs font-medium hidden mt-3 p-2.5 rounded-xl flex items-start gap-2 text-left"></div>

      <!-- Instant Demo Mode Access -->
      <div class="mt-4 pt-3 border-t border-slate-100/90">
        <button id="btn-demo-mode" type="button" class="w-full py-2.5 px-3 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200/80 text-xs font-semibold text-slate-600 hover:text-charcoal transition-all flex items-center justify-center gap-1.5 cursor-pointer shadow-xs">
          <span>⚡</span>
          <span>Explore Demo Cockpit (Offline Preview)</span>
        </button>
      </div>

      <!-- Footnote -->"""

if demo_btn_target in content:
    content = content.replace(demo_btn_target, demo_btn_replacement, 1)
    print("Injected btn-demo-mode to Auth Card")

# 2. Add btn-demo-mode event listener in script
old_auth_listeners = """    tabAuthSignIn?.addEventListener('click', () => setAuthMode('signin'));
    tabAuthSignUp?.addEventListener('click', () => setAuthMode('signup'));"""

new_auth_listeners = """    tabAuthSignIn?.addEventListener('click', () => setAuthMode('signin'));
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
    });"""

if old_auth_listeners in content:
    content = content.replace(old_auth_listeners, new_auth_listeners, 1)
    print("Injected btn-demo-mode event listener in JS")

# 3. Inject fs-sync-badge and Saving Guide HTML before </body>
OVERLAYS_HTML = """
  <!-- ================================================================ -->
  <!-- ░░  FIRESTORE REALTIME SYNC STATUS BADGE  ░░                    -->
  <!-- ================================================================ -->
  <div id="fs-sync-badge" class="connecting" role="status" aria-live="polite">
    <span id="fs-sync-dot"></span>
    <span id="fs-sync-label">Connecting…</span>
  </div>

  <!-- ================================================================ -->
  <!-- ░░  SAVING GUIDE — HYBRID BOT & LIVE ADMIN DESK HTML  ░░        -->
  <!-- ================================================================ -->

  <!-- Floating Launcher -->
  <button id="sg-launcher" title="Saving Guide — Support Chat" aria-label="Open Saving Guide chat">
    <span id="sg-unread-badge" class="hidden" aria-live="polite">0</span>
    <span id="sg-launcher-label">Saving Guide</span>
    <!-- Shield/Bot Icon -->
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      <path d="M9 12l2 2 4-4" stroke-width="2.2"/>
    </svg>
  </button>

  <!-- Chat Window -->
  <div id="sg-window" role="dialog" aria-label="Saving Guide Support Chat" aria-modal="false">
    <!-- Header -->
    <div id="sg-header">
      <div class="flex items-center gap-2.5">
        <div id="sg-avatar">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
            <path d="M9 12l2 2 4-4"/>
          </svg>
        </div>
        <div id="sg-header-info">
          <div id="sg-agent-name">Saving Guide</div>
          <div id="sg-status-row">
            <span id="sg-status-dot"></span>
            <span id="sg-status-label">Online · Auto-reply active</span>
          </div>
        </div>
      </div>
      <div id="sg-header-actions">
        <button class="sg-header-btn" id="sg-minimize-btn" title="Minimize" aria-label="Minimize chat">
          <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.3" viewBox="0 0 24 24"><path stroke-linecap="round" d="M5 12h14"/></svg>
        </button>
        <button class="sg-header-btn" id="sg-close-btn" title="Close" aria-label="Close chat">
          <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
    </div>

    <!-- Messages Stream -->
    <div id="sg-messages" role="log" aria-live="polite" aria-label="Chat messages">
      <!-- Typing Indicator (hidden by default) -->
      <div id="sg-typing-indicator">
        <span class="sg-typing-label">Saving Guide is typing…</span>
        <div class="sg-typing-bubble">
          <span></span><span></span><span></span>
        </div>
      </div>
    </div>

    <!-- Input -->
    <div id="sg-input-area">
      <input id="sg-text-input" type="text" placeholder="Ask anything about saving…" maxlength="600" autocomplete="off" aria-label="Type your message" />
      <button id="sg-send-btn" aria-label="Send message" disabled>
        <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
        </svg>
      </button>
    </div>
  </div>

  <!-- ================================================================ -->
  <!-- ░░  ADMIN LIVE DESK OVERLAY  ░░                                  -->
  <!-- ================================================================ -->
  <div id="sg-admin-overlay" role="dialog" aria-label="Saving Guide Admin Desk" aria-modal="true">
    <div id="sg-admin-desk">

      <!-- Admin Top Bar -->
      <div id="sg-admin-topbar">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0" style="background:linear-gradient(135deg,#2563EB,#1D4ED8);">
            <svg width="14" height="14" fill="none" stroke="#fff" stroke-width="2.3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4" stroke-width="2.5"/></svg>
          </div>
          <div>
            <div class="text-white font-extrabold text-sm" style="font-family:'Plus Jakarta Sans',sans-serif;letter-spacing:-0.02em;">Saving Guide — Admin Live Desk</div>
            <div class="text-slate-500 font-mono font-semibold" style="font-size:0.62rem;letter-spacing:0.04em;">SAVEMONEYMANUALLY · OPERATOR VIEW · REAL-TIME</div>
          </div>
        </div>
        <div class="flex items-center gap-3">
          <span class="flex items-center gap-1.5 font-mono font-bold text-emerald-400" style="font-size:0.65rem;">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>LIVE
          </span>
          <button id="sg-admin-close" class="sg-header-btn" title="Close Admin Desk" aria-label="Close admin desk">
            <svg width="16" height="16" fill="none" stroke="#94A3B8" stroke-width="2.3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>

      <!-- Body: Split -->
      <div id="sg-admin-body">

        <!-- Left: Thread List -->
        <div id="sg-threads-panel">
          <div id="sg-threads-header">
            <div class="text-slate-400 font-mono font-bold uppercase" style="font-size:0.6rem;letter-spacing:0.06em;">Active Sessions</div>
            <div id="sg-thread-count" class="font-bold text-charcoal mt-0.5" style="font-size:0.75rem;">0 threads</div>
          </div>
          <div id="sg-threads-list">
            <div id="sg-threads-empty" class="flex flex-col items-center justify-center gap-2 py-12 px-4 text-center">
              <svg class="w-8 h-8" style="color:#E2E8F0;" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
              <div class="text-slate-300 font-medium" style="font-size:0.72rem;">No active threads yet</div>
            </div>
          </div>
        </div>

        <!-- Right: Live Terminal -->
        <div id="sg-admin-chat-panel">
          <div id="sg-admin-toolbar">
            <div id="sg-admin-sel-user" class="flex-1 text-slate-400 font-medium" style="font-size:0.75rem;">← Select a session</div>
            <button id="sg-admin-takeover" type="button" class="hidden text-xs font-bold px-3 py-1.5 rounded-xl transition-all" style="background:#EFF6FF;color:#2563EB;border:1.5px solid #BFDBFE;" title="Take Over from Saving Guide">⚡ Take Over</button>
            <button id="sg-admin-handback" type="button" class="hidden text-xs font-bold px-3 py-1.5 rounded-xl transition-all" style="background:#F1F5F9;color:#64748B;border:1.5px solid #E2E8F0;" title="Hand Back to Saving Guide">🤖 Hand to Bot</button>
            <button id="sg-admin-resolve" type="button" class="hidden text-xs font-bold px-3 py-1.5 rounded-xl transition-all" style="background:#ECFDF5;color:#059669;border:1.5px solid #A7F3D0;" title="Mark Resolved">✓ Resolve</button>
          </div>
          <div id="sg-admin-messages">
            <div class="flex flex-col items-center justify-center gap-3 h-full text-center" id="sg-admin-placeholder">
              <svg class="w-12 h-12" style="color:#F1F5F9;" fill="none" stroke="currentColor" stroke-width="1.3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
              <div class="text-slate-300 font-medium" style="font-size:0.78rem;">Select a chat thread to monitor live</div>
            </div>
          </div>
          <div id="sg-admin-reply-bar">
            <input id="sg-admin-input" type="text" placeholder="Type operator message… (Enter to send)" disabled maxlength="1200" autocomplete="off" />
            <button id="sg-admin-send" disabled>Send</button>
          </div>
        </div>
      </div>
    </div>
  </div>
"""

body_end = '\n</body>'
if body_end in content and '<button id="sg-launcher"' not in content:
    content = content.replace(body_end, OVERLAYS_HTML + body_end, 1)
    print("Injected OVERLAYS_HTML before </body>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html fully updated!")
