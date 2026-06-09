
document.addEventListener('DOMContentLoaded', function () {

    // ── SIDEBAR TOGGLE (mobile) ──
    const sidebar = document.querySelector('.sidebar');
    const toggle = document.querySelector('.sidebar-toggle');
    const overlay = document.querySelector('.sidebar-overlay');

    if (toggle) {
        toggle.addEventListener('click', function () {
            sidebar.classList.toggle('open');
            overlay.classList.toggle('open');
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function () {
            sidebar.classList.remove('open');
            overlay.classList.remove('open');
        });
    }

    // ── ACTIVE NAV ITEM ──
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');

    navItems.forEach(item => {
        const href = item.getAttribute('href');
        if (href && currentPath.startsWith(href)) {
            item.classList.add('active');
        }
    });

    // ── AUTO SCROLL CHAT ──
    const chatMessages = document.querySelector('.chat-messages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // ── ALERTS AUTO DISMISS ──
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            alert.style.transition = 'all 0.4s ease';
            setTimeout(() => alert.remove(), 400);
        }, 4000);
    });

    // ── SCORE RING ANIMATION ──
    const rings = document.querySelectorAll('.score-ring circle.progress');
    rings.forEach(ring => {
        const score = parseFloat(ring.dataset.score) || 0;
        const radius = parseFloat(ring.getAttribute('r'));
        const circumference = 2 * Math.PI * radius;
        ring.style.strokeDasharray = circumference;
        ring.style.strokeDashoffset = circumference;
        setTimeout(() => {
            const offset = circumference - (score / 100) * circumference;
            ring.style.transition = 'stroke-dashoffset 1s ease';
            ring.style.strokeDashoffset = offset;
        }, 300);
    });

    // ── FORM INPUT STYLING ──
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        if (!input.classList.contains('form-control')) {
            input.classList.add('form-control');
        }
    });

    // ── TOPBAR TITLE ──
    const pageTitle = document.querySelector('.page-title');
    if (pageTitle) {
        const topbarTitle = document.querySelector('.topbar-title');
        if (topbarTitle) {
            topbarTitle.textContent = pageTitle.textContent;
        }
    }

});
