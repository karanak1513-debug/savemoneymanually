"""
SAVING GUIDE - Complete replacement script.
Removes OLD chatbot code (CSS L527-910, JS L3478-3476+, HTML L4027-4133)
and injects the new Saving Guide Hybrid Bot & Admin Desk.
"""

import re

ADMIN_EMAIL = "karanak1513@gmail.com"

# ── NEW CSS ───────────────────────────────────────────────────────────────────
SAVING_GUIDE_CSS = r"""
    /* ========================================================== */
    /* ░░  SAVING GUIDE — HYBRID BOT & LIVE ADMIN DESK CSS  ░░   */
    /* ========================================================== */

    /* ── Floating Launcher ─────────────────────────────────────── */
    #sg-launcher {
      position: fixed;
      bottom: 1.75rem;
      right: 1.75rem;
      z-index: 9100;
      width: 3.6rem;
      height: 3.6rem;
      border-radius: 50%;
      background: linear-gradient(145deg, #1E3A8A 0%, #2563EB 55%, #3B82F6 100%);
      box-shadow: 0 8px 32px rgba(37,99,235,0.50), 0 2px 8px rgba(37,99,235,0.28), inset 0 1px 0 rgba(255,255,255,0.18);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      border: none;
      outline: none;
      transition: transform 0.22s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.18s ease;
    }
    #sg-launcher:hover {
      transform: scale(1.12) translateY(-2px);
      box-shadow: 0 14px 44px rgba(37,99,235,0.58), 0 4px 14px rgba(37,99,235,0.36);
    }
    #sg-launcher-label {
      position: absolute;
      bottom: calc(100% + 10px);
      right: 0;
      background: #0B0F19;
      color: #fff;
      font-size: 0.68rem;
      font-weight: 700;
      font-family: 'Inter', sans-serif;
      padding: 4px 10px;
      border-radius: 8px;
      white-space: nowrap;
      pointer-events: none;
      opacity: 0;
      transform: translateY(4px);
      transition: all 0.18s ease;
    }
    #sg-launcher:hover #sg-launcher-label { opacity: 1; transform: translateY(0); }
    #sg-unread-badge {
      position: absolute;
      top: -2px;
      right: -2px;
      min-width: 1.15rem;
      height: 1.15rem;
      background: #E11D48;
      color: #fff;
      font-size: 0.58rem;
      font-weight: 900;
      border-radius: 999px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 3px;
      border: 2px solid #fff;
      box-shadow: 0 2px 8px rgba(225,29,72,0.55);
      pointer-events: none;
      animation: sgbadgepulse 1.7s ease-in-out infinite;
    }
    #sg-unread-badge.hidden { display: none !important; }
    @keyframes sgbadgepulse {
      0%,100% { transform: scale(1); }
      50% { transform: scale(1.18); }
    }

    /* ── Chat Window ────────────────────────────────────────────── */
    #sg-window {
      position: fixed;
      bottom: 7rem;
      right: 1.75rem;
      width: 23rem;
      max-width: calc(100vw - 2rem);
      height: 510px;
      background: #FFFFFF;
      border-radius: 1.6rem;
      border: 1px solid rgba(226,232,240,0.95);
      box-shadow: 0 32px 80px rgba(15,23,42,0.16), 0 8px 24px rgba(15,23,42,0.07);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      z-index: 9099;
      transform: scale(0.90) translateY(14px);
      opacity: 0;
      pointer-events: none;
      transition: all 0.28s cubic-bezier(0.34,1.56,0.64,1);
    }
    #sg-window.open {
      transform: scale(1) translateY(0);
      opacity: 1;
      pointer-events: all;
    }

    /* ── Chat Header ────────────────────────────────────────────── */
    #sg-header {
      background: linear-gradient(145deg, #070B12 0%, #0F172A 50%, #1E293B 100%);
      padding: 0.9rem 1rem 0.85rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    #sg-avatar {
      width: 2.1rem;
      height: 2.1rem;
      border-radius: 50%;
      background: linear-gradient(135deg, #2563EB, #1D4ED8);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      box-shadow: 0 2px 8px rgba(37,99,235,0.50);
    }
    #sg-header-info { min-width: 0; }
    #sg-agent-name {
      color: #F8FAFC;
      font-size: 0.8rem;
      font-weight: 800;
      font-family: 'Plus Jakarta Sans', sans-serif;
      line-height: 1.2;
    }
    #sg-status-row { display: flex; align-items: center; gap: 5px; margin-top: 2px; }
    #sg-status-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #34D399;
      flex-shrink: 0;
      transition: background 0.3s ease;
    }
    #sg-status-dot.busy { background: #F59E0B; animation: sgstatuspulse 1.4s infinite; }
    #sg-status-dot.live { background: #60A5FA; animation: sgstatuspulse 1.2s infinite; }
    @keyframes sgstatuspulse {
      0%,100% { box-shadow: 0 0 0 0 currentColor; opacity: 1; }
      50% { box-shadow: 0 0 0 4px transparent; opacity: 0.7; }
    }
    #sg-status-label {
      color: #64748B;
      font-size: 0.65rem;
      font-family: 'Space Grotesk', monospace;
      font-weight: 600;
      letter-spacing: 0.02em;
    }
    #sg-header-actions { display: flex; align-items: center; gap: 4px; }
    .sg-header-btn {
      background: none;
      border: none;
      cursor: pointer;
      color: #475569;
      padding: 5px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: color 0.15s ease, background 0.15s ease;
    }
    .sg-header-btn:hover { color: #F8FAFC; background: rgba(255,255,255,0.08); }

    /* ── Messages Stream ────────────────────────────────────────── */
    #sg-messages {
      flex: 1;
      overflow-y: auto;
      padding: 1rem 0.875rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      scroll-behavior: smooth;
      background: #FAFBFC;
    }
    #sg-messages::-webkit-scrollbar { width: 3px; }
    #sg-messages::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 99px; }

    /* ── Message Bubbles ────────────────────────────────────────── */
    .sg-msg-wrap {
      display: flex;
      flex-direction: column;
      gap: 2px;
      animation: sgfadein 0.2s ease both;
    }
    @keyframes sgfadein {
      from { opacity: 0; transform: translateY(7px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .sg-msg-wrap.user-wrap { align-items: flex-end; }
    .sg-msg-wrap.bot-wrap,
    .sg-msg-wrap.admin-wrap { align-items: flex-start; }

    .sg-bubble {
      max-width: 78%;
      padding: 0.6rem 0.875rem;
      font-size: 0.785rem;
      line-height: 1.5;
      font-family: 'Inter', sans-serif;
      border-radius: 1.2rem;
      word-break: break-word;
    }
    .sg-bubble-user {
      background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
      color: #fff;
      border-bottom-right-radius: 4px;
    }
    .sg-bubble-bot {
      background: #FFFFFF;
      color: #0F172A;
      border: 1px solid #E8EDF4;
      border-bottom-left-radius: 4px;
      box-shadow: 0 1px 4px rgba(15,23,42,0.05);
    }
    .sg-bubble-admin {
      background: linear-gradient(135deg, #0B0F19 0%, #1E293B 100%);
      color: #F1F5F9;
      border-bottom-left-radius: 4px;
    }
    .sg-sender-tag {
      font-size: 0.6rem;
      font-weight: 700;
      color: #94A3B8;
      font-family: 'Space Grotesk', monospace;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 0 4px;
    }
    /* Admin tag in Cobalt */
    .sg-sender-tag.admin-tag { color: #60A5FA; }

    /* ── Message Tick Status ────────────────────────────────────── */
    .sg-ticks {
      font-size: 0.72rem;
      margin-top: 1px;
      padding-right: 2px;
      font-weight: 700;
      letter-spacing: -1px;
      line-height: 1;
      display: inline-block;
      transition: color 0.35s ease;
    }
    .sg-ticks.sent    { color: #94A3B8; }  /* ✓ single gray  */
    .sg-ticks.delivered { color: #94A3B8; } /* ✓✓ double gray */
    .sg-ticks.seen    { color: #2563EB; }  /* ✓✓ double blue */

    /* ── Quick Action Pills ─────────────────────────────────────── */
    .sg-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem;
      padding: 0 4px;
    }
    .sg-pill {
      background: #EFF6FF;
      color: #2563EB;
      border: 1.5px solid #BFDBFE;
      border-radius: 999px;
      padding: 0.28rem 0.7rem;
      font-size: 0.7rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
      font-family: 'Inter', sans-serif;
      white-space: nowrap;
    }
    .sg-pill:hover {
      background: #2563EB;
      color: #fff;
      border-color: #2563EB;
      transform: translateY(-1px);
    }

    /* ── Typing Indicator ───────────────────────────────────────── */
    #sg-typing-indicator {
      display: none;
      flex-direction: column;
      gap: 2px;
      align-self: flex-start;
    }
    #sg-typing-indicator.visible { display: flex; animation: sgfadein 0.2s ease both; }
    .sg-typing-label {
      font-size: 0.6rem;
      font-weight: 700;
      color: #94A3B8;
      font-family: 'Space Grotesk', monospace;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding-left: 4px;
    }
    .sg-typing-bubble {
      background: #FFFFFF;
      border: 1px solid #E8EDF4;
      border-radius: 1.2rem;
      border-bottom-left-radius: 4px;
      padding: 0.55rem 0.875rem;
      display: flex;
      gap: 5px;
      align-items: center;
      width: fit-content;
      box-shadow: 0 1px 4px rgba(15,23,42,0.05);
    }
    .sg-typing-bubble span {
      width: 7px;
      height: 7px;
      background: #CBD5E1;
      border-radius: 50%;
      animation: sgtyping 1.1s ease-in-out infinite;
    }
    .sg-typing-bubble span:nth-child(2) { animation-delay: 0.15s; }
    .sg-typing-bubble span:nth-child(3) { animation-delay: 0.30s; }
    @keyframes sgtyping {
      0%,60%,100% { transform: translateY(0); opacity: 0.5; }
      30% { transform: translateY(-5px); opacity: 1; }
    }

    /* ── Date Separator ─────────────────────────────────────────── */
    .sg-date-sep {
      text-align: center;
      font-size: 0.6rem;
      font-weight: 700;
      color: #CBD5E1;
      font-family: 'Space Grotesk', monospace;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin: 4px 0;
      position: relative;
    }
    .sg-date-sep::before, .sg-date-sep::after {
      content: '';
      position: absolute;
      top: 50%;
      width: 30%;
      height: 1px;
      background: #F1F5F9;
    }
    .sg-date-sep::before { left: 0; }
    .sg-date-sep::after { right: 0; }

    /* ── Input Area ─────────────────────────────────────────────── */
    #sg-input-area {
      border-top: 1px solid #F1F5F9;
      padding: 0.7rem 0.875rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-shrink: 0;
      background: #FFFFFF;
    }
    #sg-text-input {
      flex: 1;
      background: #F8FAFC;
      border: 1.5px solid #E2E8F0;
      border-radius: 14px;
      padding: 0.52rem 0.875rem;
      font-size: 0.78rem;
      font-family: 'Inter', sans-serif;
      color: #0F172A;
      outline: none;
      transition: border-color 0.15s ease, background 0.15s ease;
      resize: none;
    }
    #sg-text-input:focus { border-color: #2563EB; background: #fff; }
    #sg-text-input::placeholder { color: #CBD5E1; }
    #sg-send-btn {
      width: 2.3rem;
      height: 2.3rem;
      border-radius: 12px;
      background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
      color: #fff;
      border: none;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.15s ease;
      flex-shrink: 0;
      box-shadow: 0 2px 8px rgba(37,99,235,0.35);
    }
    #sg-send-btn:hover:not(:disabled) { transform: scale(1.08); box-shadow: 0 4px 14px rgba(37,99,235,0.45); }
    #sg-send-btn:disabled { opacity: 0.45; cursor: not-allowed; transform: none; box-shadow: none; }

    /* ── ░░░ ADMIN LIVE DESK ░░░ ────────────────────────────────── */
    #sg-admin-overlay {
      position: fixed;
      inset: 0;
      background: rgba(7,11,18,0.72);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      z-index: 10200;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1rem;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.22s ease;
    }
    #sg-admin-overlay.open { opacity: 1; pointer-events: all; }
    #sg-admin-desk {
      width: 100%;
      max-width: 1160px;
      height: min(88vh, 740px);
      background: #FFFFFF;
      border-radius: 1.75rem;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 48px 140px rgba(7,11,18,0.35), 0 8px 32px rgba(7,11,18,0.12);
      border: 1px solid rgba(226,232,240,0.6);
    }
    #sg-admin-topbar {
      background: linear-gradient(145deg, #070B12, #0F172A 60%, #1E293B);
      padding: 0.875rem 1.25rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    #sg-admin-body {
      flex: 1;
      display: flex;
      overflow: hidden;
    }

    /* Left panel */
    #sg-threads-panel {
      width: 34%;
      border-right: 1px solid #F1F5F9;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background: #FAFBFC;
    }
    #sg-threads-header {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid #F1F5F9;
      background: #FFFFFF;
      flex-shrink: 0;
    }
    #sg-threads-list {
      flex: 1;
      overflow-y: auto;
    }
    #sg-threads-list::-webkit-scrollbar { width: 3px; }
    #sg-threads-list::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 99px; }
    .sg-thread-row {
      padding: 0.75rem 1rem;
      cursor: pointer;
      border-bottom: 1px solid #F8FAFC;
      transition: background 0.12s ease;
      display: flex;
      align-items: flex-start;
      gap: 0.6rem;
      position: relative;
    }
    .sg-thread-row:hover { background: #F8FAFC; }
    .sg-thread-row.active-thread {
      background: #EFF6FF;
      border-left: 3px solid #2563EB;
    }
    .sg-thread-avatar {
      width: 2.25rem;
      height: 2.25rem;
      border-radius: 50%;
      object-fit: cover;
      flex-shrink: 0;
    }
    .sg-thread-initials {
      width: 2.25rem;
      height: 2.25rem;
      border-radius: 50%;
      background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
      color: #2563EB;
      font-weight: 800;
      font-size: 0.75rem;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .sg-thread-online-dot {
      position: absolute;
      top: 0.85rem;
      left: 2.9rem;
      width: 9px;
      height: 9px;
      border-radius: 50%;
      border: 2px solid #FAFBFC;
    }
    .sg-thread-online-dot.online { background: #34D399; }
    .sg-thread-online-dot.offline { background: #CBD5E1; }

    /* Right chat terminal */
    #sg-admin-chat-panel {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    #sg-admin-toolbar {
      padding: 0.7rem 1rem;
      border-bottom: 1px solid #F1F5F9;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      flex-shrink: 0;
      background: #FFFFFF;
      min-height: 3.5rem;
    }
    #sg-admin-messages {
      flex: 1;
      overflow-y: auto;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      background: #FAFBFC;
    }
    #sg-admin-messages::-webkit-scrollbar { width: 3px; }
    #sg-admin-messages::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 99px; }
    #sg-admin-reply-bar {
      border-top: 1px solid #F1F5F9;
      padding: 0.7rem 1rem;
      display: flex;
      gap: 0.5rem;
      flex-shrink: 0;
      background: #FFFFFF;
    }
    #sg-admin-input {
      flex: 1;
      background: #F8FAFC;
      border: 1.5px solid #E2E8F0;
      border-radius: 14px;
      padding: 0.58rem 1rem;
      font-size: 0.8rem;
      font-family: 'Inter', sans-serif;
      color: #0F172A;
      outline: none;
      transition: border-color 0.15s ease, background 0.15s ease;
    }
    #sg-admin-input:focus { border-color: #2563EB; background: #fff; }
    #sg-admin-input::placeholder { color: #CBD5E1; }
    #sg-admin-input:disabled { opacity: 0.5; cursor: not-allowed; }
    #sg-admin-send {
      padding: 0.6rem 1.2rem;
      background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
      color: #fff;
      border: none;
      border-radius: 12px;
      font-size: 0.78rem;
      font-weight: 700;
      cursor: pointer;
      font-family: 'Inter', sans-serif;
      transition: all 0.15s ease;
      box-shadow: 0 2px 8px rgba(37,99,235,0.30);
    }
    #sg-admin-send:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(37,99,235,0.40); }
    #sg-admin-send:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

    /* Status Chips */
    .sg-chip {
      font-size: 0.6rem;
      font-weight: 800;
      padding: 0.15rem 0.52rem;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-family: 'Space Grotesk', monospace;
      white-space: nowrap;
    }
    .sg-chip-bot      { background: #F1F5F9; color: #64748B; }
    .sg-chip-live     { background: #EFF6FF; color: #2563EB; animation: livepulse 1.3s infinite; }
    .sg-chip-request  { background: #FFF1F2; color: #E11D48; animation: livepulse 1.3s infinite; }
    .sg-chip-resolved { background: #ECFDF5; color: #059669; }
    @keyframes livepulse {
      0%,100% { box-shadow: 0 0 0 0 currentColor; }
      50%      { box-shadow: 0 0 0 3px transparent; }
    }

    /* Unread count pill */
    .sg-unread-pill {
      min-width: 1rem;
      height: 1rem;
      background: #E11D48;
      color: #fff;
      font-size: 0.58rem;
      font-weight: 900;
      border-radius: 999px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 3px;
    }
"""

