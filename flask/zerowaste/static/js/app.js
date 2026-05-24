// ── Toast auto-dismiss ────────────────────────────────────────────────────────
document.querySelectorAll('.toast').forEach(t => setTimeout(() => t.remove(), 4200));

// ── Modal helpers ─────────────────────────────────────────────────────────────
function openModal(id)  { document.getElementById(id).classList.remove('hidden'); }
function closeModal(id) { document.getElementById(id).classList.add('hidden'); }

document.addEventListener('click', e => {
    if (e.target.classList.contains('modal')) {
        e.target.classList.add('hidden');
    }
});

// ── Notification panel ────────────────────────────────────────────────────────
function toggleNotif() {
    const panel = document.getElementById('notif-panel');
    panel.classList.toggle('open');
    if (panel.classList.contains('open')) {
        fetch('/notifications/read').then(() => {
            const badge = document.getElementById('notif-badge');
            if (badge) badge.remove();
        });
    }
}

// ── Confirm delete ────────────────────────────────────────────────────────────
function confirmAction(msg, url) {
    if (confirm(msg)) window.location.href = url;
}

// ── Expiry countdown ──────────────────────────────────────────────────────────
function formatExpiry(expiryStr) {
    const now    = new Date();
    const expiry = new Date(expiryStr);
    const diff   = expiry - now;
    if (diff <= 0) return { text: 'Expired', cls: 'expiry-urgent' };
    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    if (h < 2)  return { text: `${h}h ${m}m left`, cls: 'expiry-urgent' };
    if (h < 12) return { text: `${h}h ${m}m left`, cls: 'expiry-soon' };
    return { text: `${h}h left`, cls: 'expiry-ok' };
}

document.querySelectorAll('[data-expiry]').forEach(el => {
    const { text, cls } = formatExpiry(el.dataset.expiry);
    el.textContent = text;
    el.className   = cls;
});

// ── Live search filter (client-side) ─────────────────────────────────────────
const searchInput = document.getElementById('live-search');
if (searchInput) {
    searchInput.addEventListener('input', function () {
        const q = this.value.toLowerCase();
        document.querySelectorAll('[data-searchable]').forEach(row => {
            row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
        });
    });
}

// ── Claim modal ───────────────────────────────────────────────────────────────
function openClaimModal(foodId, title) {
    document.getElementById('claim-food-id').value = foodId;
    document.getElementById('claim-food-title').textContent = title;
    openModal('claim-modal');
}

// ── Assign volunteer modal ────────────────────────────────────────────────────
function openAssignModal(claimId) {
    document.getElementById('assign-claim-id').value = claimId;
    openModal('assign-modal');
}

// ── Chart helper (simple bar using CSS) ──────────────────────────────────────
function renderBarChart(canvasId, labels, values, color = '#16a34a') {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx    = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    const max = Math.max(...values, 1);
    const barW = (W - 40) / labels.length - 10;
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, W, H);
    labels.forEach((lbl, i) => {
        const x   = 20 + i * (barW + 10);
        const bh  = ((values[i] / max) * (H - 50));
        const y   = H - 30 - bh;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.roundRect(x, y, barW, bh, 4);
        ctx.fill();
        ctx.fillStyle = '#64748b';
        ctx.font = '11px Segoe UI';
        ctx.textAlign = 'center';
        ctx.fillText(lbl, x + barW / 2, H - 10);
        ctx.fillStyle = '#0f172a';
        ctx.font = 'bold 11px Segoe UI';
        ctx.fillText(values[i], x + barW / 2, y - 5);
    });
}
