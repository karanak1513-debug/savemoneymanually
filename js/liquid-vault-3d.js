// ============================================================
// VAULT.FI — 3D Liquid Vaults Engine & Confetti Celebration
// ============================================================

import { formatCurrency, calcProgress, daysUntil } from "./utils.js";

/**
 * Generates the HTML for a 3D Frosted Glass Liquid Cylinder
 * @param {Object} vault - Vault document
 * @param {Object} opts - Display options { interactive, showControls }
 */
export function createLiquidCylinderHTML(vault, opts = {}) {
  const current = Number(vault.currentAmount) || 0;
  const target = Math.max(1, Number(vault.targetAmount) || 1);
  const pct = Math.min(100, Math.max(0, Math.round((current / target) * 100)));
  const daysLeft = daysUntil(vault.deadline);

  // Theme color class or style
  const color = vault.color || "#00FFA3";
  let themeClass = "";
  if (color.includes("#00D2FF") || vault.category === "TRAVEL") themeClass = "theme-cyan";
  else if (color.includes("#FF007A") || vault.category === "EMERGENCY") themeClass = "theme-pink";
  else if (color.includes("#A855F7") || vault.category === "LIFESTYLE") themeClass = "theme-violet";

  const isComplete = pct >= 100;
  const isLocked = Boolean(vault.isLocked);

  return `
    <div class="glass-panel-3d cylinder-card" data-vault-id="${vault.vaultId || vault.id}" data-pct="${pct}">
      <div style="width:100%; display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
        <span style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; padding:0.25rem 0.65rem; border-radius:9999px; background:rgba(255,255,255,0.06); font-weight:700; color:${color}; border:1px solid ${color}40;">
          ${vault.category || "TECH"}
        </span>
        <div style="display:flex; align-items:center; gap:0.4rem;">
          ${isLocked ? '<span title="Locked Vault" style="font-size:0.9rem;">🔒</span>' : ''}
          <span style="font-size:0.8rem; color:var(--text-muted);">${daysLeft > 0 ? `${daysLeft}d left` : 'Due today'}</span>
        </div>
      </div>

      <h3 style="font-size:1.1rem; font-weight:700; margin-bottom:0.25rem; text-align:center; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; width:100%;">
        ${vault.title}
      </h3>
      <div style="font-size:0.85rem; color:var(--text-secondary); margin-bottom:0.5rem;">
        <strong style="color:#fff;">${formatCurrency(current)}</strong> of ${formatCurrency(target)}
      </div>

      <!-- 3D Glass Cylinder Vessel -->
      <div class="cylinder-container" id="cyl-${vault.vaultId || vault.id}">
        <div class="cylinder-cap-top"></div>
        <div class="cylinder-vessel">
          <div class="cylinder-ticks">
            <span class="cylinder-tick major" title="100%"></span>
            <span class="cylinder-tick" title="75%"></span>
            <span class="cylinder-tick major" title="50%"></span>
            <span class="cylinder-tick" title="25%"></span>
            <span class="cylinder-tick major" title="0%"></span>
          </div>

          <!-- Dynamic Liquid Element -->
          <div class="cylinder-liquid ${themeClass}" style="height:${pct}%;">
            <!-- Animated Surface Wave -->
            <div class="wave-surface">
              <svg viewBox="0 0 500 150" preserveAspectRatio="none">
                <path class="wave-layer-1" d="M0.00,49.98 C150.00,150.00 349.20,-50.00 500.00,49.98 L500.00,150.00 L0.00,150.00 Z"></path>
                <path class="wave-layer-2" d="M0.00,49.98 C211.37,130.25 298.24,-20.73 500.00,49.98 L500.00,150.00 L0.00,150.00 Z"></path>
              </svg>
            </div>

            <!-- Rising Bubble Particles -->
            <div class="bubble bubble-1"></div>
            <div class="bubble bubble-2"></div>
            <div class="bubble bubble-3"></div>
          </div>

          <!-- Glowing Center Percentage -->
          <div class="liquid-pct-badge">${pct}%</div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div style="width:100%; display:flex; gap:0.5rem; margin-top:0.5rem;">
        <button class="btn-cyber-mint btn-deposit-trigger" data-vault-id="${vault.vaultId || vault.id}" data-vault-title="${vault.title}" style="flex:1; padding:0.55rem; font-size:0.85rem;">
          ⚡ Deposit
        </button>
        ${!isLocked ? `
          <button class="btn-glass-secondary btn-withdraw-trigger" data-vault-id="${vault.vaultId || vault.id}" data-vault-title="${vault.title}" data-max="${current}" style="padding:0.55rem 0.85rem; font-size:0.85rem;">
            Withdraw
          </button>
        ` : `
          <button class="btn-glass-secondary" disabled title="Locked until target or deadline" style="opacity:0.4; cursor:not-allowed; padding:0.55rem 0.85rem; font-size:0.85rem;">
            🔒 Locked
          </button>
        `}
      </div>

      ${isComplete ? `
        <div style="margin-top:0.75rem; width:100%; text-align:center;">
          <button class="btn-cyber-mint btn-celebrate-trigger" data-vault-title="${vault.title}" style="width:100%; padding:0.4rem; font-size:0.8rem; background:linear-gradient(135deg, #FFB800, #FF007A);">
            🎉 100% Unlocked! Celebrate
          </button>
        </div>
      ` : ''}
    </div>
  `;
}

