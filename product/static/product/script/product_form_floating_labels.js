// product_form_floating_labels.js
// Floating labels (mesma lógica do customers, reaproveitável)

document.addEventListener('DOMContentLoaded', function() {
    function handleFloatingLabel(input) {
        const label = input.nextElementSibling;
        if (label && label.tagName === 'LABEL') {
            if (input.value.trim() !== '' || input === document.activeElement) {
                label.classList.add('floating');
            } else {
                label.classList.remove('floating');
            }
        }
    }

    // Função global para atualizar labels de campos específicos
    window.updateFloatingLabels = function(fieldIds) {
        fieldIds.forEach(fieldId => {
            const input = document.getElementById(fieldId);
            if (input) handleFloatingLabel(input);
        });
    };

    const inputs = document.querySelectorAll('.floating-label input, .floating-label select');

    inputs.forEach(input => {
        // estado inicial
        handleFloatingLabel(input);

        input.addEventListener('focus', function() {
            const label = this.nextElementSibling;
            if (label && label.tagName === 'LABEL') label.classList.add('floating');
        });

        input.addEventListener('blur', function() {
            handleFloatingLabel(this);
        });

        input.addEventListener('input', function() {
            handleFloatingLabel(this);
        });

        input.addEventListener('change', function() {
            handleFloatingLabel(this);
        });
    });
});
