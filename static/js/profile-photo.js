/**
 * Gestion de l'affichage de la checkbox "Supprimer la photo"
 * Met la checkbox et le label sur la même ligne
 */

document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.querySelector('input[name="profile_photo-clear"]');
    const label = document.querySelector('label[for="profile_photo-clear_id"]');

    if (checkbox && label) {
        // Crée un wrapper flex pour aligner checkbox + label
        const wrapper = document.createElement('div');
        wrapper.id = 'photo-clear-wrapper';

        // Insère le wrapper avant la checkbox
        checkbox.parentNode.insertBefore(wrapper, checkbox);

        // Déplace checkbox et label dans le wrapper
        wrapper.appendChild(checkbox);
        wrapper.appendChild(label);
    }
});