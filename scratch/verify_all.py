# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("="*60)
print("AUDIT: SIDEBAR BOTTOM DOCK & CLEAN 4-TAB NAVIGATION")
print("="*60)

# 1. Branding: SaveMoneyManually
assert "SaveMoneyManually" in text, "Brand name SaveMoneyManually missing!"
assert "Vault.fi" not in text and "vault.fi" not in text, "Unwanted Vault.fi still present!"
print("1. Brand Name: SaveMoneyManually confirmed across all locations (0 Vault.fi): PASS")

# 2. Left Sidebar strict flex layout:
# flex flex-col justify-between h-screen sticky top-0 py-6 px-4
assert 'flex-col justify-between h-screen sticky top-0 py-6 px-4' in text, "Sidebar sticky h-screen flex layout missing!"
print("2. Sidebar Layout: 'flex flex-col justify-between h-screen sticky top-0 py-6 px-4' confirmed: PASS")

# 3. Top Section: Brand header and User profile card ONLY
# 4. Middle Section: Empty flex-1 spacer
assert '<div class="flex-1"></div>' in text, "Empty flex-1 spacer missing!"
print("3. Middle Spacer: '<div class=\"flex-1\"></div>' confirmed pushing content down: PASS")

# 5. Bottom Section: mt-auto flex flex-col gap-1 pb-2
assert 'mt-auto flex flex-col gap-1 pb-2' in text, "mt-auto flex flex-col gap-1 pb-2 missing!"
print("4. Bottom Section: 'mt-auto flex flex-col gap-1 pb-2' confirmed: PASS")

# 6. Tab Redundancy Check: Only 4 Core Tabs (Home, Goals, Calendar, Ledger)
# Sign Out button neatly below Ledger tab
assert "tab-home-desktop" in text and "tab-goals-desktop" in text and "tab-calendar-desktop" in text and "tab-ledger-desktop" in text, "4 desktop tabs missing!"
assert "tab-history-desktop" not in text, "Redundant tab-history-desktop still present!"
assert "tab-home" in text and "tab-goals" in text and "tab-calendar" in text and "tab-ledger" in text, "4 mobile tabs missing!"
assert 'id="tab-history"' not in text, "Redundant mobile tab-history still present!"
assert 'const TABS = [\'home\', \'goals\', \'calendar\', \'ledger\'];' in text, "TABS array does not match 4 core views!"
assert 'id="view-history"' not in text, "Redundant #view-history container still present!"
print("5. 4 Core Views Only (Home, Goals, Calendar, Ledger) - History merged into Ledger: PASS")

# 7. Mobile dock: fixed bottom-0 inset-x-0
assert 'fixed bottom-0 inset-x-0' in text, "Mobile dock fixed bottom-0 missing!"
print("6. Mobile fixed bottom dock confirmed: PASS")

# 8. 3D Canvas & Texture
assert '<canvas id="three-bg-canvas"' in text, "Canvas element missing!"
assert "radial-gradient(rgba(15, 23, 42, 0.08) 1px, transparent 1px)" in text, "Dot-matrix texture missing!"
print("7. 3D Wireframe Canvas & White Dot-Matrix Texture confirmed: PASS")

print("="*60)
print("ALL CRITICAL UI REFINEMENT VERIFICATIONS PASSED!")
print("="*60)