# ── NEW HTML ──────────────────────────────────────────────────────────────────
SAVING_GUIDE_HTML = """
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

      </div><!-- /admin-body -->
    </div><!-- /admin-desk -->
  </div><!-- /admin-overlay -->
"""

# ── NEW JS ────────────────────────────────────────────────────────────────────
SAVING_GUIDE_JS = r"""
    // ================================================================
    // ░░  SAVING GUIDE — HYBRID BOT & LIVE ADMIN DESK ENGINE  ░░
    // ================================================================
    (() => {
      const ADMIN_EMAIL  = 'karanak1513@gmail.com';
      const BOT_TIMEOUT  = 5000; // ms admin must reply before bot takes over

      // ── State ────────────────────────────────────────────────────
      let sgThreadId       = null;
      let sgWindowOpen     = false;
      let sgSendLock       = false;
      let sgBotLock        = false;
      let sgBotTimer       = null;
      let sgUnsubMsgs      = null;
      let sgUnsubThread    = null;
      let sgUnsubAdmin     = null;  // admin threads stream
      let sgUnsubAdminMsgs = null;  // admin selected thread messages
      let sgActiveThread   = null;  // admin: selected threadId
      let sgAdminSendLock  = false;
      let sgChatStatus     = 'BOT_AUTONOMOUS';

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

      // ── BOT BRAIN ────────────────────────────────────────────────
      const BOT_KB = [
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
        const snap = await getDoc(tRef);
        if (!snap.exists()) {
          await setDoc(tRef, {
            userId:          user.uid,
            userName:        user.displayName || user.email?.split('@')[0] || 'User',
            userEmail:       user.email || '',
            userPhoto:       user.photoURL || '',
            chatStatus:      'BOT_AUTONOMOUS',
            lastMessage:     '',
            lastMessageTime: serverTimestamp(),
            userUnread:      0,
            adminUnread:     0
          });
        }

        // Watch thread status
        if (sgUnsubThread) sgUnsubThread();
        sgUnsubThread = onSnapshot(tRef, (s) => {
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

        // Watch messages
        if (sgUnsubMsgs) sgUnsubMsgs();
        const qry = query(
          collection(db, 'support_threads', sgThreadId, 'messages'),
          orderBy('timestamp', 'asc')
        );
        sgUnsubMsgs = onSnapshot(qry, (snap) => {
          // Clear all except typing indicator
          if (!elMessages) return;
          // Remove all msg-wrap nodes
          elMessages.querySelectorAll('.sg-msg-wrap, .sg-pills, .sg-date-sep').forEach(n => n.remove());

          if (snap.empty) {
            // Welcome
            renderWelcome();
            return;
          }
          snap.forEach(ds => {
            const d = ds.data();
            renderMsg(ds.id, d.sender, d.text, d.status, d.timestamp);
          });

          // Auto-mark DELIVERED msgs as SEEN if window is open
          if (sgWindowOpen) {
            snap.forEach(ds => {
              const d = ds.data();
              if (d.sender !== 'USER' && d.status !== 'SEEN') {
                updateDoc(ds.ref, { status: 'SEEN' }).catch(() => {});
              }
            });
          }

          // Also update user msg ticks if admin has seen them
          if (sgChatStatus === 'ADMIN_LIVE') {
            snap.forEach(ds => {
              const d = ds.data();
              if (d.sender === 'USER' && d.status === 'DELIVERED') {
                updateDoc(ds.ref, { status: 'SEEN' }).catch(() => {});
              }
            });
          }
        }, (err) => console.error('sg-msgs snapshot error', err));
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

        // Cancel pending bot timer if admin was going to be waited for
        if (sgBotTimer) { clearTimeout(sgBotTimer); sgBotTimer = null; }

        // Optimistic UI
        const optimisticWrap = renderMsg(null, 'USER', text, 'SENT', new Date());

        // Write to Firestore
        let msgDocId = null;
        if (db && sgThreadId) {
          try {
            const ref = await addDoc(
              collection(db, 'support_threads', sgThreadId, 'messages'),
              { sender: 'USER', text, status: 'SENT', timestamp: serverTimestamp() }
            );
            msgDocId = ref.id;
            // Update to DELIVERED
            await updateDoc(ref, { status: 'DELIVERED' });
            await updateDoc(doc(db, 'support_threads', sgThreadId), {
              lastMessage: text.substring(0,80),
              lastMessageTime: serverTimestamp(),
              adminUnread: increment(1)
            });
            // Update optimistic tick to delivered
            updateMessageTick(optimisticWrap, 'DELIVERED');
          } catch (e) { console.warn('User msg write error:', e); }
        }

        sgSendLock = false;

        // If bot autonomous → bot will reply (with 5s admin window)
        if (sgChatStatus === 'BOT_AUTONOMOUS') {
          botRespond(text);
        }
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
          ab.addEventListener('click', () => elAdminOverlay?.classList.add('open'));
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
        if (e.target === elAdminOverlay) elAdminOverlay.classList.remove('open');
      });
      elAdminClose?.addEventListener('click', () => elAdminOverlay?.classList.remove('open'));

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
        ensureThread(user);
        if (isAdmin(user)) initAdminDesk(user);
      };

    })(); // IIFE end
"""

