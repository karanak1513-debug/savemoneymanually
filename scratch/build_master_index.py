# -*- coding: utf-8 -*-
"""
Assembles index.html with crystal glassmorphism across all cards and layouts,
and lightning-fast real-time save logic.
"""

from dashboard_html import DASHBOARD_HTML
from dashboard_js import DASHBOARD_JS

with open('index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# Locate boundaries
idx_dash = orig.find('  <!-- ============================================================ -->\n  <!-- 2. FULL AUTONOMOUS METALLIC FINTECH DASHBOARD VIEW')
if idx_dash == -1:
    idx_dash = orig.find('<div id="dashboard-view"')

idx_three = orig.find('  <!-- ============================================================ -->\n  <!-- 3D INTERACTIVE THREE.JS BACKGROUND SCRIPT -->')
if idx_three == -1:
    idx_three = orig.find('initThreeBackground')
    idx_three = orig.rfind('<script>', 0, idx_three)

idx_module = orig.find('<script type="module">')

print(f"Indices: idx_dash={idx_dash}, idx_three={idx_three}, idx_module={idx_module}")

head_and_auth = orig[:idx_dash]
three_and_loader_scripts = orig[idx_three:idx_module]

# Upgrade CSS foundations to pure frosted glassmorphism
glass_css = """
    /* ============================================================ */
    /* ULTRA-PREMIUM CRYSTAL FROSTED GLASSMORPHISM DESIGN SYSTEM    */
    /* ============================================================ */

    body {
      background-color: #F8FAFC !important;
      background-image: 
        radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.08) 0px, transparent 55%),
        radial-gradient(at 100% 0%, rgba(99, 102, 241, 0.07) 0px, transparent 55%),
        radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.06) 0px, transparent 55%),
        radial-gradient(at 0% 100%, rgba(225, 29, 72, 0.05) 0px, transparent 55%),
        radial-gradient(rgba(15, 23, 42, 0.06) 1px, transparent 1px) !important;
      background-size: 100% 100%, 100% 100%, 100% 100%, 100% 100%, 24px 24px !important;
      background-attachment: fixed !important;
      color: #0F172A;
      font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }

    /* ── Crystal Glass Cards (Translucent, Frosted, Beveled Glow) ─ */
    .metallic-card,
    .glass-card {
      background: rgba(255, 255, 255, 0.65) !important;
      backdrop-filter: blur(28px) saturate(190%) !important;
      -webkit-backdrop-filter: blur(28px) saturate(190%) !important;
      border: 1px solid rgba(255, 255, 255, 0.85) !important;
      box-shadow: 
        0 20px 45px -12px rgba(15, 23, 42, 0.07),
        0 0 0 1px rgba(255, 255, 255, 0.9) inset,
        0 1px 0 0 rgba(255, 255, 255, 1) inset !important;
      border-radius: 24px !important;
      position: relative;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .metallic-card:hover,
    .glass-card:hover {
      background: rgba(255, 255, 255, 0.78) !important;
      border-color: rgba(191, 219, 254, 0.95) !important;
      box-shadow: 
        0 28px 60px -12px rgba(37, 99, 235, 0.12),
        0 0 0 1px rgba(255, 255, 255, 0.98) inset,
        0 1px 0 0 rgba(255, 255, 255, 1) inset !important;
      transform: translateY(-2px);
    }

    /* ── Inner Frosted Glass Tiles ─────────────────────────────── */
    .glass-inner-tile {
      background: rgba(255, 255, 255, 0.52) !important;
      backdrop-filter: blur(14px) saturate(160%) !important;
      -webkit-backdrop-filter: blur(14px) saturate(160%) !important;
      border: 1px solid rgba(255, 255, 255, 0.85) !important;
      border-radius: 18px !important;
      box-shadow: 0 4px 15px -3px rgba(15, 23, 42, 0.03), inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
      transition: all 0.2s ease;
    }
    .glass-inner-tile:hover {
      background: rgba(255, 255, 255, 0.68) !important;
      border-color: rgba(191, 219, 254, 0.8) !important;
      transform: translateY(-1px);
    }

    /* ── Crystal Glass Floating Modals ─────────────────────────── */
    .modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.38) !important;
      backdrop-filter: blur(18px) !important;
      -webkit-backdrop-filter: blur(18px) !important;
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 99999;
      opacity: 0;
      pointer-events: none;
      transition: opacity 0.28s cubic-bezier(0.22, 1, 0.36, 1);
      padding: 1.5rem;
    }
    .modal-overlay.open {
      opacity: 1;
      pointer-events: auto;
    }
    .modal-dialog {
      background: rgba(255, 255, 255, 0.82) !important;
      backdrop-filter: blur(36px) saturate(220%) !important;
      -webkit-backdrop-filter: blur(36px) saturate(220%) !important;
      border: 1.5px solid rgba(255, 255, 255, 0.92) !important;
      border-radius: 28px !important;
      box-shadow:
        0 35px 85px -15px rgba(15, 23, 42, 0.25),
        0 0 0 1px rgba(255, 255, 255, 0.95) inset,
        0 2px 0 0 #FFFFFF inset !important;
      width: 100%;
      max-width: 480px;
      transform: scale(0.94) translateY(18px);
      opacity: 0;
      transition:
        transform 0.38s cubic-bezier(0.34, 1.56, 0.64, 1),
        opacity 0.25s cubic-bezier(0.22, 1, 0.36, 1);
      overflow: hidden;
    }
    .modal-overlay.open .modal-dialog {
      transform: scale(1) translateY(0);
      opacity: 1;
    }

    /* ── Frosted Glass Inputs & Chip Autocomplete ───────────────── */
    .input-metallic,
    .chip-input-wrapper {
      width: 100%;
      background: rgba(255, 255, 255, 0.65) !important;
      backdrop-filter: blur(12px) !important;
      -webkit-backdrop-filter: blur(12px) !important;
      border: 1.5px solid rgba(203, 213, 225, 0.8) !important;
      border-radius: 14px !important;
      padding: 0.75rem 1rem;
      font-size: 0.92rem;
      color: #0F172A !important;
      box-shadow: inset 0 2px 4px rgba(15, 23, 42, 0.02) !important;
      outline: none;
      transition: all 0.18s ease;
    }
    .input-metallic:focus,
    .chip-input-wrapper:focus-within {
      background: rgba(255, 255, 255, 0.92) !important;
      border-color: #2563EB !important;
      box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14), inset 0 1px 2px rgba(15, 23, 42, 0.02) !important;
    }

    .chip-suggestions {
      background: rgba(255, 255, 255, 0.9) !important;
      backdrop-filter: blur(20px) !important;
      -webkit-backdrop-filter: blur(20px) !important;
      border: 1px solid rgba(226, 232, 240, 0.9) !important;
      border-radius: 14px !important;
      box-shadow: 0 15px 35px -5px rgba(15, 23, 42, 0.14) !important;
    }

    /* ── Interactive Calendar & Dynamic Ledger Styles ──────────── */
    .cal-day-cell {
      min-height: 52px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      padding: 7px 4px;
      border-radius: 14px;
      font-size: 0.75rem;
      font-weight: 600;
      border: 1px solid rgba(255, 255, 255, 0.8);
      background: rgba(255, 255, 255, 0.55);
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }
    .cal-day-cell:hover {
      background: rgba(255, 255, 255, 0.85);
      border-color: #93C5FD;
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(37, 99, 235, 0.1);
    }
    .cal-day-cell.cal-active-saved {
      background: linear-gradient(135deg, rgba(37, 99, 235, 0.14) 0%, rgba(59, 130, 246, 0.24) 100%) !important;
      border-color: #2563EB !important;
      color: #1E40AF !important;
      box-shadow: 0 4px 16px rgba(37, 99, 235, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
    }
    .cal-day-cell.cal-active-saved .cal-day-badge {
      background: #2563EB;
      color: #FFFFFF;
      border-radius: 9999px;
      padding: 1.5px 6px;
      font-size: 9px;
      font-family: 'Space Grotesk', monospace;
      font-weight: 700;
      box-shadow: 0 2px 6px rgba(37, 99, 235, 0.35);
    }
    .cal-day-cell.cal-today {
      box-shadow: 0 0 0 2px #2563EB, 0 4px 14px rgba(37, 99, 235, 0.25) !important;
    }
    .cal-day-cell.cal-other-month {
      background: rgba(248, 250, 252, 0.4);
      color: #CBD5E1;
      border-color: transparent;
      pointer-events: none;
    }

    .btn-danger-metallic {
      background: linear-gradient(135deg, #FFF1F2 0%, #FFE4E6 100%);
      color: #E11D48;
      font-weight: 600;
      border-radius: 12px;
      padding: 0.65rem 1.25rem;
      border: 1px solid #FECDD3;
      box-shadow: 0 2px 8px rgba(225, 29, 72, 0.1);
      transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      cursor: pointer;
    }
    .btn-danger-metallic:hover:not(:disabled) {
      background: linear-gradient(135deg, #FFE4E6 0%, #FECDD3 100%);
      border-color: #FDA4AF;
      transform: translateY(-1.5px);
    }
    .btn-danger-metallic:disabled {
      opacity: 0.55;
      cursor: not-allowed;
      transform: none !important;
    }
    .ledger-badge-add {
      background: rgba(236, 253, 245, 0.85);
      color: #059669;
      border: 1px solid #A7F3D0;
    }
    .ledger-badge-minus {
      background: rgba(255, 241, 242, 0.85);
      color: #E11D48;
      border: 1px solid #FECDD3;
    }
    .pacing-banner-warning {
      background: rgba(255, 241, 242, 0.75) !important;
      backdrop-filter: blur(16px) !important;
      border: 1px solid #FECDD3 !important;
      border-left: 4px solid #E11D48 !important;
    }
    .pacing-banner-optimal {
      background: rgba(239, 246, 255, 0.75) !important;
      backdrop-filter: blur(16px) !important;
      border: 1px solid #BFDBFE !important;
      border-left: 4px solid #2563EB !important;
    }
"""

# Replace existing custom styles in head
start_style = head_and_auth.find('<style>')
end_style = head_and_auth.find('</style>')

if start_style != -1 and end_style != -1:
    old_css = head_and_auth[start_style:end_style+8]
    # Replace the old metallic-card and body definitions
    head_and_auth = head_and_auth[:end_style] + glass_css + head_and_auth[end_style:]

final_html = head_and_auth + DASHBOARD_HTML + '\n' + three_and_loader_scripts + DASHBOARD_JS + '\n</body>\n</html>\n'

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"Generated index.html successfully with Glassy Look! Total length: {len(final_html)} chars.")
