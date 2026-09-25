# -*- coding: utf-8 -*-
"""
Mobile-First Dashboard HTML Template for Vault.fi / SaveMoneyManually
"""

DASHBOARD_HTML = """  <!-- ============================================================ -->
  <!-- 2. FULL AUTONOMOUS MOBILE-FIRST FINTECH DASHBOARD VIEW       -->
  <!-- ============================================================ -->
  <div id="dashboard-view" class="dissolve-enter hidden relative z-10 min-h-screen flex flex-col w-full pb-28 md:pb-8">

    <!-- Ambient Iridescent Glass Mesh Light Orbs -->
    <div class="fixed top-12 left-6 sm:left-10 w-72 sm:w-96 h-72 sm:h-96 rounded-full bg-blue-500/12 blur-3xl pointer-events-none z-0"></div>
    <div class="fixed top-1/3 right-6 sm:right-10 w-80 sm:w-[420px] h-80 sm:h-[420px] rounded-full bg-indigo-500/10 blur-3xl pointer-events-none z-0"></div>
    <div class="fixed bottom-24 left-1/4 w-72 sm:w-[380px] h-72 sm:h-[380px] rounded-full bg-emerald-500/10 blur-3xl pointer-events-none z-0"></div>
    <div class="fixed top-2/3 right-1/4 w-60 sm:w-80 h-60 sm:h-80 rounded-full bg-rose-500/8 blur-3xl pointer-events-none z-0"></div>

    <!-- ── STICKY GLASS NAVIGATION HEADER ───────────────────── -->
    <header class="w-full bg-white/85 backdrop-blur-2xl border-b border-white/90 sticky top-0 z-30 transition-all shadow-[0_4px_20px_-4px_rgba(15,23,42,0.05)]">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-2.5 sm:py-3 flex items-center justify-between gap-3 relative z-10">

        <!-- Brand: Vault.fi | SaveMoneyManually strictly preserved -->
        <a href="#" class="flex items-center gap-2.5 no-underline flex-shrink-0">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-cobalt to-blue-700 flex items-center justify-center shadow-md shadow-blue-500/25 flex-shrink-0">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
          </div>
          <div class="leading-none">
            <div class="text-sm sm:text-base font-extrabold text-charcoal tracking-tight flex items-center gap-1.5">
              <span>Vault.fi</span>
              <span class="text-slate-300 font-normal">|</span>
              <span class="text-cobalt text-xs sm:text-sm font-bold">SaveMoneyManually</span>
            </div>
            <div class="text-[9px] font-mono text-coolslate tracking-widest uppercase mt-0.5">Discipline Ledger &bull; 100% Offline Math</div>
          </div>
        </a>

        <!-- Center status indicators & actions (Desktop) -->
        <div class="hidden lg:flex items-center gap-3">
          <div class="flex items-center gap-2 bg-emerald-50/80 backdrop-blur-md border border-emerald-200/70 px-3 py-1 rounded-full shadow-xs">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span class="text-[11px] font-bold text-emerald-700 font-mono tracking-wide">MOBILE-FIRST ENGINE</span>
          </div>
          
          <button id="btn-header-disclaimer" class="flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-semibold text-coolslate hover:text-cobalt bg-white/80 hover:bg-white backdrop-blur-md border border-slate-200/80 shadow-xs transition-all cursor-pointer" type="button" title="View Privacy & Custody Disclosure">
            <span>🛡️</span><span>Zero Bank Connection</span>
          </button>

          <button class="btn-replay-vault flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-semibold text-coolslate hover:text-cobalt bg-white/80 hover:bg-white backdrop-blur-md border border-slate-200/80 shadow-xs transition-all cursor-pointer" type="button" title="Replay Cinematic Opening Sequence">
            <span>🎬</span><span>Intro</span>
          </button>
        </div>

        <!-- Right: user capsule + sign-out -->
        <div class="flex items-center gap-2">
          <div class="flex items-center gap-2 bg-white/70 backdrop-blur-md border border-white/90 py-1 px-2.5 rounded-xl shadow-xs">
            <div id="dash-user-avatar" class="w-7 h-7 rounded-full bg-blue-100 text-cobalt font-bold text-xs flex items-center justify-center overflow-hidden flex-shrink-0">U</div>
            <div class="text-left hidden sm:block">
              <div id="dash-user-name" class="text-xs font-bold text-charcoal leading-tight truncate max-w-[120px]">Saver</div>
              <div class="text-[9px] font-mono text-coolslate">₹520/hr baseline</div>
            </div>
          </div>
          <button id="btn-dash-signout" class="text-xs font-semibold text-coolslate hover:text-crimson bg-white/80 hover:bg-rose-50/80 backdrop-blur-md border border-slate-200/80 hover:border-rose-200 py-1.5 px-3 rounded-xl transition-all cursor-pointer shadow-xs min-h-[36px]" type="button">Sign Out</button>
        </div>
      </div>
    </header>

    <!-- ── TRANSPARENT LEDGER DISCLAIMER BANNER ────────────────── -->
    <div class="w-full bg-blue-50/60 backdrop-blur-md border-b border-blue-100/70 px-4 sm:px-6 py-2.5 relative z-10">
      <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2 text-center sm:text-left">
        <div class="flex items-center gap-2 text-[11px] font-medium text-slate-700 leading-snug">
          <span class="text-cobalt flex-shrink-0 text-sm">🛡️</span>
          <span><strong>Vault.fi is a personal ledger tool.</strong> We never connect to your bank accounts or collect real money. You save your own cash or UPI manually; this portal purely tracks your discipline and math.</span>
        </div>
        <button id="btn-banner-disclaimer" class="text-[11px] font-bold text-cobalt hover:underline flex-shrink-0 cursor-pointer whitespace-nowrap" type="button">
          Privacy Policy &amp; Security &rarr;
        </button>
      </div>
    </div>

    <!-- ── MAIN DASHBOARD SURFACE (MOBILE: SINGLE-COLUMN FLOW, DESKTOP: GRID) ── -->
    <main class="max-w-6xl mx-auto px-4 py-5 sm:px-6 sm:py-8 flex-1 w-full flex flex-col gap-6 md:gap-8 relative z-10">

      <!-- ───────────────────────────────────────────────────── -->
      <!-- SECTION 1 ─ HERO NET CAPITAL & TOUCH ACTIONS             -->
      <!-- ───────────────────────────────────────────────────── -->
      <section class="metallic-card p-5 sm:p-7 relative overflow-hidden" aria-label="Total Capital Overview">
        <div class="absolute -right-20 -top-20 w-72 h-72 rounded-full pointer-events-none" style="background:radial-gradient(circle,rgba(37,99,235,0.08) 0%,transparent 70%);"></div>
        <div class="absolute -left-10 -bottom-10 w-40 h-40 rounded-full pointer-events-none" style="background:radial-gradient(circle,rgba(225,29,72,0.05) 0%,transparent 70%);"></div>

        <div class="flex flex-col lg:flex-row lg:items-start justify-between gap-6 relative z-10">
          <!-- Left: Big Monospace Number & Quick Actions -->
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-2">
              <div class="w-1.5 h-4 sm:h-5 rounded-full bg-cobalt"></div>
              <span class="font-mono text-[10px] sm:text-[11px] font-bold uppercase tracking-widest text-coolslate">Total Net Capital Stashed</span>
            </div>
            <div id="metric-total-capital" class="font-mono text-4xl sm:text-6xl font-extrabold text-charcoal tracking-tight leading-none">&#8377;0</div>
            <p class="text-xs text-coolslate mt-2.5 max-w-md leading-relaxed">Log manual savings and emergency withdrawals. Balance, round-ups, and pacing adjust instantaneously.</p>

            <!-- Desktop action buttons (Hidden on small mobile, handled by sticky bar) -->
            <div class="hidden sm:flex flex-wrap items-center gap-2.5 mt-5">
              <button id="btn-quick-add-savings" class="btn-primary-metallic text-xs min-h-[48px] py-2.5 px-5 cursor-pointer shadow-md shadow-blue-500/20" type="button">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
                <span>+ Add Savings</span>
              </button>
              <button id="btn-quick-withdrawal" class="btn-danger-metallic text-xs min-h-[48px] py-2.5 px-4 cursor-pointer shadow-md shadow-rose-500/15" type="button">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20 12H4"/></svg>
                <span>- Record Withdrawal</span>
              </button>
              <button id="btn-quick-new-vault" class="btn-secondary-metallic text-xs min-h-[48px] py-2.5 px-4 cursor-pointer" type="button">
                <svg class="w-4 h-4 text-cobalt" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
                <span>🎯 New Goal Vault</span>
              </button>
            </div>
          </div>

          <!-- Right: 3 Glass KPI Tiles (Single-column on mobile, 3-col on desktop) -->
          <div class="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-1 xl:grid-cols-3 gap-3 lg:min-w-[340px]">
            <!-- KPI 1: Discipline Streak with Animated Flame Icon -->
            <div class="glass-inner-tile p-3.5 sm:p-4">
              <div class="flex items-center justify-between mb-2">
                <div class="w-8 h-8 rounded-xl bg-amber-50/90 border border-amber-200/80 flex items-center justify-center text-sm shadow-xs">
                  <span class="inline-block animate-pulse">🔥</span>
                </div>
                <span class="text-[9px] font-mono font-bold text-coolslate uppercase tracking-widest">Discipline Streak</span>
              </div>
              <div class="flex items-baseline gap-1.5">
                <span id="metric-streak-count" class="font-mono text-2xl font-extrabold text-charcoal">0 Days</span>
                <span class="text-xs text-amber-500 font-bold animate-bounce">🔥</span>
              </div>
              <div class="text-[10px] text-coolslate mt-0.5">Consecutive active log-ins</div>
            </div>

            <!-- KPI 2: Active Goals -->
            <div class="glass-inner-tile p-3.5 sm:p-4">
              <div class="flex items-center justify-between mb-2">
                <div class="w-8 h-8 rounded-xl bg-emerald-50/90 border border-emerald-200/80 flex items-center justify-center text-emerald-600 shadow-xs">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6l4 2"/></svg>
                </div>
                <span class="text-[9px] font-mono font-bold text-coolslate uppercase tracking-widest">Active Goals</span>
              </div>
              <div id="metric-vaults-count" class="font-mono text-2xl font-extrabold text-charcoal">0</div>
              <div class="text-[10px] text-coolslate mt-0.5">Flexi-cadence targets</div>
            </div>

            <!-- KPI 3: Monthly Net Saved -->
            <div class="glass-inner-tile p-3.5 sm:p-4">
              <div class="flex items-center justify-between mb-2">
                <div class="w-8 h-8 rounded-xl bg-blue-50/90 border border-blue-200/80 flex items-center justify-center text-cobalt shadow-xs">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/></svg>
                </div>
                <span class="text-[9px] font-mono font-bold text-coolslate uppercase tracking-widest">This Month</span>
              </div>
              <div id="metric-month-saved" class="font-mono text-2xl font-extrabold text-charcoal">&#8377;0</div>
              <div class="text-[10px] text-coolslate mt-0.5">Net disciplined stash</div>
            </div>
          </div>
        </div>
      </section>

      <!-- ───────────────────────────────────────────────────── -->
      <!-- SECTION 2 ─ ANTIGRAVITY AI PACING & DYNAMIC SUGGESTIONS  -->
      <!-- ───────────────────────────────────────────────────── -->
      <section class="metallic-card p-5 sm:p-7 relative overflow-hidden" aria-label="AI Dynamic Pacing Engine">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-white/60">
          <div class="flex items-center gap-3">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-md shadow-blue-500/25 flex-shrink-0">
              <span class="text-sm">✨</span>
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-sm sm:text-base font-extrabold text-charcoal tracking-tight">Antigravity AI Pacing &amp; Suggestions</h3>
                <span class="font-mono text-[9px] font-bold text-cobalt bg-blue-50/80 border border-blue-200/80 px-2 py-0.5 rounded-full uppercase tracking-wider">Predictive</span>
              </div>
              <p class="text-[11px] text-coolslate">Dynamic quota alerts comparing velocity against target deadlines</p>
            </div>
          </div>

          <!-- Goal selector for AI focus -->
          <div class="flex items-center gap-2 w-full sm:w-auto">
            <label for="ai-goal-selector" class="text-xs font-semibold text-coolslate whitespace-nowrap">Focus:</label>
            <select id="ai-goal-selector" class="input-metallic text-xs py-2 px-3 font-semibold bg-white/80 border border-slate-200/80 rounded-xl cursor-pointer w-full sm:w-auto">
              <!-- Dynamically populated -->
            </select>
          </div>
        </div>

        <!-- Dynamic Alert Banner (On Track / Behind Schedule) -->
        <div id="ai-pacing-banner" class="mt-4 p-4 rounded-2xl pacing-banner-optimal transition-all duration-300">
          <div class="flex items-start gap-3">
            <span id="ai-pacing-icon" class="text-xl flex-shrink-0">⚡</span>
            <div class="flex-1">
              <div id="ai-pacing-headline" class="font-extrabold text-sm text-charcoal leading-snug">Pacing Optimal: You are projected to hit your goal on schedule.</div>
              <div id="ai-pacing-detail" class="text-xs text-coolslate mt-1 leading-relaxed">
                Maintain your daily quota to hit your deadline right on schedule.
              </div>
            </div>
          </div>
        </div>

        <!-- 4-Metric Pacing Telemetry Grid -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5 sm:gap-3 mt-4">
          <div class="glass-inner-tile p-3 sm:p-3.5">
            <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate uppercase tracking-wider">Required Daily Quota</div>
            <div id="ai-quota-daily" class="font-mono text-base sm:text-lg font-extrabold text-cobalt mt-1">&#8377;0 / day</div>
            <div class="text-[9px] sm:text-[10px] text-coolslate mt-0.5">Calculated by deadline</div>
          </div>

          <div class="glass-inner-tile p-3 sm:p-3.5">
            <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate uppercase tracking-wider">Monthly Run-Rate</div>
            <div id="ai-quota-monthly" class="font-mono text-base sm:text-lg font-extrabold text-charcoal mt-1">&#8377;0 / mo</div>
            <div class="text-[9px] sm:text-[10px] text-coolslate mt-0.5">Monthly savings quota</div>
          </div>

          <div class="glass-inner-tile p-3 sm:p-3.5">
            <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate uppercase tracking-wider">Days Remaining</div>
            <div id="ai-days-remaining" class="font-mono text-base sm:text-lg font-extrabold text-charcoal mt-1">0 Days</div>
            <div id="ai-deadline-date" class="text-[9px] sm:text-[10px] text-coolslate mt-0.5 truncate">Target: --</div>
          </div>

          <div class="glass-inner-tile p-3 sm:p-3.5">
            <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate uppercase tracking-wider">Projected ETA</div>
            <div id="ai-projected-eta" class="font-mono text-base sm:text-lg font-extrabold text-emerald-600 mt-1">--</div>
            <div id="ai-eta-diff" class="text-[9px] sm:text-[10px] text-emerald-600 font-medium mt-0.5">At current velocity</div>
          </div>
        </div>
      </section>

      <!-- ───────────────────────────────────────────────────── -->
      <!-- SECTION 3 ─ CUSTOM GOAL ENGINE (FLEXI-CADENCE)           -->
      <!-- ───────────────────────────────────────────────────── -->
      <section aria-label="Smart Goal Vaults">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3.5">
          <div class="flex items-center gap-2.5">
            <div class="w-1.5 h-4 sm:h-5 rounded-full bg-cobalt"></div>
            <div>
              <h2 class="text-sm sm:text-base font-extrabold text-charcoal tracking-tight">Active Smart Goal Vaults</h2>
              <p class="text-[11px] text-coolslate">Flexi-cadence targets (Daily, Monthly, Yearly) with live quota calculations</p>
            </div>
          </div>
          <button id="btn-grid-new-vault" class="btn-primary-metallic text-xs min-h-[44px] py-2 px-4 cursor-pointer w-full sm:w-auto shadow-sm" type="button">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
            <span>+ Create Goal Vault</span>
          </button>
        </div>

        <!-- Dynamic Vault Cards Grid -->
        <div id="vaults-grid-container" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5 sm:gap-4"></div>

        <!-- Empty State Container -->
        <div id="vaults-empty-state" class="metallic-card p-8 sm:p-12 flex flex-col items-center justify-center text-center gap-4 hidden">
          <div class="w-14 h-14 rounded-2xl bg-blue-50/90 border border-blue-100 flex items-center justify-center shadow-xs">
            <svg class="w-6 h-6 text-cobalt" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
          </div>
          <div>
            <div class="font-bold text-charcoal text-sm sm:text-base">No active vaults yet</div>
            <div class="text-xs text-coolslate mt-1 max-w-xs leading-relaxed">Create your first goal target (e.g., "Emergency Fund", "New Bike"). The flexi-cadence engine calculates exact daily or monthly quotas.</div>
          </div>
          <button id="btn-empty-new-vault" class="btn-primary-metallic text-xs min-h-[48px] py-2.5 px-6 cursor-pointer shadow-md shadow-blue-500/20" type="button">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
            <span>Create First Goal Vault</span>
          </button>
        </div>
      </section>

      <!-- ───────────────────────────────────────────────────── -->
      <!-- SECTION 4 ─ INTERACTIVE SAVINGS CALENDAR & STREAK MATRIX -->
      <!-- ───────────────────────────────────────────────────── -->
      <section class="metallic-card p-4 sm:p-6" aria-label="Interactive Savings Calendar">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-white/60">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-xl bg-blue-50/90 border border-blue-100 flex items-center justify-center text-sm shadow-xs">
              <span>📅</span>
            </div>
            <div>
              <h3 class="font-extrabold text-charcoal text-xs sm:text-sm">Interactive Savings Calendar &amp; Streak</h3>
              <p class="text-[10px] sm:text-[11px] text-coolslate">Days with logged savings marked with glowing Cobalt Blue badges</p>
            </div>
          </div>

          <!-- Calendar month navigation -->
          <div class="flex items-center justify-between sm:justify-end gap-2">
            <button id="cal-prev-btn" class="w-8 h-8 rounded-lg border border-slate-200/80 bg-white/70 hover:bg-white flex items-center justify-center text-charcoal font-bold transition-colors cursor-pointer shadow-xs min-h-[36px]" type="button" aria-label="Previous Month">&lsaquo;</button>
            <div id="cal-month-title" class="font-mono font-bold text-xs text-charcoal min-w-[120px] text-center uppercase tracking-wider">September 2026</div>
            <button id="cal-next-btn" class="w-8 h-8 rounded-lg border border-slate-200/80 bg-white/70 hover:bg-white flex items-center justify-center text-charcoal font-bold transition-colors cursor-pointer shadow-xs min-h-[36px]" type="button" aria-label="Next Month">&rsaquo;</button>
            <button id="cal-today-btn" class="text-[10px] font-bold text-cobalt px-2.5 py-1.5 rounded-lg border border-blue-200/80 bg-blue-50/80 hover:bg-blue-100/90 transition-colors cursor-pointer shadow-xs min-h-[36px]" type="button">Today</button>
          </div>
        </div>

        <!-- 7-Column Day Names Header (strictly fits on 360px) -->
        <div class="grid grid-cols-7 gap-1 text-center mt-3 mb-1.5">
          <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate">SUN</div>
          <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate">MON</div>
          <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate">TUE</div>
          <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate">WED</div>
          <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate">THU</div>
          <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate">FRI</div>
          <div class="text-[9px] sm:text-[10px] font-mono font-bold text-coolslate">SAT</div>
        </div>

        <!-- Calendar Day Cells Grid -->
        <div id="calendar-grid" class="grid grid-cols-7 gap-1 sm:gap-1.5 min-h-[190px]">
          <!-- Populated dynamically by JS -->
        </div>

        <!-- Calendar Summary Footer -->
        <div class="mt-3.5 pt-3 border-t border-white/60 flex flex-col sm:flex-row items-center justify-between gap-2.5 text-xs text-coolslate font-medium">
          <div class="flex items-center gap-3 text-[11px]">
            <div class="flex items-center gap-1.5">
              <span class="w-2.5 h-2.5 rounded-full bg-cobalt inline-block shadow-xs"></span>
              <span>Saved Day</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-2.5 h-2.5 rounded-full border border-slate-300 bg-white/80 inline-block shadow-xs"></span>
              <span>Inactive</span>
            </div>
          </div>
          <div class="font-mono text-[10px] sm:text-[11px] text-slate-600">
            Monthly Discipline Rate: <strong id="cal-discipline-rate" class="text-cobalt font-bold">0%</strong> &bull; Total Days: <strong id="cal-month-days-count" class="text-charcoal font-bold">0</strong>
          </div>
        </div>
      </section>

      <!-- ───────────────────────────────────────────────────── -->
      <!-- SECTION 5 ─ MOBILE-OPTIMIZED LEDGER HISTORY               -->
      <!-- ───────────────────────────────────────────────────── -->
      <section class="metallic-card p-4 sm:p-6" aria-label="Transaction Ledger">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-white/60">
          <div class="flex items-center gap-2.5">
            <div class="w-1.5 h-4 sm:h-5 rounded-full bg-cobalt"></div>
            <div>
              <h3 class="font-extrabold text-charcoal text-xs sm:text-base">Ledger History &amp; Audit Trail</h3>
              <p class="text-[10px] sm:text-[11px] text-coolslate">Mobile-first stacked cards with inline edit &amp; deletion</p>
            </div>
          </div>

          <!-- Filter buttons -->
          <div class="flex items-center gap-1 bg-white/60 backdrop-blur-md p-1 rounded-xl border border-white/80 shadow-xs self-start sm:self-auto">
            <button id="filter-ledger-all" class="text-[11px] font-bold px-3 py-1 rounded-lg bg-white text-charcoal shadow-xs transition-all cursor-pointer min-h-[32px]" type="button">All</button>
            <button id="filter-ledger-add" class="text-[11px] font-bold px-3 py-1 rounded-lg text-coolslate hover:text-charcoal transition-all cursor-pointer min-h-[32px]" type="button">+ Deposits</button>
            <button id="filter-ledger-minus" class="text-[11px] font-bold px-3 py-1 rounded-lg text-coolslate hover:text-charcoal transition-all cursor-pointer min-h-[32px]" type="button">- Withdrawals</button>
          </div>
        </div>

        <!-- 1. MOBILE RESPONSIVE STACKED CARDS (md:hidden) — Zero Clipping / Horizontal Scroll -->
        <div id="ledger-mobile-cards" class="mt-3.5 flex flex-col gap-2.5 md:hidden">
          <!-- Rendered dynamically by JS -->
        </div>

        <!-- 2. DESKTOP DATA TABLE (hidden md:block) -->
        <div class="mt-4 overflow-x-auto hidden md:block">
          <table class="w-full text-left border-collapse" id="ledger-table">
            <thead>
              <tr class="border-b border-white/80 text-[10px] font-mono font-bold text-coolslate uppercase tracking-wider">
                <th class="py-2.5 px-3">Date &amp; Time</th>
                <th class="py-2.5 px-3">Goal Vault</th>
                <th class="py-2.5 px-3">Type</th>
                <th class="py-2.5 px-3">Note / Reason</th>
                <th class="py-2.5 px-3 text-right">Amount</th>
                <th class="py-2.5 px-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody id="ledger-table-body" class="divide-y divide-white/60 text-xs">
              <!-- Dynamically populated by JS -->
            </tbody>
          </table>
        </div>

        <!-- Empty state -->
        <div id="ledger-empty-state" class="py-8 sm:py-12 flex flex-col items-center justify-center text-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-blue-50/90 border border-blue-100 flex items-center justify-center text-cobalt shadow-xs">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
          </div>
          <div class="text-xs text-coolslate font-medium leading-relaxed">
            No entries recorded in your ledger yet.<br/>Use <strong>[+ Add Saved]</strong> or <strong>[- Withdraw]</strong> below to record your discipline.
          </div>
        </div>
      </section>

      <!-- ───────────────────────────────────────────────────── -->
      <!-- SECTION 6 ─ IMPULSE COOLDOWN CHAMBER                     -->
      <!-- ───────────────────────────────────────────────────── -->
      <section class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-5" aria-label="Impulse Cooldown Chamber">
        <!-- Left: Calculator -->
        <div class="metallic-card p-4 sm:p-6">
          <div class="flex items-center gap-2.5 mb-3.5">
            <div class="w-8 h-8 rounded-xl bg-rose-50/90 border border-rose-100 flex items-center justify-center text-crimson flex-shrink-0 shadow-xs">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3"/></svg>
            </div>
            <div>
              <div class="flex items-center gap-2">
                <div class="w-1 h-3.5 rounded-full bg-crimson"></div>
                <h3 class="font-bold text-charcoal text-xs sm:text-sm">Impulse Cooldown Chamber</h3>
              </div>
              <p class="text-[10px] sm:text-[11px] text-coolslate">Convert impulse prices into real life-work-hours before buying</p>
            </div>
          </div>

          <form id="cooldown-calc-form" class="space-y-3.5" novalidate autocomplete="off">
            <div>
              <label class="block text-xs font-bold text-charcoal mb-1" for="cd-item-name">Item you want to buy</label>
              <input type="text" id="cd-item-name" class="input-metallic text-sm" placeholder="e.g. Noise Cancelling Headphones, Sneakers…" required />
            </div>
            <div>
              <label class="block text-xs font-bold text-charcoal mb-1" for="cd-item-price">Price Tag (&#8377;)</label>
              <div class="amount-prefix-wrap">
                <span class="prefix-symbol">&#8377;</span>
                <input type="number" id="cd-item-price" class="input-metallic font-mono text-sm" placeholder="15,000" min="10" required />
              </div>
            </div>

            <!-- Work-hour readout panel -->
            <div class="rounded-xl border border-white/80 overflow-hidden bg-white/70 backdrop-blur-md shadow-xs">
              <div class="px-3.5 py-2.5 border-b border-white/60">
                <div class="text-[10px] font-mono font-bold text-coolslate uppercase tracking-widest">Required Labor Hours at &#8377;520/hr</div>
              </div>
              <div class="px-3.5 py-2.5 flex items-end justify-between">
                <div>
                  <div id="cd-hours-output" class="font-mono text-2xl sm:text-3xl font-extrabold text-cobalt leading-none">0.0</div>
                  <div class="text-[10px] text-coolslate mt-0.5">work hours</div>
                </div>
                <div class="text-right">
                  <div id="cd-days-output" class="text-xs text-coolslate font-medium">Enter price to calculate</div>
                  <div id="cd-weeks-output" class="text-[10px] text-coolslate mt-0.5"></div>
                </div>
              </div>
            </div>

            <button type="submit" id="btn-cooldown-submit" class="btn-primary-metallic w-full min-h-[48px] py-2.5 text-xs font-bold cursor-pointer flex items-center justify-center gap-2 shadow-sm">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              <span>Lock in 48-Hour Cooldown</span>
            </button>
          </form>
        </div>

        <!-- Right: Active cooldown timers -->
        <div class="metallic-card p-4 sm:p-6 flex flex-col">
          <div class="flex items-center justify-between mb-1">
            <div class="flex items-center gap-2">
              <div class="w-1 h-3.5 rounded-full bg-crimson"></div>
              <h3 class="font-bold text-charcoal text-xs sm:text-sm">Active Cooldown Locks</h3>
            </div>
            <span class="font-mono text-[9px] sm:text-[10px] font-bold text-coolslate bg-white/70 px-2 py-0.5 rounded-full border border-slate-200/80 shadow-xs">48h PROTOCOL</span>
          </div>
          <p class="text-[10px] sm:text-[11px] text-coolslate mb-3.5">Over 78% of impulse desires fade within 48 hours. When expired, stash the saved money into your vault.</p>

          <div id="cooldown-active-items" class="space-y-2.5 flex-1"></div>

          <!-- Empty state -->
          <div id="cooldown-empty-state" class="flex-1 flex flex-col items-center justify-center text-center gap-3 py-6">
            <div class="w-10 h-10 rounded-2xl bg-white/80 border border-slate-200/80 flex items-center justify-center shadow-xs">
              <svg class="w-5 h-5 text-coolslate" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
            </div>
            <div class="text-xs text-coolslate font-medium">No active cooldowns.<br/>Lock an impulse spend using the calculator.</div>
          </div>

          <div class="mt-3.5 pt-2.5 border-t border-white/60 flex items-center gap-2 text-[10px] text-coolslate">
            <svg class="w-3.5 h-3.5 text-emerald-500 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
            <span>Personal Ledger Guarantee: Funds remain 100% under your private possession.</span>
          </div>
        </div>
      </section>

    </main>

    <!-- ── STICKY BOTTOM FLOATING ACTION BAR (MOBILE ONLY: md:hidden) ── -->
    <div id="mobile-floating-bar" class="fixed bottom-0 inset-x-0 z-40 p-3 bg-white/90 backdrop-blur-2xl border-t border-slate-200/90 shadow-[0_-10px_30px_rgba(15,23,42,0.12)] md:hidden flex items-center gap-2.5 pb-[max(0.75rem,env(safe-area-inset-bottom))]">
      <button id="btn-mobile-add" class="flex-1 btn-primary-metallic min-h-[48px] text-xs font-bold flex items-center justify-center gap-2 cursor-pointer shadow-md shadow-blue-500/25 active:scale-[0.98] transition-transform" type="button">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
        <span>+ Add Saved</span>
      </button>
      <button id="btn-mobile-withdraw" class="flex-1 btn-danger-metallic min-h-[48px] text-xs font-bold flex items-center justify-center gap-2 cursor-pointer shadow-md shadow-rose-500/20 active:scale-[0.98] transition-transform" type="button">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20 12H4"/></svg>
        <span>- Withdraw</span>
      </button>
    </div>

    <!-- ── DASHBOARD STATUS FOOTER ────────────────────────────── -->
    <footer class="w-full border-t border-white/70 mt-6 relative z-10" style="background:rgba(255,255,255,0.75); backdrop-filter:blur(20px);">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 py-5 flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left">
        <div class="flex flex-wrap items-center justify-center sm:justify-start gap-3 font-mono text-[10px] text-coolslate">
          <div class="flex items-center gap-1.5">
            <div class="w-1.5 h-1.5 rounded-full bg-emerald-500"></div>
            <span>Firebase Secure Auth</span>
          </div>
          <div class="w-px h-3 bg-slate-300"></div>
          <div class="flex items-center gap-1.5">
            <svg class="w-2.5 h-2.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
            <span>Zero Banking Link</span>
          </div>
          <div class="w-px h-3 bg-slate-300"></div>
          <button id="btn-footer-disclaimer" class="text-cobalt font-bold hover:underline cursor-pointer" type="button">Privacy Policy &amp; Disclaimer</button>
        </div>
        <div class="font-mono text-[10px] text-slate-400">Vault.fi &bull; SaveMoneyManually &bull; Manual Savings &amp; Discipline Ledger</div>
      </div>
    </footer>

  </div>

  <!-- ============================================================ -->
  <!-- MOBILE BOTTOM SHEET MODALS (NATIVE SLIDE-UP ON MOBILE, DIALOG ON DESKTOP) -->
  <!-- ============================================================ -->

  <!-- 1. MODAL: CREATE GOAL VAULT (FLEXI-CADENCE & LIVE MATH) -->
  <div class="modal-overlay" id="modal-create-goal" role="dialog" aria-modal="true" aria-labelledby="modal-goal-title">
    <div class="modal-dialog">
      <!-- Native Mobile Bottom Sheet Drag Handle Bar -->
      <div class="bottom-sheet-handle"></div>

      <div class="flex items-center justify-between px-5 pt-4 pb-3 border-b border-white/60">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-700 flex items-center justify-center shadow-md shadow-blue-500/25 text-white flex-shrink-0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
          </div>
          <div>
            <h3 id="modal-goal-title" class="font-bold text-charcoal text-sm leading-tight">Create Smart Goal Vault</h3>
            <p class="text-[11px] text-coolslate">Target, deadline &amp; flexi-cadence live math</p>
          </div>
        </div>
        <button class="w-8 h-8 rounded-full bg-white/80 hover:bg-white flex items-center justify-center text-coolslate hover:text-charcoal modal-close cursor-pointer transition-colors shadow-xs" type="button" aria-label="Close">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <form id="form-create-goal" class="px-5 py-4 space-y-3.5" novalidate autocomplete="off">
        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="goal-input-name">Goal Name</label>
          <input type="text" id="goal-input-name" class="input-metallic text-base sm:text-sm" placeholder="e.g. Emergency Fund, New Bike, Gold Reserve" required />
          <p id="goal-err-name" class="text-[11px] text-rose-600 font-medium mt-1 hidden">Please provide a goal name.</p>
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="goal-input-amount">Target Amount (&#8377;)</label>
          <div class="amount-prefix-wrap">
            <span class="prefix-symbol">&#8377;</span>
            <input type="number" id="goal-input-amount" class="input-metallic font-mono text-base sm:text-sm" placeholder="50,000" min="100" required />
          </div>
          <p id="goal-err-amount" class="text-[11px] text-rose-600 font-medium mt-1 hidden">Please enter a valid target amount.</p>
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="goal-input-deadline">Target Date</label>
          <input type="date" id="goal-input-deadline" class="input-metallic text-base sm:text-sm font-mono" required />
          <p id="goal-err-deadline" class="text-[11px] text-rose-600 font-medium mt-1 hidden">Please select a deadline in the future.</p>
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1.5">Preferred Cadence Selector</label>
          <div class="grid grid-cols-3 gap-2">
            <button type="button" class="btn-cadence-toggle min-h-[48px] py-2 px-3 text-xs font-bold rounded-xl border border-cobalt bg-blue-50/90 text-cobalt transition-all cursor-pointer shadow-xs" data-cadence="DAILY">Daily</button>
            <button type="button" class="btn-cadence-toggle min-h-[48px] py-2 px-3 text-xs font-bold rounded-xl border border-slate-200/80 bg-white/70 text-coolslate transition-all cursor-pointer shadow-xs" data-cadence="MONTHLY">Monthly</button>
            <button type="button" class="btn-cadence-toggle min-h-[48px] py-2 px-3 text-xs font-bold rounded-xl border border-slate-200/80 bg-white/70 text-coolslate transition-all cursor-pointer shadow-xs" data-cadence="YEARLY">Yearly</button>
          </div>
        </div>

        <!-- Dynamic Cadence Math Readout (Formula: Remaining / Days) -->
        <div id="goal-math-readout" class="rounded-xl border border-blue-200/80 p-3 bg-blue-50/70 backdrop-blur-md shadow-xs">
          <div class="text-[10px] font-mono font-bold text-cobalt uppercase tracking-wider mb-0.5">⚡ Dynamic Cadence Math</div>
          <div id="goal-math-text" class="text-xs font-medium text-slate-800 leading-relaxed">
            Enter amount and target date to compute your required saving quota: Remaining / Days.
          </div>
        </div>

        <div class="border-t border-white/60 pt-3 flex items-center justify-between gap-2.5">
          <button type="button" class="btn-secondary-metallic min-h-[48px] text-xs modal-close flex-1">Cancel</button>
          <button type="submit" id="btn-create-goal-submit" class="btn-primary-metallic min-h-[48px] text-xs flex-[2] flex items-center justify-center gap-2 shadow-sm">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
            <span>Confirm &amp; Lock Vault</span>
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- 2. MODAL: ADD SAVINGS (+ MANUAL MONEY LOG) -->
  <div class="modal-overlay" id="modal-add-savings" role="dialog" aria-modal="true" aria-labelledby="modal-add-title">
    <div class="modal-dialog">
      <!-- Native Mobile Bottom Sheet Drag Handle Bar -->
      <div class="bottom-sheet-handle"></div>

      <div class="flex items-center justify-between px-5 pt-4 pb-3 border-b border-white/60">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-blue-500 to-blue-700 flex items-center justify-center shadow-md shadow-blue-500/25 text-white flex-shrink-0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/></svg>
          </div>
          <div>
            <h3 id="modal-add-title" class="font-bold text-charcoal text-sm leading-tight">Add Savings to Vault</h3>
            <p class="text-[11px] text-coolslate">Log cash or UPI money saved manually today</p>
          </div>
        </div>
        <button class="w-8 h-8 rounded-full bg-white/80 hover:bg-white flex items-center justify-center text-coolslate hover:text-charcoal modal-close cursor-pointer transition-colors shadow-xs" type="button" aria-label="Close">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <form id="form-add-savings" class="px-5 py-4 space-y-3.5" novalidate autocomplete="off">
        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="add-savings-vault-input">
            Target Goal Vault
            <span class="font-normal text-coolslate ml-1">(type name or choose chip)</span>
          </label>
          <div class="relative">
            <div class="chip-input-wrapper" id="add-chips-wrapper">
              <input type="text" id="add-savings-vault-input" placeholder="e.g. Emergency Fund, New Bike…" autocomplete="off" class="text-base sm:text-sm" />
            </div>
            <div class="chip-suggestions" id="add-chips-suggestions"></div>
          </div>
          <p id="add-err-vault" class="text-[11px] text-rose-600 font-medium mt-1 hidden">Please select or type a target vault.</p>
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="add-savings-amount">Deposit Amount (&#8377;)</label>
          <div class="amount-prefix-wrap">
            <span class="prefix-symbol">&#8377;</span>
            <input type="number" id="add-savings-amount" class="input-metallic font-mono text-base sm:text-sm" placeholder="500" min="1" required />
          </div>
          <p id="add-err-amount" class="text-[11px] text-rose-600 font-medium mt-1 hidden">Please enter an amount greater than &#8377;0.</p>
        </div>

        <!-- Quick-pick amount chips for rapid thumb tapping -->
        <div class="flex flex-wrap gap-2 pt-0.5">
          <span class="text-[11px] font-semibold text-coolslate self-center">Quick:</span>
          <button type="button" class="btn-add-preset text-xs font-bold px-3 py-1.5 rounded-full border border-slate-200/80 bg-white/70 hover:border-cobalt hover:text-cobalt transition-colors cursor-pointer shadow-xs min-h-[38px]" data-amount="150">&#8377;150</button>
          <button type="button" class="btn-add-preset text-xs font-bold px-3 py-1.5 rounded-full border border-slate-200/80 bg-white/70 hover:border-cobalt hover:text-cobalt transition-colors cursor-pointer shadow-xs min-h-[38px]" data-amount="500">&#8377;500</button>
          <button type="button" class="btn-add-preset text-xs font-bold px-3 py-1.5 rounded-full border border-slate-200/80 bg-white/70 hover:border-cobalt hover:text-cobalt transition-colors cursor-pointer shadow-xs min-h-[38px]" data-amount="1000">&#8377;1,000</button>
          <button type="button" class="btn-add-preset text-xs font-bold px-3 py-1.5 rounded-full border border-slate-200/80 bg-white/70 hover:border-cobalt hover:text-cobalt transition-colors cursor-pointer shadow-xs min-h-[38px]" data-amount="2000">&#8377;2,000</button>
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="add-savings-note">Note / Memo (Optional)</label>
          <input type="text" id="add-savings-note" class="input-metallic text-base sm:text-sm" placeholder="e.g. Daily coffee saving, UPI envelope" />
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="add-savings-date">Date</label>
          <input type="date" id="add-savings-date" class="input-metallic text-base sm:text-sm font-mono" required />
        </div>

        <div class="border-t border-white/60 pt-3 flex items-center justify-between gap-2.5">
          <button type="button" class="btn-secondary-metallic min-h-[48px] text-xs modal-close flex-1">Cancel</button>
          <button type="submit" id="btn-add-savings-submit" class="btn-primary-metallic min-h-[48px] text-xs flex-[2] flex items-center justify-center gap-2 shadow-sm">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
            <span>Confirm Stash</span>
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- 3. MODAL: RECORD WITHDRAWAL (- MANUAL MONEY LOG) -->
  <div class="modal-overlay" id="modal-record-withdrawal" role="dialog" aria-modal="true" aria-labelledby="modal-withdrawal-title">
    <div class="modal-dialog">
      <!-- Native Mobile Bottom Sheet Drag Handle Bar -->
      <div class="bottom-sheet-handle"></div>

      <div class="flex items-center justify-between px-5 pt-4 pb-3 border-b border-white/60">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-rose-500 to-rose-700 flex items-center justify-center shadow-md shadow-rose-500/25 text-white flex-shrink-0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20 12H4"/></svg>
          </div>
          <div>
            <h3 id="modal-withdrawal-title" class="font-bold text-charcoal text-sm leading-tight">Record Emergency Withdrawal</h3>
            <p class="text-[11px] text-coolslate">Log money taken out for an emergency</p>
          </div>
        </div>
        <button class="w-8 h-8 rounded-full bg-white/80 hover:bg-white flex items-center justify-center text-coolslate hover:text-charcoal modal-close cursor-pointer transition-colors shadow-xs" type="button" aria-label="Close">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <form id="form-record-withdrawal" class="px-5 py-4 space-y-3.5" novalidate autocomplete="off">
        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="withdrawal-vault-select">Source Goal Vault</label>
          <select id="withdrawal-vault-select" class="input-metallic text-base sm:text-sm font-semibold bg-white/80 border border-slate-200/80 rounded-xl cursor-pointer" required>
            <!-- Populated dynamically -->
          </select>
          <p id="withdrawal-err-vault" class="text-[11px] text-rose-600 font-medium mt-1 hidden">Please select a goal vault.</p>
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="withdrawal-amount">Withdrawal Amount (&#8377;)</label>
          <div class="amount-prefix-wrap">
            <span class="prefix-symbol">&#8377;</span>
            <input type="number" id="withdrawal-amount" class="input-metallic font-mono text-base sm:text-sm" placeholder="500" min="1" required />
          </div>
          <p id="withdrawal-err-amount" class="text-[11px] text-rose-600 font-medium mt-1 hidden">Please enter a valid amount.</p>
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="withdrawal-note">Emergency Reason / Memo</label>
          <input type="text" id="withdrawal-note" class="input-metallic text-base sm:text-sm" placeholder="e.g. Urgent bike repair, medical prescription" required />
          <p id="withdrawal-err-note" class="text-[11px] text-rose-600 font-medium mt-1 hidden">Please enter the emergency reason.</p>
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="withdrawal-date">Date</label>
          <input type="date" id="withdrawal-date" class="input-metallic text-base sm:text-sm font-mono" required />
        </div>

        <div class="border-t border-white/60 pt-3 flex items-center justify-between gap-2.5">
          <button type="button" class="btn-secondary-metallic min-h-[48px] text-xs modal-close flex-1">Cancel</button>
          <button type="submit" id="btn-withdrawal-submit" class="btn-danger-metallic min-h-[48px] text-xs flex-[2] flex items-center justify-center gap-2 shadow-sm">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M20 12H4"/></svg>
            <span>Record Withdrawal</span>
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- 4. MODAL: INLINE EDIT LEDGER ENTRY -->
  <div class="modal-overlay" id="modal-edit-ledger" role="dialog" aria-modal="true" aria-labelledby="modal-edit-title">
    <div class="modal-dialog">
      <!-- Native Mobile Bottom Sheet Drag Handle Bar -->
      <div class="bottom-sheet-handle"></div>

      <div class="flex items-center justify-between px-5 pt-4 pb-3 border-b border-white/60">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-blue-50/90 border border-blue-100 flex items-center justify-center text-charcoal shadow-xs flex-shrink-0">
            <span class="text-sm">✏️</span>
          </div>
          <div>
            <h3 id="modal-edit-title" class="font-bold text-charcoal text-sm leading-tight">Edit Transaction Entry</h3>
            <p class="text-[11px] text-coolslate">Correct amount, note, or date</p>
          </div>
        </div>
        <button class="w-8 h-8 rounded-full bg-white/80 hover:bg-white flex items-center justify-center text-coolslate hover:text-charcoal modal-close cursor-pointer transition-colors shadow-xs" type="button" aria-label="Close">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <form id="form-edit-ledger" class="px-5 py-4 space-y-3.5" novalidate autocomplete="off">
        <input type="hidden" id="edit-entry-id" />

        <div class="p-3 rounded-xl bg-white/70 border border-white/90 flex items-center justify-between text-xs backdrop-blur-md shadow-xs">
          <div>
            <span class="font-semibold text-coolslate">Goal Vault: </span>
            <span id="edit-entry-vault" class="font-bold text-charcoal">--</span>
          </div>
          <span id="edit-entry-type-badge" class="font-mono text-[10px] font-bold px-2 py-0.5 rounded-full">--</span>
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="edit-entry-amount">Amount (&#8377;)</label>
          <div class="amount-prefix-wrap">
            <span class="prefix-symbol">&#8377;</span>
            <input type="number" id="edit-entry-amount" class="input-metallic font-mono text-base sm:text-sm" min="1" required />
          </div>
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="edit-entry-note">Note / Reason</label>
          <input type="text" id="edit-entry-note" class="input-metallic text-base sm:text-sm" required />
        </div>

        <div>
          <label class="block text-xs font-bold text-charcoal mb-1" for="edit-entry-date">Date</label>
          <input type="date" id="edit-entry-date" class="input-metallic text-base sm:text-sm font-mono" required />
        </div>

        <div class="border-t border-white/60 pt-3 flex items-center justify-between gap-2.5">
          <button type="button" class="btn-secondary-metallic min-h-[48px] text-xs modal-close flex-1">Cancel</button>
          <button type="submit" id="btn-edit-ledger-submit" class="btn-primary-metallic min-h-[48px] text-xs flex-[2] flex items-center justify-center gap-2 shadow-sm">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
            <span>Save Changes</span>
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- 5. MODAL: DELETE LEDGER CONFIRMATION -->
  <div class="modal-overlay" id="modal-delete-ledger" role="dialog" aria-modal="true" aria-labelledby="modal-del-title">
    <div class="modal-dialog max-w-sm">
      <!-- Native Mobile Bottom Sheet Drag Handle Bar -->
      <div class="bottom-sheet-handle"></div>

      <div class="p-5 text-center space-y-3.5">
        <div class="w-12 h-12 rounded-2xl bg-rose-50/90 border border-rose-200 text-crimson flex items-center justify-center mx-auto text-xl shadow-xs">
          🗑️
        </div>
        <div>
          <h3 id="modal-del-title" class="font-extrabold text-charcoal text-base">Delete Transaction?</h3>
          <p class="text-xs text-coolslate mt-1 leading-relaxed">
            This will permanently remove this transaction and reverse its balance impact on your goal vault and total capital.
          </p>
        </div>

        <div id="delete-preview-box" class="p-3 bg-white/70 border border-white/90 rounded-xl text-left text-xs space-y-1 backdrop-blur-md shadow-xs">
          <div class="text-coolslate font-mono text-[10px]" id="del-preview-date">--</div>
          <div class="font-bold text-charcoal flex justify-between">
            <span id="del-preview-vault">--</span>
            <span id="del-preview-amount" class="font-mono">--</span>
          </div>
          <div class="text-coolslate text-[11px]" id="del-preview-note">--</div>
        </div>

        <input type="hidden" id="delete-entry-id" />

        <div class="flex items-center gap-2.5 pt-1">
          <button type="button" class="btn-secondary-metallic min-h-[48px] text-xs modal-close flex-1">Cancel</button>
          <button type="button" id="btn-delete-ledger-confirm" class="btn-danger-metallic min-h-[48px] text-xs flex-1 flex items-center justify-center gap-2">
            <span>Delete Entry</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 6. MODAL: PRIVACY POLICY & TRANSPARENT LEDGER DISCLAIMER -->
  <div class="modal-overlay" id="modal-privacy-disclaimer" role="dialog" aria-modal="true" aria-labelledby="modal-disc-title">
    <div class="modal-dialog max-w-lg">
      <!-- Native Mobile Bottom Sheet Drag Handle Bar -->
      <div class="bottom-sheet-handle"></div>

      <div class="flex items-center justify-between px-5 pt-4 pb-3 border-b border-white/60">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-blue-50/90 border border-blue-200 text-cobalt flex items-center justify-center shadow-xs flex-shrink-0">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
          </div>
          <div>
            <h3 id="modal-disc-title" class="font-bold text-charcoal text-sm leading-tight">Privacy Policy &amp; Security Disclaimer</h3>
            <p class="text-[11px] text-coolslate">Transparent Personal Ledger Architecture</p>
          </div>
        </div>
        <button class="w-8 h-8 rounded-full bg-white/80 hover:bg-white flex items-center justify-center text-coolslate hover:text-charcoal modal-close cursor-pointer transition-colors shadow-xs" type="button" aria-label="Close">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <div class="px-5 py-4 space-y-3.5 text-xs text-slate-700 leading-relaxed max-h-[65vh] overflow-y-auto">
        <div class="p-3.5 rounded-xl bg-blue-50/80 border border-blue-200/90 backdrop-blur-md shadow-xs">
          <div class="font-bold text-cobalt flex items-center gap-1.5 mb-1.5 text-sm">
            <span>🛡️</span> Transparent Ledger Disclaimer
          </div>
          <p class="text-slate-800 font-medium leading-relaxed">
            <strong>"Vault.fi is a personal ledger tool. We never connect to your bank accounts or collect real money. You save your own cash or UPI manually; this portal purely tracks your discipline and math."</strong>
          </p>
          <p class="text-cobalt font-semibold mt-2">
            <strong>"Your financial data is private and securely isolated in your Firebase account."</strong>
          </p>
        </div>

        <div>
          <h4 class="font-bold text-charcoal text-xs uppercase tracking-wider mb-1">1. Zero Bank Account Connection</h4>
          <p>
            Vault.fi does NOT require, request, or store your bank credentials, net banking passwords, UPI PINs, or debit/credit card information. All transactions are logged manually by you with single-click precision.
          </p>
        </div>

        <div>
          <h4 class="font-bold text-charcoal text-xs uppercase tracking-wider mb-1">2. Private Firebase Cryptographic Isolation</h4>
          <p>
            Your goal records, ledger history, and streak metrics are isolated end-to-end within your personal Firebase document collection. No third-party data broker or advertising network can read your financial records.
          </p>
        </div>

        <div>
          <h4 class="font-bold text-charcoal text-xs uppercase tracking-wider mb-1">3. Offline-First Math &amp; Real-Time Discipline</h4>
          <p>
            The dynamic pacing engine and flexi-cadence math run client-side in real-time, calculating exact daily and monthly saving quotas to keep you on schedule toward your targets without external surveillance.
          </p>
        </div>
      </div>

      <div class="px-5 py-3.5 border-t border-white/60 flex justify-end">
        <button type="button" class="btn-primary-metallic min-h-[48px] text-xs py-2 px-6 modal-close cursor-pointer w-full sm:w-auto">I Understand &amp; Agree</button>
      </div>
    </div>
  </div>
"""
