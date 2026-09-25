# -*- coding: utf-8 -*-
"""
Applies FEATURE: COLLAPSIBLE SIDEBAR WITH SMOOTH SLIDE ANIMATION
1. Updates <aside> to have:
   id="sidebar"
   class="hidden md:flex md:w-64 flex-shrink-0 flex-col justify-between h-screen sticky top-0 py-6 px-4 border-r border-slate-200/90 bg-white/95 backdrop-blur-2xl z-30 shadow-xs transition-all duration-300 ease-in-out relative"
2. Adds toggle button at the top-right border of the sidebar:
   <button id="sidebarToggleBtn" aria-label="Toggle Sidebar" title="Collapse Sidebar" class="absolute -right-3 top-6 border border-slate-200 shadow-md bg-white hover:bg-slate-50 w-7 h-7 rounded-full flex items-center justify-center cursor-pointer z-50 text-slate-600 transition-all hover:scale-105" type="button">
     <svg class="w-3.5 h-3.5 transition-transform duration-300" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
       <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
     </svg>
   </button>
3. Tags all text labels with class "sidebar-text"
4. Centers icons and emblems in collapsed w-20 state
5. Adds CSS rules for .w-20 state and transitions
6. Integrates JS toggle logic with state persistence in localStorage
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS rules in <style>
css_marker = "/* Base Canvas: Stark Pure White"
sidebar_css = """    /* ── COLLAPSIBLE SIDEBAR TRANSITIONS & DOCK STYLES ───────── */
    #sidebar {
      transition: width 300ms cubic-bezier(0.16, 1, 0.3, 1), padding 300ms cubic-bezier(0.16, 1, 0.3, 1);
    }
    #sidebar.w-20 {
      width: 5rem !important;
      padding-left: 0.625rem !important;
      padding-right: 0.625rem !important;
    }
    #sidebar.w-20 .sidebar-text {
      display: none !important;
      opacity: 0 !important;
      pointer-events: none !important;
    }
    #sidebar.w-20 #dash-brand-wrap {
      justify-content: center !important;
    }
    #sidebar.w-20 #dash-profile-card {
      padding: 0.375rem !important;
      justify-content: center !important;
    }
    #sidebar.w-20 .desktop-nav-item {
      justify-content: center !important;
      padding-left: 0 !important;
      padding-right: 0 !important;
    }
    #sidebar.w-20 .desktop-nav-item .active-dot {
      display: none !important;
    }
    #sidebar.w-20 #btn-dash-signout {
      justify-content: center !important;
      padding-left: 0 !important;
      padding-right: 0 !important;
    }

