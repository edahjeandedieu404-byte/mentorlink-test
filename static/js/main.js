

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
// ── DARK MODE ──
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);
    updateThemeIcon(isDark);
}

function updateThemeIcon(isDark) {
    const icon = document.getElementById('theme-icon');
    if (icon) {
        icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
        icon.style.color = isDark ? '#f39c12' : 'var(--gray-600)';
    }
}

// Appliquer le dark mode au chargement
const savedDarkMode = localStorage.getItem('darkMode');
if (savedDarkMode === 'true') {
    document.body.classList.add('dark-mode');
    updateThemeIcon(true);
}

// ── SWITCH LANGUE ──
const translations = {
    fr: {
        'dashboard': 'Tableau de bord',
        'offer_mentoring': 'Offrir mentorat',
        'find_mentor': 'Chercher mentor',
        'my_mentors': 'Mes mentors',
        'my_mentees': 'Mes mentorés',
        'matching_history': 'Historique matching',
        'messages': 'Messages',
        'my_profile': 'Mon profil',
        'logout': 'Déconnexion',
        'btn_new': '+ Nouvelle',
        'no_offer': 'Aucune offre publiée',
        'no_demand': 'Aucune demande en cours',
        'no_mentor': 'Aucun mentor associé',
        'no_mentee': 'Aucun mentoré associé',
    },
    en: {
        'dashboard': 'Dashboard',
        'offer_mentoring': 'Offer mentoring',
        'find_mentor': 'Find mentor',
        'my_mentors': 'My mentors',
        'my_mentees': 'My mentees',
        'matching_history': 'Matching history',
        'messages': 'Messages',
        'my_profile': 'My profile',
        'logout': 'Logout',
        'btn_new': '+ New',
        'no_offer': 'No published offer',
        'no_demand': 'No active request',
        'no_mentor': 'No mentor yet',
        'no_mentee': 'No mentee yet',
    }
};

function setLang(lang) {
    localStorage.setItem('lang', lang);

    // Mettre à jour les boutons
    document.getElementById('btn-fr').classList.toggle('active', lang === 'fr');
    document.getElementById('btn-en').classList.toggle('active', lang === 'en');

    // Traduire les éléments avec data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });
}

// Appliquer la langue sauvegardée
const savedLang = localStorage.getItem('lang') || 'fr';
document.addEventListener('DOMContentLoaded', function() {
    setLang(savedLang);
});