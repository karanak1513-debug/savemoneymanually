# -*- coding: utf-8 -*-
"""
Injects two-way live support & bot engine into index.html:
1. Chatbot CSS
2. Chatbot HTML (floating widget + admin console modal)
3. Chatbot JS (rule-based bot, Firestore real-time messaging, admin takeover)
4. Updates Firestore security rules
"""

# ─── UPDATE FIRESTORE RULES ───────────────────────────────────────
new_rules = """rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    function isAuthenticated() {
      return request.auth != null;
    }
    function isAdmin() {
      return isAuthenticated() && request.auth.token.email == 'karanak1513@gmail.com';
    }

    match /users/{userId} {
      allow read, write: if isAuthenticated() && request.auth.uid == userId;
      match /{allSubcollections=**} {
        allow read, write: if isAuthenticated() && request.auth.uid == userId;
      }
    }

    match /support_threads/{threadId} {
      allow read, write: if isAuthenticated() && (request.auth.uid == threadId || isAdmin());
      match /messages/{messageId} {
        allow read, write: if isAuthenticated() && (request.auth.uid == threadId || isAdmin());
      }
    }
  }
}
"""

with open('firestore.rules', 'w', encoding='utf-8') as f:
    f.write(new_rules)
print("Updated firestore.rules with support_threads rules.")

