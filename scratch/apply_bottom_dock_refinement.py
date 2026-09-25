# -*- coding: utf-8 -*-
"""
Applies Critical UI Refinement:
1. Left sidebar strict flex layout:
   flex flex-col justify-between h-screen sticky top-0 py-6 px-4
   - Top Section: Brand header and User profile card ONLY.
   - Middle Section: Empty spacer flex-1 pushing all content down.
   - Bottom Section: mt-auto flex flex-col gap-1 pb-2 with Home, Goals, Calendar, Ledger and Sign Out.
2. Clean Tab Redundancy:
   - Merge Ledger and History into single tab: 'Ledger'
   - Keep ONLY 4 core views: Home, Goals, Calendar, Ledger
   - Remove #view-history container
   - TABS = ['home', 'goals', 'calendar', 'ledger']
3. Mobile Compatibility:
   - Fixed bottom dock with only 4 tabs (Home, Goals, Calendar, Ledger)
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update <aside> and its entire structure
old_aside_start = html.find('<!-- ── DESKTOP LEFT VERTICAL SIDEBAR')
if old_aside_start == -1:
    old_aside_start = html.find('<aside')

old_aside_end = html.find('</aside>') + len('</aside>')

new_aside = """<!-- ── DESKTOP LEFT VERTICAL SIDEBAR (STRICTLY DOCKED BOTTOM) ── -->
    <aside class="hidden md:flex md:w-64 lg:w-72 flex-shrink-0 flex-col justify-between h-screen sticky top-0 py-6 px-4 border-r border-slate-200/90 bg-white/95 backdrop-blur-2xl z-30 shadow-xs">
      
      <!-- Top Section: Brand Header & User Profile Card ONLY -->
      <div class="flex flex-col gap-4">
        <!-- Brand Emblem & Identity -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cobalt to-blue-700 flex items-center justify-center shadow-md shadow-blue-500/25 flex-shrink-0">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
          </div>
          <div>
            <div class="text-lg font-extrabold text-charcoal tracking-tight leading-tight">SaveMoneyManually</div>
            <div class="text-[9px] font-mono text-coolslate tracking-widest uppercase">Discipline Ledger</div>
          </div>
        </div>

        <!-- User Profile Card -->
        <div class="p-3 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center gap-3">
          <div id="dash-user-avatar" class="w-9 h-9 rounded-xl bg-blue-100 text-cobalt font-bold text-sm flex items-center justify-center overflow-hidden flex-shrink-0">U</div>
          <div class="min-w-0 flex-1">
            <div id="dash-user-name" class="text-xs font-bold text-charcoal truncate">Saver</div>
            <div class="text-[10px] font-mono text-coolslate">&#8377;520/hr baseline</div>
          </div>
        </div>
      </div>

      <!-- Middle Section: Empty flex-1 spacer pushing all navigation to absolute bottom -->
      <div class="flex-1"></div>

      <!-- Bottom/Lower Section: Anchored at Very Bottom (mt-auto flex flex-col gap-1 pb-2) -->
      <div class="mt-auto flex flex-col gap-1 pb-2 border-t border-slate-100 pt-3">
        <div class="text-[10px] font-mono font-bold text-coolslate uppercase tracking-wider px-3 mb-1">Cockpit Views</div>

        <!-- 1. Home Tab -->
        <button id="tab-home-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer bg-blue-50/90 text-blue-600 border border-blue-200/80 shadow-xs" data-target="home" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span>Home</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 transition-opacity"></span>
        </button>

        <!-- 2. Goals Tab -->
        <button id="tab-goals-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="goals" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
            <span>Goals</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- 3. Calendar Tab -->
        <button id="tab-calendar-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="calendar" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <span>Calendar</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- 4. Ledger Tab (Merged Ledger & History) -->
        <button id="tab-ledger-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="ledger" type="button">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            <span>Ledger</span>
          </div>
          <span class="active-dot w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- Sign Out Action (Neatly below Ledger tab) -->
        <div class="pt-2">
          <button id="btn-dash-signout" class="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl text-xs font-semibold text-coolslate hover:text-crimson hover:bg-rose-50 border border-slate-200 transition-colors cursor-pointer" type="button">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
            <span>Sign Out</span>
          </button>
        </div>
      </div>
    </aside>"""

html = html[:old_aside_start] + new_aside + html[old_aside_end:]
print("Updated aside with strict h-screen sticky top-0 flex-1 spacer and mt-auto bottom dock.")

# 2. Update <main> class to remove md:pl-64 lg:pl-72 since aside is sticky inside flex-row
html = html.replace(
    '<main class="md:pl-64 lg:pl-72 flex-1 w-full min-h-screen px-4 py-5 sm:px-6 sm:py-8 pb-24 md:pb-12 max-w-6xl mx-auto">',
    '<main class="flex-1 min-w-0 min-h-screen px-4 py-5 sm:px-6 sm:py-8 pb-24 md:pb-12 max-w-6xl mx-auto">'
)

# 3. Update Mobile Bottom Dock: ONLY 4 tabs (Home, Goals, Calendar, Ledger)
old_mobile_dock_start = html.find('<!-- ── MOBILE LOWER NAVIGATION DOCK')
if old_mobile_dock_start == -1:
    old_mobile_dock_start = html.find('<nav id="mobile-navigation-dock"')

old_mobile_dock_end = html.find('</nav>', old_mobile_dock_start) + len('</nav>')

new_mobile_dock = """<!-- ── MOBILE LOWER NAVIGATION DOCK (STRICT 4 TABS: md:hidden) ── -->
    <nav id="mobile-navigation-dock" class="fixed bottom-0 inset-x-0 bg-white/90 backdrop-blur-md border-t border-slate-200 z-50 py-2.5 px-4 flex justify-around items-center pb-safe md:hidden shadow-[0_-8px_25px_rgba(15,23,42,0.08)]">
      
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

      <!-- Tab 4: Ledger (Merged Ledger & History) -->
      <button id="tab-ledger" class="mobile-nav-item flex-1 flex flex-col items-center justify-center py-1.5 text-slate-500 font-medium transition-all cursor-pointer" data-target="ledger" type="button">
        <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
        <span class="text-[10px] leading-tight">Ledger</span>
        <span class="active-dot w-1 h-1 rounded-full bg-blue-600 mt-0.5 opacity-0 transition-opacity"></span>
      </button>

    </nav>"""

html = html[:old_mobile_dock_start] + new_mobile_dock + html[old_mobile_dock_end:]
print("Updated Mobile Navigation dock to 4 tabs.")

# 4. Remove #view-history container to keep strictly 4 core views
idx_hist_view_start = html.find('<!-- VIEW 5: CHRONOLOGICAL TRANSACTION HISTORY')
if idx_hist_view_start != -1:
    idx_hist_view_start = html.rfind('<!--', 0, idx_hist_view_start)
    idx_hist_view_end = html.find('</div>\n\n    </main>', idx_hist_view_start) + len('</div>\n')
    html = html[:idx_hist_view_start] + html[idx_hist_view_end:]
    print("Removed duplicate #view-history view markup.")

# 5. Clean JS Router: TABS = ['home', 'goals', 'calendar', 'ledger']
html = html.replace(
    "const TABS = ['home', 'goals', 'calendar', 'ledger', 'history'];",
    "const TABS = ['home', 'goals', 'calendar', 'ledger'];"
)
html = html.replace(
    "      if (targetTab === 'ledger') renderLedger();\n      if (targetTab === 'history') renderHistory();",
    "      if (targetTab === 'ledger') renderLedger();"
)
html = html.replace(
    "      renderLedger();\n      renderHistory();",
    "      renderLedger();"
)

# Also remove unused history listeners if present
idx_hist_js = html.find('    let historyFilter = \'ALL\';')
if idx_hist_js != -1:
    idx_render_ledger_start = html.find('    // View 4: Ledger & History Helper', idx_hist_js)
    if idx_render_ledger_start != -1:
        html = html[:idx_hist_js] + html[idx_render_ledger_start:]
        print("Cleaned up redundant history JS helper functions.")

idx_filter_hist = html.find('    // History Filters & Search')
if idx_filter_hist != -1:
    idx_filter_ledger_all = html.find('    // Ledger Filters\n    const fAll = document.getElementById', idx_filter_hist)
    if idx_filter_ledger_all != -1:
        html = html[:idx_filter_hist] + html[idx_filter_ledger_all:]
        print("Cleaned up redundant history filter listeners.")

# Save updated index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved updated index.html successfully! Length:", len(html))
