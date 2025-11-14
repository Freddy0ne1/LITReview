// ==========================================
// SYSTÈME DE GESTION DES MODALES
// ==========================================

// ⭐ HELPER : Désactiver le scroll
function disableScroll() {
    // Sauvegarder la position actuelle
    const scrollY = window.scrollY;

    // Bloquer le scroll sur html et body
    document.documentElement.style.overflow = 'hidden';
    document.body.style.overflow = 'hidden';

    // Fixer la position pour éviter le saut
    document.body.style.position = 'fixed';
    document.body.style.top = `-${scrollY}px`;
    document.body.style.width = '100%';
}

// ⭐ HELPER : Réactiver le scroll
function enableScroll() {
    // Récupérer la position sauvegardée
    const scrollY = document.body.style.top;

    // Réinitialiser les styles
    document.documentElement.style.overflow = '';
    document.body.style.overflow = '';
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.width = '';

    // Restaurer la position de scroll
    if (scrollY) {
        window.scrollTo(0, parseInt(scrollY || '0') * -1);
    }
}

// ==========================================
// MODALE DE DÉSABONNEMENT
// ==========================================

function openUnfollowModal(userId, username) {
    const modal = document.getElementById('unfollowModal');
    const usernameSpan = document.getElementById('unfollowUsername');
    const form = document.getElementById('unfollowForm');

    if (modal && usernameSpan && form) {
        usernameSpan.textContent = username;
        form.action = `/accounts/unfollow/${userId}/`;
        modal.classList.remove('hidden');

        // ⭐ Désactiver le scroll
        disableScroll();

        const firstButton = modal.querySelector('button');
        if (firstButton) firstButton.focus();
    }
}

function closeUnfollowModal() {
    const modal = document.getElementById('unfollowModal');
    if (modal) {
        modal.classList.add('hidden');

        // ⭐ Réactiver le scroll
        enableScroll();
    }
}

// ==========================================
// MODALE DE BLOCAGE
// ==========================================

function openBlockModal(userId, username) {
    const modal = document.getElementById('blockModal');
    const usernameSpan = document.getElementById('blockUsername');
    const form = document.getElementById('blockForm');

    if (modal && usernameSpan && form) {
        usernameSpan.textContent = username;
        form.action = `/accounts/block/${userId}/`;
        modal.classList.remove('hidden');

        disableScroll();

        const firstButton = modal.querySelector('button');
        if (firstButton) firstButton.focus();
    }
}

function closeBlockModal() {
    const modal = document.getElementById('blockModal');
    if (modal) {
        modal.classList.add('hidden');
        enableScroll();
    }
}

// ==========================================
// MODALE DE DÉBLOCAGE
// ==========================================

function openUnblockModal(userId, username) {
    const modal = document.getElementById('unblockModal');
    const usernameSpan = document.getElementById('unblockUsername');
    const form = document.getElementById('unblockForm');

    if (modal && usernameSpan && form) {
        usernameSpan.textContent = username;
        form.action = `/accounts/unblock/${userId}/`;
        modal.classList.remove('hidden');

        disableScroll();

        const firstButton = modal.querySelector('button');
        if (firstButton) firstButton.focus();
    }
}

function closeUnblockModal() {
    const modal = document.getElementById('unblockModal');
    if (modal) {
        modal.classList.add('hidden');
        enableScroll();
    }
}

// ==========================================
// MODALE DE SUPPRESSION DE TICKET
// ==========================================

function openDeleteTicketModal(ticketId, ticketTitle) {
    const modal = document.getElementById('deleteTicketModal');
    const titleSpan = document.getElementById('deleteTicketTitle');
    const form = document.getElementById('deleteTicketForm');

    if (modal && titleSpan && form) {
        titleSpan.textContent = ticketTitle;
        form.action = `/blog/ticket/${ticketId}/delete/`;
        modal.classList.remove('hidden');

        disableScroll();

        const firstButton = modal.querySelector('button');
        if (firstButton) firstButton.focus();
    }
}

function closeDeleteTicketModal() {
    const modal = document.getElementById('deleteTicketModal');
    if (modal) {
        modal.classList.add('hidden');
        enableScroll();
    }
}

// ==========================================
// MODALE DE SUPPRESSION DE CRITIQUE
// ==========================================

function openDeleteReviewModal(reviewId, reviewHeadline) {
    const modal = document.getElementById('deleteReviewModal');
    const headlineSpan = document.getElementById('deleteReviewHeadline');
    const form = document.getElementById('deleteReviewForm');

    if (modal && headlineSpan && form) {
        headlineSpan.textContent = reviewHeadline;
        form.action = `/blog/review/${reviewId}/delete/`;
        modal.classList.remove('hidden');

        disableScroll();

        const firstButton = modal.querySelector('button');
        if (firstButton) firstButton.focus();
    }
}

function closeDeleteReviewModal() {
    const modal = document.getElementById('deleteReviewModal');
    if (modal) {
        modal.classList.add('hidden');
        enableScroll();
    }
}

// ==========================================
// GESTIONNAIRES D'ÉVÉNEMENTS GLOBAUX
// ==========================================

document.addEventListener('DOMContentLoaded', function() {

    // Empêcher la fermeture au clic extérieur
    const modals = [
        'unfollowModal',
        'blockModal',
        'unblockModal',
        'deleteTicketModal',
        'deleteReviewModal'
    ];

    modals.forEach(modalId => {
        const modal = document.getElementById(modalId);
        if (modal) {
            const modalContent = modal.querySelector('div > div');
            if (modalContent) {
                modalContent.addEventListener('click', function(event) {
                    event.stopPropagation();
                });
            }
        }
    });

    // Fermer les modales avec Escape
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeUnfollowModal();
            closeBlockModal();
            closeUnblockModal();
            closeDeleteTicketModal();
            closeDeleteReviewModal();
        }
    });
});