# ─── READ index.html ──────────────────────────────────────────────
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ─── 1. INJECT CHATBOT CSS (before </style>) ──────────────────────
chatbot_css = """
    /* ========================================================== */
    /* CHATBOT WIDGET & ADMIN CONSOLE STYLES                      */
    /* ========================================================== */

    /* Floating Launcher */
    #chatbot-launcher {
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      z-index: 9000;
      width: 3.5rem;
      height: 3.5rem;
      border-radius: 50%;
      background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
      box-shadow: 0 8px 32px rgba(37, 99, 235, 0.45), 0 2px 8px rgba(37, 99, 235, 0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.2s ease;
      border: none;
      outline: none;
    }
    #chatbot-launcher:hover {
      transform: scale(1.1);
      box-shadow: 0 12px 40px rgba(37, 99, 235, 0.55), 0 4px 12px rgba(37, 99, 235, 0.4);
    }
    #chatbot-unread-badge {
      position: absolute;
      top: -3px;
      right: -3px;
      min-width: 1.1rem;
      height: 1.1rem;
      background: #E11D48;
      color: #fff;
      font-size: 0.6rem;
      font-weight: 800;
      border-radius: 9999px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 3px;
      border: 2px solid #fff;
      box-shadow: 0 2px 6px rgba(225, 29, 72, 0.5);
      pointer-events: none;
      animation: chatbadgepulse 1.8s infinite;
    }
    @keyframes chatbadgepulse {
      0%, 100% { transform: scale(1); }
      50% { transform: scale(1.15); }
    }

    /* Chat Window */
    #chatbot-window {
      position: fixed;
      bottom: 6.5rem;
      right: 1.5rem;
      width: 22rem;
      max-width: calc(100vw - 2rem);
      height: 480px;
      background: #FFFFFF;
      border-radius: 1.5rem;
      border: 1px solid rgba(226, 232, 240, 0.9);
      box-shadow: 0 32px 80px rgba(15, 23, 42, 0.14), 0 8px 24px rgba(15, 23, 42, 0.06);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      z-index: 8999;
      transform: scale(0.92) translateY(12px);
      opacity: 0;
      pointer-events: none;
      transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    #chatbot-window.open {
      transform: scale(1) translateY(0);
      opacity: 1;
      pointer-events: all;
    }

    /* Chat Header */
    #chatbot-header {
      background: linear-gradient(135deg, #0B0F19 0%, #1E293B 100%);
      padding: 0.875rem 1rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }

    /* Messages Area */
    #chatbot-messages {
      flex: 1;
      overflow-y: auto;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.625rem;
      scroll-behavior: smooth;
    }
    #chatbot-messages::-webkit-scrollbar { width: 4px; }
    #chatbot-messages::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 99px; }

    /* Message Bubbles */
    .chat-msg {
      max-width: 80%;
      padding: 0.6rem 0.875rem;
      font-size: 0.8rem;
      line-height: 1.45;
      font-family: 'Inter', sans-serif;
      border-radius: 1.1rem;
      animation: chatfadein 0.22s ease both;
    }
    @keyframes chatfadein {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .chat-msg-user {
      background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
      color: #fff;
      border-bottom-right-radius: 4px;
      align-self: flex-end;
    }
    .chat-msg-bot {
      background: #F1F5F9;
      color: #0F172A;
      border-bottom-left-radius: 4px;
      align-self: flex-start;
    }
    .chat-msg-admin {
      background: linear-gradient(135deg, #0B0F19 0%, #1E293B 100%);
      color: #fff;
      border-bottom-left-radius: 4px;
      align-self: flex-start;
    }

    /* Quick Action Pills */
    .chat-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 0.375rem;
      align-self: flex-start;
      max-width: 90%;
      margin-top: -0.25rem;
    }
    .chat-pill {
      background: #EFF6FF;
      color: #2563EB;
      border: 1px solid #BFDBFE;
      border-radius: 999px;
      padding: 0.3rem 0.7rem;
      font-size: 0.72rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: 'Inter', sans-serif;
    }
    .chat-pill:hover {
      background: #2563EB;
      color: #fff;
      border-color: #2563EB;
    }

    /* Chat Input */
    #chatbot-input-area {
      border-top: 1px solid #F1F5F9;
      padding: 0.75rem;
      display: flex;
      gap: 0.5rem;
      flex-shrink: 0;
      background: #FAFAFA;
    }
    #chatbot-text-input {
      flex: 1;
      background: #FFFFFF;
      border: 1.5px solid #E2E8F0;
      border-radius: 12px;
      padding: 0.5rem 0.75rem;
      font-size: 0.8rem;
      font-family: 'Inter', sans-serif;
      color: #0F172A;
      outline: none;
      transition: border-color 0.15s ease;
    }
    #chatbot-text-input:focus { border-color: #2563EB; }
    #chatbot-text-input::placeholder { color: #94A3B8; }
    #chatbot-send-btn {
      width: 2.25rem;
      height: 2.25rem;
      border-radius: 10px;
      background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
      color: #fff;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
      flex-shrink: 0;
    }
    #chatbot-send-btn:hover { transform: scale(1.06); }
    #chatbot-send-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

    /* Typing indicator */
    .chat-typing {
      display: flex;
      gap: 4px;
      padding: 0.6rem 0.875rem;
      background: #F1F5F9;
      border-radius: 1.1rem;
      border-bottom-left-radius: 4px;
      align-self: flex-start;
      width: fit-content;
    }
    .chat-typing span {
      width: 7px;
      height: 7px;
      background: #94A3B8;
      border-radius: 50%;
      animation: typingdot 1.2s infinite;
    }
    .chat-typing span:nth-child(2) { animation-delay: 0.15s; }
    .chat-typing span:nth-child(3) { animation-delay: 0.30s; }
    @keyframes typingdot {
      0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
      30% { transform: translateY(-5px); opacity: 1; }
    }

    /* Admin Console Overlay */
    #admin-console-overlay {
      position: fixed;
      inset: 0;
      background: rgba(11, 15, 25, 0.65);
      backdrop-filter: blur(8px);
      z-index: 10000;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.2s ease;
    }
    #admin-console-overlay.open {
      opacity: 1;
      pointer-events: all;
    }
    #admin-console {
      width: 100%;
      max-width: 1100px;
      height: min(85vh, 720px);
      background: #FFFFFF;
      border-radius: 1.5rem;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 40px 120px rgba(11, 15, 25, 0.30);
      border: 1px solid rgba(226, 232, 240, 0.8);
    }

    /* Admin Header Bar */
    #admin-header {
      background: linear-gradient(135deg, #0B0F19 0%, #1E293B 100%);
      padding: 1rem 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }

    /* Admin Split */
    #admin-body {
      flex: 1;
      display: flex;
      overflow: hidden;
    }

    /* Left Threads Panel */
    #admin-threads-panel {
      width: 35%;
      border-right: 1px solid #F1F5F9;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    #admin-threads-list {
      flex: 1;
      overflow-y: auto;
    }
    #admin-threads-list::-webkit-scrollbar { width: 4px; }
    #admin-threads-list::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 99px; }

    .admin-thread-item {
      padding: 0.875rem 1rem;
      cursor: pointer;
      border-bottom: 1px solid #F8FAFC;
      transition: background 0.15s ease;
      display: flex;
      align-items: flex-start;
      gap: 0.625rem;
    }
    .admin-thread-item:hover { background: #F8FAFC; }
    .admin-thread-item.active { background: #EFF6FF; border-left: 3px solid #2563EB; }

    /* Right Chat Panel */
    #admin-chat-panel {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    #admin-chat-toolbar {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid #F1F5F9;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-shrink: 0;
      background: #FAFAFA;
    }
    #admin-chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    #admin-chat-messages::-webkit-scrollbar { width: 4px; }
    #admin-chat-messages::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 99px; }
    #admin-reply-area {
      border-top: 1px solid #F1F5F9;
      padding: 0.75rem 1rem;
      display: flex;
      gap: 0.5rem;
      flex-shrink: 0;
      background: #FAFAFA;
    }
    #admin-reply-input {
      flex: 1;
      background: #FFFFFF;
      border: 1.5px solid #E2E8F0;
      border-radius: 12px;
      padding: 0.6rem 0.875rem;
      font-size: 0.82rem;
      font-family: 'Inter', sans-serif;
      color: #0F172A;
      outline: none;
      transition: border-color 0.15s ease;
    }
    #admin-reply-input:focus { border-color: #2563EB; }
    #admin-reply-input::placeholder { color: #94A3B8; }
    #admin-reply-send {
      padding: 0.6rem 1.1rem;
      background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
      color: #fff;
      border: none;
      border-radius: 12px;
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: 'Inter', sans-serif;
    }
    #admin-reply-send:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35); }

    /* Status Badges */
    .status-badge {
      font-size: 0.62rem;
      font-weight: 700;
      padding: 0.18rem 0.55rem;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      font-family: 'Space Grotesk', monospace;
    }
    .status-bot { background: #F1F5F9; color: #64748B; }
    .status-requested { background: #FFF1F2; color: #E11D48; animation: requestedpulse 1.4s infinite; }
    .status-connected { background: #EFF6FF; color: #2563EB; }
    .status-resolved { background: #ECFDF5; color: #10B981; }
    @keyframes requestedpulse {
      0%, 100% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.4); }
      50% { box-shadow: 0 0 0 4px rgba(225, 29, 72, 0); }
    }
"""

