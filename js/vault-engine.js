// ============================================================
// VAULT.FI — MODERN FINTECH VAULT ENGINE
// Stripe / Linear / Revolut Inspired Visual Components
// ============================================================

import { formatCurrency, calcProgress, daysUntil } from "./utils.js";

/**
 * Renders a modern Silicon Valley fintech Vault card
 * @param {Object} vault - Vault record
 */
export function createVaultCardHTML(vault) {
  const current = Number(vault.currentAmount) || 0;
  const target = Math.max(1, Number(vault.targetAmount) || 1);
  const pct = Math.min(100, Math.max(0, Math.round((current / target) * 100)));
  const daysLeft = daysUntil(vault.deadline);
  const isLocked = Boolean(vault.isLocked);
  const isComplete = pct >= 100;

  // Category styling
  const categoryLabels = {
    TECH: { label: "Technology", bg: "#EFF6FF", text: "#2563EB" },
    TRAVEL: { label: "Travel Reserve", bg: "#F0FDF4", text: "#16A34A" },
    EMERGENCY: { label: "Emergency Safety", bg: "#FEF2F2", text: "#DC2626" },
    LIFESTYLE: { label: "Lifestyle Goal", bg: "#FAF5FF", text: "#9333EA" },
  };
  const cat = categoryLabels[vault.category] || { label: vault.category || "Savings", bg: "#F1F5F9", text: "#475569" };

  return `
    <div class="stripe-card" data-vault-id="${vault.vaultId || vault.id}" style="padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between;">
      
      <div>
        <!-- Card Top Pill Badges -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <span style="font-size: 0.75rem; font-weight: 700; color: ${cat.text}; background: ${cat.bg}; padding: 0.25rem 0.75rem; border-radius: 9999px;">
            ${cat.label}
          </span>
          <span style="font-size: 0.8rem; color: #64748B; font-weight: 500;">
            ${daysLeft > 0 ? `${daysLeft} days left` : 'Due today'} ${isLocked ? '• 🔒 Locked' : ''}
          </span>
        </div>

        <!-- Title -->
        <h3 style="font-size: 1.25rem; font-weight: 700; color: #0F172A; margin: 0 0 0.5rem; letter-spacing: -0.02em;">
          ${vault.title}
        </h3>

        <!-- Amount Overview -->
        <div style="display: flex; align-items: baseline; gap: 0.4rem; margin-bottom: 1.25rem;">
          <span style="font-size: 1.75rem; font-weight: 800; color: #0F172A; letter-spacing: -0.03em;">
            ${formatCurrency(current)}
          </span>
          <span style="font-size: 0.9rem; color: #64748B; font-weight: 500;">
            of ${formatCurrency(target)}
          </span>
        </div>

        <!-- Modern Progress Bar & Percentage Pill -->
        <div style="margin-bottom: 1.5rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem; font-size: 0.85rem;">
            <span style="color: #64748B; font-weight: 500;">Goal Progress</span>
            <span style="font-weight: 700; color: #2563EB;">${pct}%</span>
          </div>
          <div class="progress-bar-track">
            <div class="progress-bar-fill" style="width: ${pct}%;"></div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
          <button class="btn-primary-blue btn-deposit-trigger" data-vault-id="${vault.vaultId || vault.id}" data-vault-title="${vault.title}">
            + Add Funds
          </button>
          ${!isLocked ? `
            <button class="btn-secondary-white btn-withdraw-trigger" data-vault-id="${vault.vaultId || vault.id}" data-vault-title="${vault.title}" data-max="${current}">
              Withdraw
            </button>
          ` : `
            <button class="btn-secondary-white" disabled style="opacity: 0.5; cursor: not-allowed;">
              🔒 Locked
            </button>
          `}
        </div>

        ${isComplete ? `
          <div style="margin-top: 0.75rem; background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 10px; padding: 0.5rem; text-align: center;">
            <span style="font-size: 0.8rem; font-weight: 700; color: #059669;">
              🎉 100% Goal Target Achieved!
            </span>
          </div>
        ` : ''}
      </div>

    </div>
  `;
}