# ── APPLY CHANGES ─────────────────────────────────────────────────────────────
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()
    lines = html.split('\n')

print(f"Original lines: {len(lines)}")
print(f"Original bytes: {len(html)}")

# ── STEP 1: REMOVE OLD CHATBOT CSS (L527-910, 0-indexed: 526-909) ────────────
CSS_START_MARKER = '    /* ========================================================== */\n    /* CHATBOT WIDGET & ADMIN CONSOLE STYLES'
CSS_END_MARKER   = '\n    /* ── TOAST MESSAGES'

# Find and replace the old CSS block
css_start = html.find(CSS_START_MARKER)
css_end   = html.find(CSS_END_MARKER, css_start)

if css_start != -1 and css_end != -1:
    old_css_block = html[css_start:css_end]
    html = html.replace(old_css_block, SAVING_GUIDE_CSS + '\n    /* ── TOAST MESSAGES'.rstrip(' \n') + '\n    ', 1)
    print(f"CSS replaced: {len(old_css_block)} bytes → {len(SAVING_GUIDE_CSS)} bytes")
else:
    # Fallback: inject before toast section
    if '/* ── TOAST MESSAGES' in html and CSS_START_MARKER not in html:
        html = html.replace('    /* ── TOAST MESSAGES', SAVING_GUIDE_CSS + '\n    /* ── TOAST MESSAGES', 1)
        print("CSS injected before toast (fallback).")
    else:
        print(f"WARNING: CSS markers not found! css_start={css_start}, css_end={css_end}")

