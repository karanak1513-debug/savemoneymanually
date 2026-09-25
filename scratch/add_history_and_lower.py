# -*- coding: utf-8 -*-
"""
Implements user request:
1. 'isko lower kro': Lower the desktop sidebar navigation so it docks firmly at the bottom of the left rail.
2. 'isme historz bhi add kro': Add History tab to desktop sidebar, mobile bottom dock, router, and create rich #view-history.
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update aside element and desktop navigation
old_aside_start = """    <aside class="hidden md:flex md:w-64 lg:w-72 min-h-screen border-r border-slate-200/90 bg-white/95 backdrop-blur-2xl flex-col justify-between p-6 fixed left-0 top-0 bottom-0 z-30 shadow-xs">
      
      <!-- Upper Area: Minimal, Clean, and Spacious -->
      <div>
        <!-- Brand Emblem & Identity -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cobalt to-blue-700 flex items-center justify-center shadow-md shadow-blue-500/25 flex-shrink-0">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
          </div>
          <div>
            <div class="text-lg font-extrabold text-charcoal tracking-tight">SaveMoneyManually</div>
            <div class="text-[9px] font-mono text-coolslate tracking-widest uppercase">Discipline Ledger</div>
          </div>
        </div>

        <!-- User Profile Capsule -->
        <div class="mt-8 p-3 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center gap-3">
          <div id="dash-user-avatar" class="w-9 h-9 rounded-xl bg-blue-100 text-cobalt font-bold text-sm flex items-center justify-center overflow-hidden flex-shrink-0">U</div>
          <div class="min-w-0 flex-1">
            <div id="dash-user-name" class="text-xs font-bold text-charcoal truncate">Saver</div>
            <div class="text-[10px] font-mono text-coolslate">&#8377;520/hr baseline</div>
          </div>
        </div>

        <!-- Status Telemetry Badge -->
        <div class="mt-4 px-3 py-1.5 rounded-xl bg-emerald-50 border border-emerald-200/70 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-[10px] font-bold text-emerald-700 font-mono tracking-wide">0ms REAL-TIME ENGINE</span>
        </div>
      </div>

      <!-- LOWER HALF / BOTTOM QUADRANT: DOCKED NAVIGATION STACK -->
      <div class="flex flex-col justify-end gap-2 pb-6 mt-auto pt-6 border-t border-slate-100">
        <div class="text-[10px] font-mono font-bold text-coolslate uppercase tracking-wider px-3 mb-1">Cockpit Views</div>

        <!-- 1. Home Tab -->
        <button id="tab-home-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-3 rounded-xl text-xs font-bold transition-all cursor-pointer bg-blue-50/90 text-blue-600 border border-blue-200/80 shadow-xs" data-target="home" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span>Home</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 transition-opacity"></span>
        </button>

        <!-- 2. Goals Tab -->
        <button id="tab-goals-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-3 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="goals" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
            <span>Goals</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- 3. Calendar Tab -->
        <button id="tab-calendar-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-3 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="calendar" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <span>Calendar</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- 4. Ledger Tab -->
        <button id="tab-ledger-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-3 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="ledger" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            <span>Ledger</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- Sign Out Action -->
        <div class="pt-3">
          <button id="btn-dash-signout" class="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl text-xs font-semibold text-coolslate hover:text-crimson hover:bg-rose-50 border border-slate-200 transition-colors cursor-pointer" type="button">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </aside>"""

new_aside_start = """    <aside class="hidden md:flex md:w-64 lg:w-72 min-h-screen border-r border-slate-200/90 bg-white/95 backdrop-blur-2xl flex-col justify-between p-5 pb-3.5 fixed left-0 top-0 bottom-0 z-30 shadow-xs">
      
      <!-- Upper Area: Minimal, Clean, and Spacious -->
      <div>
        <!-- Brand Emblem & Identity -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cobalt to-blue-700 flex items-center justify-center shadow-md shadow-blue-500/25 flex-shrink-0">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
          </div>
          <div>
            <div class="text-lg font-extrabold text-charcoal tracking-tight">SaveMoneyManually</div>
            <div class="text-[9px] font-mono text-coolslate tracking-widest uppercase">Discipline Ledger</div>
          </div>
        </div>

        <!-- User Profile Capsule -->
        <div class="mt-5 p-2.5 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center gap-3">
          <div id="dash-user-avatar" class="w-9 h-9 rounded-xl bg-blue-100 text-cobalt font-bold text-sm flex items-center justify-center overflow-hidden flex-shrink-0">U</div>
          <div class="min-w-0 flex-1">
            <div id="dash-user-name" class="text-xs font-bold text-charcoal truncate">Saver</div>
            <div class="text-[10px] font-mono text-coolslate">&#8377;520/hr baseline</div>
          </div>
        </div>

        <!-- Status Telemetry Badge -->
        <div class="mt-3 px-3 py-1 rounded-xl bg-emerald-50 border border-emerald-200/70 flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-[10px] font-bold text-emerald-700 font-mono tracking-wide">0ms REAL-TIME ENGINE</span>
        </div>
      </div>

      <!-- LOWER QUADRANT: DOCKED NAVIGATION STACK PUSHED FIRMLY TO BOTTOM -->
      <div class="flex flex-col justify-end gap-1.5 mt-auto pt-3 border-t border-slate-100 pb-0">
        <div class="text-[10px] font-mono font-bold text-coolslate uppercase tracking-wider px-3 mb-0.5">Cockpit Views</div>

        <!-- 1. Home Tab -->
        <button id="tab-home-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer bg-blue-50/90 text-blue-600 border border-blue-200/80 shadow-xs" data-target="home" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span>Home</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 transition-opacity"></span>
        </button>

        <!-- 2. Goals Tab -->
        <button id="tab-goals-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="goals" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
            <span>Goals</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- 3. Calendar Tab -->
        <button id="tab-calendar-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="calendar" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <span>Calendar</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- 4. Ledger Tab -->
        <button id="tab-ledger-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="ledger" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            <span>Ledger</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- 5. History Tab -->
        <button id="tab-history-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="history" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            <span>History</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- Sign Out Action -->
        <div class="pt-2">
          <button id="btn-dash-signout" class="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl text-xs font-semibold text-coolslate hover:text-crimson hover:bg-rose-50 border border-slate-200 transition-colors cursor-pointer" type="button">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </aside>"""

if old_aside_start in html:
    html = html.replace(old_aside_start, new_aside_start)
    print("Updated Desktop sidebar layout (lower position + History tab).")
else:
    print("Warning: old_aside_start not matched directly.")

# 2. Update Mobile Bottom Navigation Dock with History tab
old_mobile_nav = """    <nav id="mobile-navigation-dock" class="fixed bottom-0 inset-x-0 bg-white/90 backdrop-blur-md border-t border-slate-200 z-50 py-2.5 px-4 flex justify-around items-center pb-safe md:hidden shadow-[0_-8px_25px_rgba(15,23,42,0.08)]">
      
      <!-- Tab 1: Home -->
      <button id="tab-home" class="mobile-nav-item flex-1 flex flex-col items-center justify-center py-1.5 text-blue-600 font-bold transition-all cursor-pointer" data-target="home" type="button">
        <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        <span class="text-[10px] leading-tight">Home</span>
        <span class="active-dot w-1 h-1 rounded-full bg-blue-600 mt-0.5 transition-opacity"></span>
      </button>

      <!-- Tab 2: Goals -->
      <button id="tab-goals" class="mobile-nav-item flex-1 flex flex-col items-center justify-center py-1.5 text-slate-500 font-medium transition-all cursor-pointer" data-target="goals" type="button">
        <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
        <span class="text-[10px] leading-tight">Goals</span>
        <span class="active-dot w-1 h-1 rounded-full bg-blue-600 mt-0.5 opacity-0 transition-opacity"></span>
      </button>

      <!-- Tab 3: Calendar -->
      <button id="tab-calendar" class="mobile-nav-item flex-1 flex flex-col items-center justify-center py-1.5 text-slate-500 font-medium transition-all cursor-pointer" data-target="calendar" type="button">
        <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        <span class="text-[10px] leading-tight">Calendar</span>
        <span class="active-dot w-1 h-1 rounded-full bg-blue-600 mt-0.5 opacity-0 transition-opacity"></span>
      </button>

      <!-- Tab 4: Ledger -->
      <button id="tab-ledger" class="mobile-nav-item flex-1 flex flex-col items-center justify-center py-1.5 text-slate-500 font-medium transition-all cursor-pointer" data-target="ledger" type="button">
        <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
        <span class="text-[10px] leading-tight">Ledger</span>
        <span class="active-dot w-1 h-1 rounded-full bg-blue-600 mt-0.5 opacity-0 transition-opacity"></span>
      </button>

    </nav>"""

new_mobile_nav = """    <nav id="mobile-navigation-dock" class="fixed bottom-0 inset-x-0 bg-white/90 backdrop-blur-md border-t border-slate-200 z-50 py-1.5 px-2 flex justify-around items-center pb-safe md:hidden shadow-[0_-8px_25px_rgba(15,23,42,0.08)]">
      
      <!-- Tab 1: Home -->
      <button id="tab-home" class="mobile-nav-item flex-1 flex flex-col items-center justify-center py-1 text-blue-600 font-bold transition-all cursor-pointer" data-target="home" type="button">
        <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
        <span class="text-[10px] leading-tight">Home</span>
        <span class="active-dot w-1 h-1 rounded-full bg-blue-600 mt-0.5 transition-opacity"></span>
      </button>

      <!-- Tab 2: Goals -->
      <button id="tab-goals" class="mobile-nav-item flex-1 flex flex-col items-center justify-center py-1 text-slate-500 font-medium transition-all cursor-pointer" data-target="goals" type="button">
        <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
        <span class="text-[10px] leading-tight">Goals</span>
        <span class="active-dot w-1 h-1 rounded-full bg-blue-600 mt-0.5 opacity-0 transition-opacity"></span>
      </button>

      <!-- Tab 3: Calendar -->
      <button id="tab-calendar" class="mobile-nav-item flex-1 flex flex-col items-center justify-center py-1 text-slate-500 font-medium transition-all cursor-pointer" data-target="calendar" type="button">
        <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        <span class="text-[10px] leading-tight">Calendar</span>
        <span class="active-dot w-1 h-1 rounded-full bg-blue-600 mt-0.5 opacity-0 transition-opacity"></span>
      </button>

      <!-- Tab 4: Ledger -->
      <button id="tab-ledger" class="mobile-nav-item flex-1 flex flex-col items-center justify-center py-1 text-slate-500 font-medium transition-all cursor-pointer" data-target="ledger" type="button">
        <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
        <span class="text-[10px] leading-tight">Ledger</span>
        <span class="active-dot w-1 h-1 rounded-full bg-blue-600 mt-0.5 opacity-0 transition-opacity"></span>
      </button>

      <!-- Tab 5: History -->
      <button id="tab-history" class="mobile-nav-item flex-1 flex flex-col items-center justify-center py-1 text-slate-500 font-medium transition-all cursor-pointer" data-target="history" type="button">
        <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        <span class="text-[10px] leading-tight">History</span>
        <span class="active-dot w-1 h-1 rounded-full bg-blue-600 mt-0.5 opacity-0 transition-opacity"></span>
      </button>

    </nav>"""

if old_mobile_nav in html:
    html = html.replace(old_mobile_nav, new_mobile_nav)
    print("Updated Mobile Navigation dock with History tab.")
else:
    print("Warning: old_mobile_nav not matched directly.")

# 3. Add #view-history right after #view-ledger
idx_view_ledger_end = html.find('</section>\n\n      </div>\n\n    </main>')
if idx_view_ledger_end == -1:
    idx_view_ledger_end = html.find('id="view-ledger"')
    idx_view_ledger_end = html.find('</div>\n\n    </main>', idx_view_ledger_end)

history_view_html = """

      <!-- ======================================================= -->
      <!-- VIEW 5: CHRONOLOGICAL TRANSACTION HISTORY (#view-history)-->
      <!-- ======================================================= -->
      <div id="view-history" class="dissolve-enter hidden flex flex-col gap-6">

        <section class="metallic-card p-4 sm:p-6" aria-label="Transaction History & Activity Log">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
            <div class="flex items-center gap-2.5">
              <div class="w-1.5 h-5 rounded-full bg-cobalt"></div>
              <div>
                <h3 class="font-extrabold text-charcoal text-base">Transaction History &amp; Activity Log</h3>
                <p class="text-xs text-coolslate">Complete chronological audit trail with real-time filters and inline adjustments</p>
              </div>
            </div>

            <!-- Filter buttons -->
            <div class="flex items-center gap-1 bg-slate-50 p-1 rounded-xl border border-slate-200 self-start sm:self-auto">
              <button id="filter-history-all" class="text-xs font-bold px-3 py-1.5 rounded-lg bg-white text-charcoal shadow-xs transition-all cursor-pointer min-h-[34px]" type="button">All Records</button>
              <button id="filter-history-add" class="text-xs font-bold px-3 py-1.5 rounded-lg text-coolslate hover:text-charcoal transition-all cursor-pointer min-h-[34px]" type="button">+ Deposits</button>
              <button id="filter-history-minus" class="text-xs font-bold px-3 py-1.5 rounded-lg text-coolslate hover:text-charcoal transition-all cursor-pointer min-h-[34px]" type="button">- Withdrawals</button>
            </div>
          </div>

          <!-- History Quick Search & Summary Row -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mt-4">
            <div class="relative flex-1 max-w-md">
              <svg class="w-4 h-4 text-coolslate absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-4.35-4.35"/></svg>
              <input type="text" id="history-search-input" placeholder="Search by note, goal vault, or amount…" class="input-metallic pl-9 text-xs py-2 w-full rounded-xl" />
            </div>

            <div class="flex items-center gap-2 text-xs font-mono">
              <span id="history-inflow-chip" class="px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 font-bold border border-emerald-200/60">+&#8377;0 in</span>
              <span id="history-outflow-chip" class="px-2.5 py-1 rounded-lg bg-rose-50 text-rose-700 font-bold border border-rose-200/60">-&#8377;0 out</span>
            </div>
          </div>

          <!-- 1. MOBILE RESPONSIVE STACKED CARDS (md:hidden) -->
          <div id="history-mobile-cards" class="mt-4 flex flex-col gap-2.5 md:hidden"></div>

          <!-- 2. DESKTOP DATA TABLE (hidden md:block) -->
          <div class="mt-4 overflow-x-auto hidden md:block">
            <table class="w-full text-left border-collapse" id="history-table">
              <thead>
                <tr class="border-b border-slate-200 text-[10px] font-mono font-bold text-coolslate uppercase tracking-wider">
                  <th class="py-2.5 px-3">Date</th>
                  <th class="py-2.5 px-3">Goal Vault</th>
                  <th class="py-2.5 px-3">Type</th>
                  <th class="py-2.5 px-3">Note / Reason</th>
                  <th class="py-2.5 px-3 text-right">Amount</th>
                  <th class="py-2.5 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody id="history-table-body" class="divide-y divide-slate-100 text-xs"></tbody>
            </table>
          </div>

          <!-- Empty state -->
          <div id="history-empty-state" class="py-10 flex flex-col items-center justify-center text-center gap-3">
            <div class="w-12 h-12 rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center text-cobalt shadow-xs">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <div class="text-xs text-coolslate font-medium">
              No transactions recorded yet.<br/>Log your first deposit with <strong>[+ Add Saved]</strong>.
            </div>
          </div>
        </section>

      </div>"""

if idx_view_ledger_end != -1:
    idx_insert = idx_view_ledger_end + len('</section>\n\n      </div>')
    html = html[:idx_insert] + history_view_html + html[idx_insert:]
    print("Inserted #view-history view markup.")
else:
    print("Warning: could not locate ledger end boundary.")

# 4. Update JS Router TABS array & switchTab logic
html = html.replace(
    "const TABS = ['home', 'goals', 'calendar', 'ledger'];",
    "const TABS = ['home', 'goals', 'calendar', 'ledger', 'history'];"
)

old_switch_target = """      // 4. Trigger specific view refresh
      if (targetTab === 'home') renderHomeView();
      if (targetTab === 'goals') renderGoalsGrid();
      if (targetTab === 'calendar') renderSavingsCalendar();
      if (targetTab === 'ledger') renderLedger();"""

new_switch_target = """      // 4. Trigger specific view refresh
      if (targetTab === 'home') renderHomeView();
      if (targetTab === 'goals') renderGoalsGrid();
      if (targetTab === 'calendar') renderSavingsCalendar();
      if (targetTab === 'ledger') renderLedger();
      if (targetTab === 'history') renderHistory();"""

html = html.replace(old_switch_target, new_switch_target)

# 5. In renderAll, call renderHistory() as well
html = html.replace(
    """function renderAll() {
      renderCommandMetrics();
      renderHomeView();
      renderGoalsGrid();
      renderSavingsCalendar();
      renderLedger();
      renderGoalSelectors();
    }""",
    """function renderAll() {
      renderCommandMetrics();
      renderHomeView();
      renderGoalsGrid();
      renderSavingsCalendar();
      renderLedger();
      renderHistory();
      renderGoalSelectors();
    }"""
)

# 6. Add renderHistory function & filter listeners in JS
idx_render_ledger = html.find('function renderLedger() {')
if idx_render_ledger != -1:
    history_js = """    let historyFilter = 'ALL';
    let historySearchQuery = '';

    function renderHistory() {
      const mobileCards = document.getElementById('history-mobile-cards');
      const tbody = document.getElementById('history-table-body');
      const emptyState = document.getElementById('history-empty-state');
      const inflowChip = document.getElementById('history-inflow-chip');
      const outflowChip = document.getElementById('history-outflow-chip');

      let filtered = [...ledger];

      if (historyFilter === 'ADD') filtered = filtered.filter(i => i.type === 'ADD');
      if (historyFilter === 'MINUS') filtered = filtered.filter(i => i.type === 'MINUS');

      if (historySearchQuery) {
        const q = historySearchQuery.toLowerCase();
        filtered = filtered.filter(i => 
          (i.goalName && i.goalName.toLowerCase().includes(q)) ||
          (i.note && i.note.toLowerCase().includes(q)) ||
          String(i.amount).includes(q) ||
          (i.date && i.date.includes(q))
        );
      }

      filtered.sort((a, b) => new Date(b.date || b.timestamp) - new Date(a.date || a.timestamp));

      // Calculate inflows / outflows
      let totalIn = 0;
      let totalOut = 0;
      ledger.forEach(i => {
        const amt = Number(i.amount) || 0;
        if (i.type === 'ADD') totalIn += amt;
        else totalOut += amt;
      });
      if (inflowChip) inflowChip.textContent = `+₹${totalIn.toLocaleString('en-IN')} in`;
      if (outflowChip) outflowChip.textContent = `-₹${totalOut.toLocaleString('en-IN')} out`;

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

      document.querySelectorAll('#view-history .btn-edit-entry').forEach(btn => {
        btn.addEventListener('click', () => openEditLedgerModal(btn.dataset.id));
      });
      document.querySelectorAll('#view-history .btn-del-entry').forEach(btn => {
        btn.addEventListener('click', () => openDeleteLedgerModal(btn.dataset.id));
      });
    }

"""
    html = html[:idx_render_ledger] + history_js + html[idx_render_ledger:]
    print("Added renderHistory() and history state variables.")

# 7. Add filter and search listeners for History view
idx_filter_init = html.find("document.getElementById('filter-ledger-all')")
if idx_filter_init != -1:
    filter_history_listeners = """    // History Filters & Search
    const fHistAll = document.getElementById('filter-history-all');
    const fHistAdd = document.getElementById('filter-history-add');
    const fHistMinus = document.getElementById('filter-history-minus');
    const histSearchInput = document.getElementById('history-search-input');

    function updateHistFilterUI(active) {
      historyFilter = active;
      [fHistAll, fHistAdd, fHistMinus].forEach(btn => {
        if (!btn) return;
        btn.className = 'text-xs font-bold px-3 py-1.5 rounded-lg text-coolslate hover:text-charcoal transition-all cursor-pointer min-h-[34px]';
      });
      if (active === 'ALL' && fHistAll) fHistAll.className = 'text-xs font-bold px-3 py-1.5 rounded-lg bg-white text-charcoal shadow-xs transition-all cursor-pointer min-h-[34px]';
      if (active === 'ADD' && fHistAdd) fHistAdd.className = 'text-xs font-bold px-3 py-1.5 rounded-lg bg-white text-cobalt shadow-xs transition-all cursor-pointer min-h-[34px]';
      if (active === 'MINUS' && fHistMinus) fHistMinus.className = 'text-xs font-bold px-3 py-1.5 rounded-lg bg-white text-crimson shadow-xs transition-all cursor-pointer min-h-[34px]';
      renderHistory();
    }

    fHistAll?.addEventListener('click', () => updateHistFilterUI('ALL'));
    fHistAdd?.addEventListener('click', () => updateHistFilterUI('ADD'));
    fHistMinus?.addEventListener('click', () => updateHistFilterUI('MINUS'));

    histSearchInput?.addEventListener('input', (e) => {
      historySearchQuery = e.target.value.trim();
      renderHistory();
    });

"""
    html = html[:idx_filter_init] + filter_history_listeners + html[idx_filter_init:]
    print("Added History filter and search listeners.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated index.html with lowered dock & History tab! Length:", len(html))