css_injection_point = "    /* ── TOAST MESSAGES"
if css_injection_point in html:
    html = html.replace(css_injection_point, chatbot_css + "\n    /* ── TOAST MESSAGES", 1)
    print("Injected chatbot CSS before toast section.")

# ─── 2. INJECT CHATBOT & ADMIN HTML (before </body>) ──────────────
chatbot_html = """
  <!-- ============================================================ -->
  <!-- FLOATING CHATBOT WIDGET & ADMIN CONSOLE                     -->
  <!-- ============================================================ -->

  <!-- Floating Launcher Button -->
  <button id="chatbot-launcher" title="Support Chat" aria-label="Open support chat">
    <span id="chatbot-unread-badge" class="hidden">0</span>
    <!-- Chat Bubble Icon -->
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
    </svg>
  </button>

  <!-- Chatbot Window -->
  <div id="chatbot-window" role="dialog" aria-label="Support Chat">
    <!-- Header -->
    <div id="chatbot-header">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center flex-shrink-0">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
        </div>
        <div>
          <div id="chat-agent-name" class="text-white text-xs font-bold font-sans">AI Assistant</div>
          <div class="flex items-center gap-1.5">
            <span id="chat-status-dot" class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span id="chat-status-label" class="text-slate-400 text-[10px] font-mono">Online — Auto-reply active</span>
          </div>
        </div>
      </div>
      <button id="chatbot-close" class="text-slate-400 hover:text-white transition-colors p-1 rounded-lg" aria-label="Close chat">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>
    </div>

    <!-- Messages Stream -->
    <div id="chatbot-messages"></div>

    <!-- Input Area -->
    <div id="chatbot-input-area">
      <input id="chatbot-text-input" type="text" placeholder="Type your message..." maxlength="500" autocomplete="off" />
      <button id="chatbot-send-btn" aria-label="Send message">
        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/></svg>
      </button>
    </div>
  </div>

  <!-- ── ADMIN LIVE CONSOLE OVERLAY ── -->
  <div id="admin-console-overlay" role="dialog" aria-label="Admin Live Support Console" aria-modal="true">
    <div id="admin-console">
      <!-- Admin Header Bar -->
      <div id="admin-header">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-cobalt to-blue-700 flex items-center justify-center">
            <svg width="15" height="15" fill="none" stroke="#fff" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </div>
          <div>
            <div class="text-white text-sm font-extrabold font-sans tracking-tight">Admin Live Support Console</div>
            <div class="text-slate-400 text-[10px] font-mono">SaveMoneyManually · Operator View · Real-time</div>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span id="admin-live-indicator" class="flex items-center gap-1.5 text-[10px] text-emerald-400 font-mono font-bold">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>LIVE
          </span>
          <button id="admin-console-close" class="text-slate-400 hover:text-white transition-colors p-1.5 rounded-lg ml-2" aria-label="Close admin console">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </div>

      <!-- Admin Split Layout -->
      <div id="admin-body">
        <!-- Left: Thread List -->
        <div id="admin-threads-panel">
          <div class="px-3 py-2.5 border-b border-slate-100 bg-slate-50">
            <div class="text-[10px] font-mono font-bold text-slate-400 uppercase tracking-wider">Active Sessions</div>
            <div id="admin-thread-count" class="text-xs font-bold text-charcoal mt-0.5">0 open threads</div>
          </div>
          <div id="admin-threads-list">
            <div class="flex flex-col items-center justify-center gap-2 py-10 px-4 text-center">
              <svg class="w-8 h-8 text-slate-200" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
              <div class="text-[11px] text-slate-400 font-medium">No active support threads</div>
            </div>
          </div>
        </div>

        <!-- Right: Live Chat Terminal -->
        <div id="admin-chat-panel">
          <div id="admin-chat-toolbar">
            <div id="admin-selected-user" class="text-xs font-semibold text-slate-500 flex-1">Select a thread from the left →</div>
            <button id="admin-takeover-btn" class="hidden text-[11px] font-bold px-3 py-1.5 rounded-lg bg-cobalt text-white cursor-pointer transition-all hover:bg-blue-700" type="button">⚡ Take Over Chat</button>
            <button id="admin-resolve-btn" class="hidden text-[11px] font-bold px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-700 border border-emerald-200 cursor-pointer transition-all hover:bg-emerald-100" type="button">✓ Mark Resolved</button>
          </div>
          <div id="admin-chat-messages">
            <div class="flex flex-col items-center justify-center gap-2 h-full text-center">
              <svg class="w-10 h-10 text-slate-100" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>
              <div class="text-xs text-slate-300 font-medium">Select a chat thread to start monitoring</div>
            </div>
          </div>
          <div id="admin-reply-area">
            <input id="admin-reply-input" type="text" placeholder="Type operator reply..." disabled maxlength="1000" autocomplete="off" />
            <button id="admin-reply-send" disabled>Send</button>
          </div>
        </div>
      </div>
    </div>
  </div>
"""