# ── STEP 2: REMOVE OLD CHATBOT JS (L3478 to end of old block) ────────────────
JS_START_MARKER = '    // ============================================================\n    // TWO-WAY LIVE SUPPORT & BOT ENGINE'
JS_END_MARKER   = '    });\n\n  </script>'  # closing of the old module

js_start = html.find(JS_START_MARKER)
js_end   = html.find(JS_END_MARKER, js_start)

if js_start != -1 and js_end != -1:
    old_js = html[js_start : js_end + len(JS_END_MARKER)]
    # Replace old JS with new JS + closing script
    html = html.replace(old_js, '\n  </script>', 1)
    print(f"JS removed: {len(old_js)} bytes")
else:
    # Also try alternate markers
    alt_js_start = html.find('// TWO-WAY LIVE SUPPORT & BOT ENGINE')
    if alt_js_start != -1:
        # Find the </script> that closes this block
        sc_end = html.find('  </script>', alt_js_start)
        if sc_end != -1:
            old_block = html[alt_js_start : sc_end]
            html = html.replace(html[alt_js_start - 4 : sc_end], '', 1)
            print(f"JS removed via alt marker")
    else:
        print(f"WARNING: JS markers not found! js_start={js_start}, js_end={js_end}")

# ── STEP 3: REMOVE OLD CHATBOT HTML (L4027-4133) ─────────────────────────────
HTML_START_MARKER = '  <!-- ============================================================ -->\n  <!-- FLOATING CHATBOT WIDGET & ADMIN CONSOLE'
HTML_END_MARKER   = '\n</body>'