/**
 * 3D Gyro Tilt effect for cursor hover
 */
export function attachGyroTilt(cardElement, maxTilt = 15) {
  if (!cardElement) return;

  function handleMove(e) {
    const rect = cardElement.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = ((y - centerY) / centerY) * -maxTilt;
    const rotateY = ((x - centerX) / centerX) * maxTilt;

    cardElement.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) scale3d(1.02, 1.02, 1.02)`;
  }

  function handleLeave() {
    cardElement.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
  }

  cardElement.addEventListener("mousemove", handleMove);
  cardElement.addEventListener("mouseleave", handleLeave);
}

/**
 * Fullscreen 3D Confetti Burst
 */
export function triggerCelebration(title = "Goal Reached!") {
  let canvas = document.getElementById("confetti-canvas");
  if (!canvas) {
    canvas = document.createElement("canvas");
    canvas.id = "confetti-canvas";
    document.body.appendChild(canvas);
  }

  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const colors = ["#00FFA3", "#00D2FF", "#FF007A", "#FFB800", "#A855F7", "#FFFFFF"];
  const pieces = [];
  const count = 180;

  for (let i = 0; i < count; i++) {
    pieces.push({
      x: canvas.width / 2 + (Math.random() - 0.5) * 200,
      y: canvas.height / 2 + (Math.random() - 0.5) * 100,
      w: Math.random() * 12 + 6,
      h: Math.random() * 8 + 4,
      color: colors[Math.floor(Math.random() * colors.length)],
      vx: (Math.random() - 0.5) * 22,
      vy: Math.random() * -18 - 8,
      rotation: Math.random() * 360,
      vRotation: (Math.random() - 0.5) * 16,
      gravity: 0.45,
      friction: 0.98,
      shape: Math.random() > 0.4 ? "rect" : "circle",
    });
  }

  let animationFrame;
  let startTime = Date.now();

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const elapsed = Date.now() - startTime;

    pieces.forEach((p) => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += p.gravity;
      p.vx *= p.friction;
      p.rotation += p.vRotation;

      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate((p.rotation * Math.PI) / 180);
      ctx.fillStyle = p.color;

      if (p.shape === "circle") {
        ctx.beginPath();
        ctx.arc(0, 0, p.w / 2, 0, Math.PI * 2);
        ctx.fill();
      } else {
        ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
      }
      ctx.restore();
    });

    if (elapsed < 4000) {
      animationFrame = requestAnimationFrame(animate);
    } else {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      cancelAnimationFrame(animationFrame);
    }
  }

  animate();

  // Create celebratory modal banner
  const banner = document.createElement("div");
  banner.className = "celebration-banner";
  banner.innerHTML = `
    <div style="position:fixed; top:20%; left:50%; transform:translateX(-50%); z-index:100000; background:rgba(11,14,23,0.95); border:2px solid #00FFA3; border-radius:24px; padding:2rem 3rem; text-align:center; box-shadow:0 0 50px rgba(0,255,163,0.6); backdrop-filter:blur(25px); animation:celebrationEntry 0.5s cubic-bezier(0.16,1,0.3,1);">
      <div style="font-size:3.5rem; margin-bottom:0.5rem; animation:flamePulse 1s infinite alternate;">🏆 100% UNLOCKED!</div>
      <h2 style="font-family:var(--font-head); font-size:1.8rem; color:#fff; margin-bottom:0.5rem;">
        "${title}" Completed!
      </h2>
      <p style="color:var(--cyber-mint); font-size:1.1rem; font-weight:700;">
        You're officially built different. Your discipline paid off! 👑
      </p>
      <button id="close-celebrate-btn" class="btn-cyber-mint" style="margin-top:1.5rem; padding:0.65rem 2rem;">
        Keep Winning 🚀
      </button>
    </div>
  `;
  document.body.appendChild(banner);

  document.getElementById("close-celebrate-btn")?.addEventListener("click", () => {
    banner.remove();
  });
  setTimeout(() => banner.remove(), 7000);
}