"""

if css_marker in html and "/* ── COLLAPSIBLE SIDEBAR" not in html:
    html = html.replace(css_marker, sidebar_css + css_marker, 1)
    print("Added collapsible sidebar CSS rules.")

# 2. Replace the <aside> block
old_aside_start = html.find('<!-- ── DESKTOP LEFT VERTICAL SIDEBAR')
old_aside_end = html.find('</aside>', old_aside_start) + len('</aside>')

new_aside_block = """<!-- ── DESKTOP LEFT VERTICAL SIDEBAR (STRICTLY DOCKED BOTTOM & COLLAPSIBLE) ── -->
    <aside id="sidebar" class="hidden md:flex md:w-64 flex-shrink-0 flex-col justify-between h-screen sticky top-0 py-6 px-4 border-r border-slate-200/90 bg-white/95 backdrop-blur-2xl z-30 shadow-xs transition-all duration-300 ease-in-out relative">
      
      <!-- Collapse / Expand Toggle Button -->
      <button id="sidebarToggleBtn" aria-label="Toggle Sidebar" title="Collapse Sidebar" class="absolute -right-3 top-6 border border-slate-200 shadow-md bg-white hover:bg-slate-50 w-7 h-7 rounded-full flex items-center justify-center cursor-pointer z-50 text-slate-600 transition-all hover:scale-105" type="button">
        <svg class="w-3.5 h-3.5 transition-transform duration-300" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
      </button>

      <!-- Top Section: Brand Header & User Profile Card ONLY -->
      <div class="flex flex-col gap-4">
        <!-- Brand Emblem & Identity -->
        <div id="dash-brand-wrap" class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cobalt to-blue-700 flex items-center justify-center shadow-md shadow-blue-500/25 flex-shrink-0">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
          </div>
          <div class="sidebar-text min-w-0">
            <div class="text-lg font-extrabold text-charcoal tracking-tight leading-tight truncate">SaveMoneyManually</div>
            <div class="text-[9px] font-mono text-coolslate tracking-widest uppercase truncate">Discipline Ledger</div>
          </div>
        </div>

        <!-- User Profile Card -->
        <div id="dash-profile-card" class="p-3 rounded-2xl bg-slate-50 border border-slate-200/80 flex items-center gap-3 transition-all">
          <div id="dash-user-avatar" class="w-9 h-9 rounded-xl bg-blue-100 text-cobalt font-bold text-sm flex items-center justify-center overflow-hidden flex-shrink-0">U</div>
          <div class="min-w-0 flex-1 sidebar-text">
            <div id="dash-user-name" class="text-xs font-bold text-charcoal truncate">Saver</div>
            <div class="text-[10px] font-mono text-coolslate">&#8377;520/hr baseline</div>
          </div>
        </div>
      </div>

      <!-- Middle Section: Empty flex-1 spacer pushing all navigation to absolute bottom -->
      <div class="flex-1"></div>

      <!-- Bottom/Lower Section: Anchored at Very Bottom (mt-auto flex flex-col gap-1 pb-2) -->
      <div class="mt-auto flex flex-col gap-1 pb-2 border-t border-slate-100 pt-3">
        <div class="sidebar-text text-[10px] font-mono font-bold text-coolslate uppercase tracking-wider px-3 mb-1">Cockpit Views</div>

        <!-- 1. Home Tab -->
        <button id="tab-home-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-bold transition-all cursor-pointer bg-blue-50/90 text-blue-600 border border-blue-200/80 shadow-xs" data-target="home" type="button" title="Home">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
            <span class="sidebar-text">Home</span>
          </div>
          <span class="active-dot sidebar-text w-1.5 h-1.5 rounded-full bg-blue-600 transition-opacity"></span>
        </button>

        <!-- 2. Goals Tab -->
        <button id="tab-goals-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="goals" type="button" title="Goals">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><circle cx="12" cy="11" r="2.5"/></svg>
            <span class="sidebar-text">Goals</span>
          </div>
          <span class="active-dot sidebar-text w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- 3. Calendar Tab -->
        <button id="tab-calendar-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="calendar" type="button" title="Calendar">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <span class="sidebar-text">Calendar</span>
          </div>
          <span class="active-dot sidebar-text w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- 4. Ledger Tab (Merged Ledger & History) -->
        <button id="tab-ledger-desktop" class="desktop-nav-item w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 transition-all cursor-pointer border border-transparent" data-target="ledger" type="button" title="Ledger">
          <div class="flex items-center gap-3">
            <svg class="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
            <span class="sidebar-text">Ledger</span>
          </div>
          <span class="active-dot sidebar-text w-1.5 h-1.5 rounded-full bg-blue-600 opacity-0 transition-opacity"></span>
        </button>

        <!-- Sign Out Action (Neatly below Ledger tab) -->
        <div class="pt-2">
          <button id="btn-dash-signout" class="w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl text-xs font-semibold text-coolslate hover:text-crimson hover:bg-rose-50 border border-slate-200 transition-colors cursor-pointer" type="button" title="Sign Out">
            <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
            <span class="sidebar-text">Sign Out</span>
          </button>
        </div>
      </div>
    </aside>"""

html = html[:old_aside_start] + new_aside_block + html[old_aside_end:]
print("Replaced aside block with collapsible sidebar markup.")

# 3. Add JS collapsible controller
js_marker = "const trailingArrowIcon = document.getElementById('trailing-arrow-icon');"
sidebar_js = """    // ============================================================
    // COLLAPSIBLE SIDEBAR CONTROLLER WITH SMOOTH SLIDE ANIMATION
    // ============================================================
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebarToggleBtn');
    let isCollapsed = false;

    function applySidebarState(collapsed) {
      isCollapsed = !!collapsed;
      if (!sidebar || !toggleBtn) return;

      sidebar.classList.toggle('w-64', !isCollapsed);
      sidebar.classList.toggle('w-20', isCollapsed);
      document.querySelectorAll('.sidebar-text').forEach(el => {
        el.classList.toggle('hidden', isCollapsed);
      });

      const chevron = toggleBtn.querySelector('svg');
      if (chevron) {
        chevron.classList.toggle('rotate-180', isCollapsed);
      }
      toggleBtn.setAttribute('title', isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar');
      toggleBtn.setAttribute('aria-expanded', String(!isCollapsed));

      try {
        localStorage.setItem('smm_sidebar_collapsed', isCollapsed ? 'true' : 'false');
      } catch (e) {}
    }

    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        applySidebarState(!isCollapsed);
      });

      // Restore persisted collapsed state from localStorage
      try {
        const savedSidebarState = localStorage.getItem('smm_sidebar_collapsed');
        if (savedSidebarState === 'true') {
          applySidebarState(true);
        }
      } catch (e) {}
    }

    """

if js_marker in html and "COLLAPSIBLE SIDEBAR CONTROLLER" not in html:
    html = html.replace(js_marker, sidebar_js + js_marker, 1)
    print("Added collapsible sidebar JavaScript controller.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved index.html successfully! Length:", len(html))