h_start = html.find(HTML_START_MARKER)
h_end   = html.rfind(HTML_END_MARKER)

if h_start != -1 and h_end != -1 and h_start < h_end:
    old_html_block = html[h_start:h_end]
    html = html.replace(old_html_block, '', 1)
    print(f"Old chatbot HTML removed: {len(old_html_block)} bytes")
else:
    print(f"WARNING: HTML block markers not found! h_start={h_start}, h_end={h_end}")

# ── STEP 4: INJECT NEW HTML before </body> ───────────────────────────────────
if SAVING_GUIDE_HTML[:30] not in html:
    html = html.replace('\n</body>', SAVING_GUIDE_HTML + '\n</body>', 1)
    print(f"New Saving Guide HTML injected ({len(SAVING_GUIDE_HTML)} bytes)")
else:
    print("Saving Guide HTML already present.")

# ── STEP 5: INJECT NEW JS before </script> closing the main module ────────────
# Find the last script block closing before </body>
main_script_end = html.rfind('  </script>\n</body>')
if main_script_end != -1:
    html = html[:main_script_end] + '\n' + SAVING_GUIDE_JS + '\n  </script>\n</body>' + html[main_script_end + len('  </script>\n</body>'):]
    print(f"New Saving Guide JS injected ({len(SAVING_GUIDE_JS)} bytes)")