if '</body>' in html:
    html = html.replace('</body>', chatbot_html + '\n</body>', 1)
    print("Injected chatbot and admin console HTML before </body>.")

# ─── 3. INJECT CHATBOT JS (before </script> closing the module) ───
chatbot_js = """
    // ============================================================
    // TWO-WAY LIVE SUPPORT & BOT ENGINE
    // ============================================================
    const ADMIN_EMAIL = 'karanak1513@gmail.com';

    let chatThreadId = null;
    let unsubChatMessages = null;
    let unsubAdminThreads = null;
    let unsubAdminMessages = null;
    let activeAdminThreadId = null;
    let chatWindowOpen = false;
    let userUnreadCount = 0;
    let isBotSending = false;

    // DOM refs
    const chatLauncher = document.getElementById('chatbot-launcher');
    const chatWindow = document.getElementById('chatbot-window');
    const chatClose = document.getElementById('chatbot-close');
    const chatMessages = document.getElementById('chatbot-messages');
    const chatInput = document.getElementById('chatbot-text-input');
    const chatSendBtn = document.getElementById('chatbot-send-btn');
    const chatUnreadBadge = document.getElementById('chatbot-unread-badge');
    const chatAgentName = document.getElementById('chat-agent-name');
    const chatStatusDot = document.getElementById('chat-status-dot');
    const chatStatusLabel = document.getElementById('chat-status-label');
    const adminConsoleOverlay = document.getElementById('admin-console-overlay');
    const adminConsoleClose = document.getElementById('admin-console-close');
    const adminThreadsList = document.getElementById('admin-threads-list');
    const adminThreadCount = document.getElementById('admin-thread-count');
    const adminSelectedUser = document.getElementById('admin-selected-user');
    const adminTakeoverBtn = document.getElementById('admin-takeover-btn');
    const adminResolveBtn = document.getElementById('admin-resolve-btn');
    const adminChatMessages = document.getElementById('admin-chat-messages');
    const adminReplyInput = document.getElementById('admin-reply-input');
    const adminReplySend = document.getElementById('admin-reply-send');

    // ── BOT KNOWLEDGE BASE (Rule-Based Intent Matching) ──────────
    const BOT_RULES = [
      {
        patterns: ['how to save', 'deposit', 'add saved', 'add money', 'log deposit', 'add funds', 'savings'],
        reply: "Tap <strong>\"+ Add Saved\"</strong> on your dashboard, input your manual cash or UPI saving, and confirm. Vault totals update automatically in real time. ⚡"
      },
      {
        patterns: ['real money', 'bank', 'security', 'safe', 'collect', 'collect money', 'link bank', 'account'],
        reply: "🔒 <strong>No real money is collected.</strong> SaveMoneyManually does not connect to bank accounts or hold funds. This platform functions strictly as a <em>discipline ledger</em>. Your savings stay in your own cash or bank account."
      },
      {
        patterns: ['set target', 'goal', 'create vault', 'new vault', 'target', 'deadline', 'cadence'],
        reply: "Navigate to <strong>\"Goals\"</strong> from the lower menu → tap <strong>\"+ Create Target Vault\"</strong> → choose your deadline → set cadence to Daily, Monthly, or Yearly. The app auto-calculates your required daily savings quota. 🎯"
      },
      {
        patterns: ['withdraw', 'withdrawal', 'take out', 'remove money'],
        reply: "Tap <strong>\"- Record Withdrawal\"</strong> on the Home screen, choose your vault, enter the amount, and add a reason. The withdrawal is logged and your vault balance updates instantly."
      },
      {
        patterns: ['ledger', 'history', 'records', 'transactions'],
        reply: "Open the <strong>Ledger</strong> tab from the bottom navigation. You can view, edit, or delete any historical entry. All changes reflect instantly."
      },
      {
        patterns: ['calendar', 'streak', 'discipline'],
        reply: "The <strong>Calendar</strong> tab shows your saving streak. Days where you logged deposits are highlighted in Electric Cobalt Blue. Build your streak — consistency is the habit."
      },
      {
        patterns: ['contact', 'agent', 'human', 'help', 'support', 'speak', 'talk', 'operator', 'connect agent'],
        reply: "Connecting you to a live agent. Please hold a moment... 🔗",
        action: 'REQUEST_AGENT'
      },
      {
        patterns: ['hello', 'hi', 'hey', 'hola', 'namaste', 'start'],
        reply: "👋 Hi there! I'm the SaveMoneyManually AI Assistant. I can help you with deposits, goals, withdrawals, security questions, and more. What would you like help with?"
      },
      {
        patterns: ['firebase', 'error', 'bug', 'issue', 'not working', 'problem', 'broken'],
        reply: "Sorry to hear you're experiencing an issue. Please try refreshing the page first. If the problem persists, I'll connect you to a live agent.",
        action: 'SUGGEST_AGENT'
      }
    ];

    const DEFAULT_PILLS = [
      { label: '💰 How to save?', text: 'How do I add saved money?' },
      { label: '🔒 Is it secure?', text: 'Is real money collected?' },
      { label: '🎯 Set a target', text: 'How to set a savings target?' },
      { label: '🤝 Speak with agent', text: 'Connect to agent' }
    ];

    function matchBotRule(input) {
      const lower = input.toLowerCase().trim();
      for (const rule of BOT_RULES) {
        if (rule.patterns.some(p => lower.includes(p))) return rule;
      }
      return null;
    }

    // ── CHAT RENDERING ────────────────────────────────────────────
    function renderChatMessage(sender, text, senderName) {
      if (!chatMessages) return;
      const div = document.createElement('div');
      const isUser = sender === 'USER';
      const isAdmin = sender === 'ADMIN';
      div.className = 'chat-msg ' + (isUser ? 'chat-msg-user' : isAdmin ? 'chat-msg-admin' : 'chat-msg-bot');
      if (isAdmin) {
        div.innerHTML = '<div class="flex items-center gap-1 mb-0.5"><span class="text-blue-300 text-[9px] font-bold uppercase tracking-widest">● Official Support</span></div>' + text;
      } else {
        div.innerHTML = text;
      }
      chatMessages.appendChild(div);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function renderChatPills(pills) {
      if (!chatMessages) return;
      const container = document.createElement('div');
      container.className = 'chat-pills';
      pills.forEach(p => {
        const btn = document.createElement('button');
        btn.className = 'chat-pill';
        btn.textContent = p.label;
        btn.type = 'button';
        btn.addEventListener('click', () => {
          container.remove();
          sendUserMessage(p.text);
        });
        container.appendChild(btn);
      });
      chatMessages.appendChild(container);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTypingIndicator() {
      const div = document.createElement('div');
      div.id = 'chat-typing';
      div.className = 'chat-typing';
      div.innerHTML = '<span></span><span></span><span></span>';
      chatMessages?.appendChild(div);
      chatMessages && (chatMessages.scrollTop = chatMessages.scrollHeight);
    }
    function removeTypingIndicator() {
      document.getElementById('chat-typing')?.remove();
    }

    // ── FIRESTORE CHAT ─────────────────────────────────────────────
    async function ensureChatThread(user) {
      if (!db || !user) return;
      chatThreadId = user.uid;
      const threadRef = doc(db, 'support_threads', chatThreadId);
      const threadSnap = await getDoc(threadRef);
      if (!threadSnap.exists()) {
        await setDoc(threadRef, {
          userName: user.displayName || user.email?.split('@')[0] || 'User',
          userEmail: user.email || '',
          userPhoto: user.photoURL || '',
          status: 'BOT_ACTIVE',
          lastMessage: '',
          lastUpdated: serverTimestamp(),
          unreadAdminCount: 0,
          unreadUserCount: 0
        });
      }
      // Subscribe to messages in real time
      if (unsubChatMessages) unsubChatMessages();
      const msgsRef = collection(db, 'support_threads', chatThreadId, 'messages');
      const msgsQuery = query(msgsRef, orderBy('timestamp', 'asc'));
      unsubChatMessages = onSnapshot(msgsQuery, (snap) => {
        if (!chatMessages) return;
        chatMessages.innerHTML = '';
        if (snap.empty) {
          // Welcome bot message on first open
          renderChatMessage('BOT', "👋 Hi! I'm your SaveMoneyManually AI Assistant. How can I help you today?");
          renderChatPills(DEFAULT_PILLS);
          return;
        }
        snap.forEach(docSnap => {
          const d = docSnap.data();
          renderChatMessage(d.sender, d.text, d.senderName);
        });
        // Update header based on thread status
        updateChatHeader();
      }, (err) => console.error("Chat messages snapshot error:", err));

      // Listen for thread status changes
      onSnapshot(threadRef, (snap) => {
        if (snap.exists()) {
          updateChatHeaderFromStatus(snap.data().status, snap.data().unreadUserCount);
        }
      });
    }

    async function sendChatMessageToFirestore(sender, text, senderName) {
      if (!db || !chatThreadId) return;
      const msgsRef = collection(db, 'support_threads', chatThreadId, 'messages');
      await addDoc(msgsRef, {
        sender,
        senderName: senderName || sender,
        text,
        timestamp: serverTimestamp()
      });
      const threadRef = doc(db, 'support_threads', chatThreadId);
      await updateDoc(threadRef, {
        lastMessage: text.replace(/<[^>]*>/g, '').substring(0, 80),
        lastUpdated: serverTimestamp(),
        ...(sender === 'USER' ? { unreadAdminCount: increment(1) } : {})
      });
    }

    function updateChatHeaderFromStatus(status, unreadCount) {
      if (status === 'AGENT_CONNECTED') {
        chatAgentName && (chatAgentName.textContent = 'Live Agent Active');
        chatStatusDot && (chatStatusDot.className = 'w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse');
        chatStatusLabel && (chatStatusLabel.textContent = 'Connected to support agent');
      } else if (status === 'AGENT_REQUESTED') {
        chatAgentName && (chatAgentName.textContent = 'Connecting to Agent...');
        chatStatusDot && (chatStatusDot.className = 'w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse');
        chatStatusLabel && (chatStatusLabel.textContent = 'Agent will join shortly');
      } else if (status === 'RESOLVED') {
        chatAgentName && (chatAgentName.textContent = 'Support Resolved');
        chatStatusDot && (chatStatusDot.className = 'w-1.5 h-1.5 rounded-full bg-emerald-400');
        chatStatusLabel && (chatStatusLabel.textContent = 'Conversation closed ✓');
      } else {
        chatAgentName && (chatAgentName.textContent = 'AI Assistant');
        chatStatusDot && (chatStatusDot.className = 'w-1.5 h-1.5 rounded-full bg-emerald-400');
        chatStatusLabel && (chatStatusLabel.textContent = 'Online — Auto-reply active');
      }
      if (unreadCount > 0 && !chatWindowOpen) {
        userUnreadCount = unreadCount;
        chatUnreadBadge && (chatUnreadBadge.textContent = unreadCount);
        chatUnreadBadge?.classList.remove('hidden');
      }
    }
    function updateChatHeader() {}

    async function sendUserMessage(text) {
      if (!text || !text.trim() || !currentUser) return;
      text = text.trim();

      renderChatMessage('USER', text);

      if (db && chatThreadId) {
        await sendChatMessageToFirestore('USER', text, currentUser.displayName || 'You');
      }

      // Check thread status first
      if (db && chatThreadId) {
        const threadSnap = await getDoc(doc(db, 'support_threads', chatThreadId));
        const status = threadSnap.data()?.status;
        if (status === 'AGENT_CONNECTED' || status === 'AGENT_REQUESTED') return; // Let agent reply
      }

      // Bot rule matching
      if (isBotSending) return;
      isBotSending = true;

      const rule = matchBotRule(text);
      showTypingIndicator();

      setTimeout(async () => {
        removeTypingIndicator();
        if (rule) {
          renderChatMessage('BOT', rule.reply);
          if (db && chatThreadId) {
            await sendChatMessageToFirestore('BOT', rule.reply, 'AI Assistant');
          }
          if (rule.action === 'REQUEST_AGENT') {
            if (db && chatThreadId) {
              await updateDoc(doc(db, 'support_threads', chatThreadId), { status: 'AGENT_REQUESTED' });
            }
          } else if (rule.action === 'SUGGEST_AGENT') {
            setTimeout(() => {
              renderChatPills([{ label: '🤝 Connect to Agent', text: 'Connect to agent' }]);
            }, 300);
          }
        } else {
          const fallback = "I'm not sure about that. Here are some things I can help you with:";
          renderChatMessage('BOT', fallback);
          if (db && chatThreadId) {
            await sendChatMessageToFirestore('BOT', fallback, 'AI Assistant');
          }
          renderChatPills(DEFAULT_PILLS);
        }
        isBotSending = false;
      }, 900 + Math.random() * 400);
    }

    // ── CHATBOT OPEN / CLOSE ──────────────────────────────────────
    function openChatWindow() {
      chatWindowOpen = true;
      chatWindow?.classList.add('open');
      // Clear unread
      if (db && chatThreadId && userUnreadCount > 0) {
        updateDoc(doc(db, 'support_threads', chatThreadId), { unreadUserCount: 0 }).catch(() => {});
      }
      userUnreadCount = 0;
      chatUnreadBadge?.classList.add('hidden');
      setTimeout(() => chatInput?.focus(), 200);
    }
    function closeChatWindow() {
      chatWindowOpen = false;
      chatWindow?.classList.remove('open');
    }

    chatLauncher?.addEventListener('click', () => {
      if (chatWindowOpen) { closeChatWindow(); return; }
      if (!currentUser) { showToast('Please sign in to use live support.', 'info'); return; }
      openChatWindow();
      if (db && !chatThreadId) ensureChatThread(currentUser);
      else if (!chatMessages?.children.length) ensureChatThread(currentUser);
    });
    chatClose?.addEventListener('click', closeChatWindow);

    // Send on Enter
    chatInput?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleChatSend();
      }
    });

    let chatSendLocked = false;
    async function handleChatSend() {
      if (chatSendLocked) return;
      const text = chatInput?.value?.trim();
      if (!text) return;
      chatSendLocked = true;
      if (chatInput) chatInput.value = '';
      await sendUserMessage(text);
      chatSendLocked = false;
    }
    chatSendBtn?.addEventListener('click', handleChatSend);

    // ── ADMIN CONSOLE ENGINE ──────────────────────────────────────
    function isAdminUser(user) {
      return user && user.email === ADMIN_EMAIL;
    }

    function initAdminConsole(user) {
      if (!isAdminUser(user) || !db) return;

      // Add Admin Console button to sidebar and mobile header
      const signoutArea = document.getElementById('btn-dash-signout');
      if (signoutArea && !document.getElementById('btn-admin-console')) {
        const adminBtn = document.createElement('button');
        adminBtn.id = 'btn-admin-console';
        adminBtn.type = 'button';
        adminBtn.title = 'Admin Console';
        adminBtn.className = 'w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl text-xs font-semibold text-cobalt hover:bg-blue-50 border border-blue-200 transition-colors cursor-pointer mt-2';
        adminBtn.innerHTML = '<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg><span class="sidebar-text">Admin Console</span>';
        adminBtn.addEventListener('click', openAdminConsole);
        signoutArea.parentNode?.insertBefore(adminBtn, signoutArea);
      }

      // Stream all support threads in real time
      if (unsubAdminThreads) unsubAdminThreads();
      const threadsRef = collection(db, 'support_threads');
      const threadsQuery = query(threadsRef, orderBy('lastUpdated', 'desc'));
      unsubAdminThreads = onSnapshot(threadsQuery, (snap) => {
        renderAdminThreadList(snap.docs);
      }, (err) => console.error("Admin threads snapshot error:", err));
    }

    function renderAdminThreadList(docs) {
      if (!adminThreadsList) return;
      if (docs.length === 0) {
        adminThreadsList.innerHTML = '<div class="flex flex-col items-center justify-center gap-2 py-10 px-4 text-center"><svg class="w-8 h-8 text-slate-200" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg><div class="text-[11px] text-slate-400 font-medium">No active support threads</div></div>';
        adminThreadCount && (adminThreadCount.textContent = '0 open threads');
        return;
      }

      adminThreadCount && (adminThreadCount.textContent = `${docs.length} open thread${docs.length !== 1 ? 's' : ''}`);

      adminThreadsList.innerHTML = docs.map(docSnap => {
        const d = docSnap.data();
        const tid = docSnap.id;
        const statusBadge = {
          BOT_ACTIVE: '<span class="status-badge status-bot">Bot</span>',
          AGENT_REQUESTED: '<span class="status-badge status-requested">Requested</span>',
          AGENT_CONNECTED: '<span class="status-badge status-connected">Live</span>',
          RESOLVED: '<span class="status-badge status-resolved">Resolved</span>'
        }[d.status] || '<span class="status-badge status-bot">Bot</span>';

        const avatarHtml = d.userPhoto
          ? `<img src="${d.userPhoto}" class="w-9 h-9 rounded-full object-cover flex-shrink-0" alt="${d.userName}" />`
          : `<div class="w-9 h-9 rounded-full bg-blue-100 text-cobalt font-bold text-xs flex items-center justify-center flex-shrink-0">${(d.userName || 'U')[0].toUpperCase()}</div>`;

        const unread = d.unreadAdminCount > 0
          ? `<span class="text-[9px] font-bold bg-crimson text-white rounded-full px-1.5 py-0.5">${d.unreadAdminCount}</span>` : '';

        return `<div class="admin-thread-item${activeAdminThreadId === tid ? ' active' : ''}" data-tid="${tid}">
          ${avatarHtml}
          <div class="min-w-0 flex-1">
            <div class="flex items-center justify-between gap-1 mb-0.5">
              <span class="text-xs font-bold text-charcoal truncate">${d.userName || 'User'}</span>
              <div class="flex items-center gap-1">${unread}${statusBadge}</div>
            </div>
            <div class="text-[11px] text-slate-400 truncate">${d.lastMessage || 'No messages yet'}</div>
          </div>
        </div>`;
      }).join('');

      adminThreadsList.querySelectorAll('.admin-thread-item').forEach(el => {
        el.addEventListener('click', () => selectAdminThread(el.dataset.tid));
      });
    }

    function selectAdminThread(tid) {
      activeAdminThreadId = tid;
      // Re-render list to mark active
      document.querySelectorAll('.admin-thread-item').forEach(el => {
        el.classList.toggle('active', el.dataset.tid === tid);
      });

      // Enable reply inputs
      if (adminReplyInput) adminReplyInput.disabled = false;
      if (adminReplySend) adminReplySend.disabled = false;
      adminTakeoverBtn?.classList.remove('hidden');
      adminResolveBtn?.classList.remove('hidden');

      // Fetch and display thread user info
      if (db) {
        getDoc(doc(db, 'support_threads', tid)).then(snap => {
          if (snap.exists()) {
            const d = snap.data();
            if (adminSelectedUser) adminSelectedUser.textContent = `🧑 ${d.userName || 'User'} · ${d.userEmail || ''} · ${d.status}`;
            // Clear admin unread
            updateDoc(doc(db, 'support_threads', tid), { unreadAdminCount: 0 }).catch(() => {});
          }
        });
      }

      // Subscribe to messages
      if (unsubAdminMessages) unsubAdminMessages();
      const msgsQuery = query(collection(db, 'support_threads', tid, 'messages'), orderBy('timestamp', 'asc'));
      unsubAdminMessages = onSnapshot(msgsQuery, (snap) => {
        if (!adminChatMessages) return;
        adminChatMessages.innerHTML = '';
        if (snap.empty) {
          adminChatMessages.innerHTML = '<div class="flex flex-col items-center justify-center gap-2 h-full text-center"><div class="text-xs text-slate-300">No messages yet in this thread</div></div>';
          return;
        }
        snap.forEach(docSnap => {
          const d = docSnap.data();
          const isUser = d.sender === 'USER';
          const isAdmin = d.sender === 'ADMIN';
          const isBot = d.sender === 'BOT';
          const div = document.createElement('div');
          div.style.cssText = 'display:flex;flex-direction:column;align-items:' + (isUser ? 'flex-end' : 'flex-start') + ';gap:2px;margin-bottom:4px';
          const label = document.createElement('div');
          label.style.cssText = 'font-size:9px;font-family:monospace;color:#94A3B8;font-weight:600;padding:0 4px';
          label.textContent = (d.senderName || d.sender) + (d.sender === 'BOT' ? ' · AI' : d.sender === 'ADMIN' ? ' · Agent' : ' · User');
          const bubble = document.createElement('div');
          bubble.style.cssText = 'max-width:78%;padding:8px 12px;border-radius:14px;font-size:12px;font-family:Inter,sans-serif;line-height:1.45;' +
            (isUser ? 'background:#EFF6FF;color:#1E3A5F;border-bottom-right-radius:3px' :
             isAdmin ? 'background:#0B0F19;color:#fff;border-bottom-left-radius:3px' :
             'background:#F1F5F9;color:#0F172A;border-bottom-left-radius:3px');
          bubble.innerHTML = d.text;
          div.appendChild(label);
          div.appendChild(bubble);
          adminChatMessages.appendChild(div);
        });
        adminChatMessages.scrollTop = adminChatMessages.scrollHeight;
      }, err => console.error("Admin messages snapshot error:", err));
    }

    // Admin Takeover
    adminTakeoverBtn?.addEventListener('click', async () => {
      if (!activeAdminThreadId || !db) return;
      await updateDoc(doc(db, 'support_threads', activeAdminThreadId), {
        status: 'AGENT_CONNECTED',
        lastUpdated: serverTimestamp()
      });
      showToast('Chat taken over. You are now the live agent.', 'success');
    });

    // Admin Resolve
    adminResolveBtn?.addEventListener('click', async () => {
      if (!activeAdminThreadId || !db) return;
      await updateDoc(doc(db, 'support_threads', activeAdminThreadId), {
        status: 'RESOLVED',
        lastUpdated: serverTimestamp()
      });
      // Send resolved bot message to user
      const msgsRef = collection(db, 'support_threads', activeAdminThreadId, 'messages');
      await addDoc(msgsRef, { sender: 'ADMIN', senderName: 'Support Agent', text: '✅ This support session has been marked as resolved. Thank you for reaching out!', timestamp: serverTimestamp() });
      showToast('Thread marked as resolved.', 'success');
    });

    // Admin Reply Send
    let adminSendLocked = false;
    async function handleAdminReply() {
      if (adminSendLocked || !activeAdminThreadId || !db) return;
      const text = adminReplyInput?.value?.trim();
      if (!text) return;
      adminSendLocked = true;
      if (adminReplyInput) adminReplyInput.value = '';

      try {
        const msgsRef = collection(db, 'support_threads', activeAdminThreadId, 'messages');
        await addDoc(msgsRef, {
          sender: 'ADMIN',
          senderName: currentUser?.displayName || 'Support Agent',
          text,
          timestamp: serverTimestamp()
        });
        await updateDoc(doc(db, 'support_threads', activeAdminThreadId), {
          lastMessage: text.substring(0, 80),
          lastUpdated: serverTimestamp(),
          status: 'AGENT_CONNECTED',
          unreadUserCount: increment(1)
        });
      } catch (err) {
        console.error("Admin reply error:", err);
        showToast('Failed to send reply.', 'error');
      } finally {
        adminSendLocked = false;
        adminReplyInput?.focus();
      }
    }

    adminReplySend?.addEventListener('click', handleAdminReply);
    adminReplyInput?.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleAdminReply(); }
    });

    // Open/Close Admin Console
    function openAdminConsole() {
      adminConsoleOverlay?.classList.add('open');
    }
    adminConsoleClose?.addEventListener('click', () => {
      adminConsoleOverlay?.classList.remove('open');
    });
    adminConsoleOverlay?.addEventListener('click', (e) => {
      if (e.target === adminConsoleOverlay) adminConsoleOverlay.classList.remove('open');
    });

    // Initialize chatbot after login
    const _origEnterDashboard = enterDashboard;
    // Override enterDashboard to also init chatbot
"""