else:
    # fallback: inject before final </script>
    last_script = html.rfind('  </script>')
    if last_script != -1:
        html = html[:last_script] + '\n' + SAVING_GUIDE_JS + '\n  </script>' + html[last_script + len('  </script>'):]
        print("New JS injected via fallback.</script>")

# ── STEP 6: Update onAuthStateChanged to call __sgInit ───────────────────────
OLD_AUTH = """    onAuthStateChanged(auth, (user) => {
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

NEW_AUTH = """    onAuthStateChanged(auth, (user) => {
      if (user) {
        enterDashboard(user);
        if (typeof window.__sgInit === 'function') window.__sgInit(user);
      } else {
        exitToAuth();
        if (typeof window.__sgInit === 'function') window.__sgInit(null);
      }
    });"""

if OLD_AUTH in html:
    html = html.replace(OLD_AUTH, NEW_AUTH, 1)
    print("Updated onAuthStateChanged → window.__sgInit()")
elif 'initChatSystem(user)' in html:
    html = html.replace('initChatSystem(user);', "if (typeof window.__sgInit === 'function') window.__sgInit(user);", 1)
    html = html.replace('initChatSystem(null);', "if (typeof window.__sgInit === 'function') window.__sgInit(null);", 1)
    print("Patched initChatSystem calls → window.__sgInit")
else:
    # direct patch
    html = html.replace(
        "        enterDashboard(user);\n      } else {",
        "        enterDashboard(user);\n        if (typeof window.__sgInit === 'function') window.__sgInit(user);\n      } else {",
    )
    html = html.replace(
        "        exitToAuth();\n      }",
        "        exitToAuth();\n        if (typeof window.__sgInit === 'function') window.__sgInit(null);\n      }",
    )
    print("Patched onAuthStateChanged via fallback string replace.")

# ── STEP 7: Remove dead initChatSystem / old chatbot var declarations ─────────
dead_code_patterns = [
    'let chatThreadId = null;',
    'let unsubChatMessages = null;',
    'let unsubAdminThreads = null;',
    'let unsubAdminMessages = null;',
    'let activeAdminThreadId = null;',
    'let chatWindowOpen = false;',
    'let userUnreadCount = 0;',
    'let isBotSending = false;',
    'function initChatSystem(',
    'function initAdminConsole(',
    'function ensureChatThread(',
    'const ADMIN_EMAIL = \'karanak1513@gmail.com\';',
    'const BOT_RULES = [',
]
for pattern in dead_code_patterns:
    if pattern in html:
        # Don't remove if it's inside the IIFE (our new code)
        idx = html.find(pattern)
        # Only remove if before the SAVING GUIDE IIFE
        sg_iife_idx = html.find('░░  SAVING GUIDE — HYBRID BOT')
        if sg_iife_idx == -1 or idx < sg_iife_idx:
            # Find line and remove it
            line_start = html.rfind('\n', 0, idx) + 1
            line_end   = html.find('\n', idx)
            if line_end != -1:
                old_line = html[line_start:line_end+1]
                html = html.replace(old_line, '', 1)
                print(f"Removed dead code: {pattern[:40]}")

# ── SAVE ──────────────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Done! Final size: {len(html):,} bytes / {html.count(chr(10)):,} lines")