# Inject the JS before the closing of the module script
# Find the enterDashboard function call in onAuthStateChanged
inject_before = "    onAuthStateChanged(auth, (user) => {"

chat_init_js = """
    // Init chat & admin when auth state fires
    function initChatSystem(user) {
      if (!user || !db) return;
      ensureChatThread(user);
      if (isAdminUser(user)) initAdminConsole(user);
    }

"""

if inject_before in html and "initChatSystem" not in html:
    html = html.replace(inject_before, chat_init_js + "    " + inject_before, 1)
    print("Injected initChatSystem function.")

# Modify onAuthStateChanged to call initChatSystem
old_auth_block = """    onAuthStateChanged(auth, (user) => {
      if (user) {
        enterDashboard(user);
      } else {
        exitToAuth();
      }
    });"""

new_auth_block = """    onAuthStateChanged(auth, (user) => {
      if (user) {
        enterDashboard(user);
        initChatSystem(user);
      } else {
        exitToAuth();
        chatThreadId = null;
        if (unsubChatMessages) { unsubChatMessages(); unsubChatMessages = null; }
        if (unsubAdminThreads) { unsubAdminThreads(); unsubAdminThreads = null; }
      }
    });"""

if old_auth_block in html:
    html = html.replace(old_auth_block, new_auth_block, 1)
    print("Updated onAuthStateChanged to call initChatSystem.")

# Inject the full chatbot JS before the onAuthStateChanged block
if "TWO-WAY LIVE SUPPORT & BOT ENGINE" not in html:
    html = html.replace(inject_before.strip(), chatbot_js.strip() + "\n\n    " + inject_before.strip(), 1)
    print("Injected chatbot JS engine.")
else:
    print("Chatbot JS already present, skipping JS injection.")

# ─── SAVE ─────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved index.html successfully! Length:", len(html))
