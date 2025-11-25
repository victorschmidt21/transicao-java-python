// product_delete.js
// Scripts para a página de confirmação de exclusão (product_confirm_delete.html)

document.addEventListener('DOMContentLoaded', function() {
    // Confirmação adicional de exclusão (página dedicada)
    const deleteForm = document.querySelector('form[method="POST"]');
    if (deleteForm) {
        deleteForm.addEventListener('submit', function(e) {
            const productNameEl = document.querySelector('strong');
            const productName = productNameEl ? productNameEl.textContent : '';

            if (!confirm(`Tem certeza absoluta que deseja excluir o produto "${productName}"?\n\nEsta ação não pode ser desfeita.`)) {
                e.preventDefault();
                return false;
            }

            // efeito visual de carregamento no botão
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                const originalText = submitButton.textContent;
                submitButton.textContent = 'Excluindo...';
                submitButton.disabled = true;
                submitButton.style.opacity = '0.7';

                // fallback para restaurar botão caso algo dê errado
                setTimeout(() => {
                    if (submitButton && submitButton.disabled) {
                        submitButton.textContent = originalText;
                        submitButton.disabled = false;
                        submitButton.style.opacity = '1';
                    }
                }, 5000);
            }
        });
    }

    // Destaque no nome do produto
    const productNameEl = document.querySelector('strong');
    if (productNameEl) {
        productNameEl.style.color = '#ef4444';
        productNameEl.style.fontWeight = 'bold';

        let blinkCount = 0;
        const blinkInterval = setInterval(() => {
            productNameEl.style.opacity = productNameEl.style.opacity === '0.5' ? '1' : '0.5';
            blinkCount++;
            if (blinkCount >= 6) {
                clearInterval(blinkInterval);
                productNameEl.style.opacity = '1';
            }
        }, 300);
    }

    // Prevenção de duplo envio
    let isSubmitting = false;
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (isSubmitting) {
                e.preventDefault();
                return false;
            }
            isSubmitting = true;
        });
    }

    // Atalho ESC para voltar para a lista
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const cancelButton = document.querySelector('a[href*="product_list"]');
            if (cancelButton) {
                cancelButton.click();
            }
        }
    });

    // Animação de entrada
    const container = document.querySelector('.form-container');
    if (container) {
        container.style.animation = 'fadeIn 0.3s ease-in';
    }
});

// Adiciona keyframes de animação se necessário
(function injectStyles(){
    if (document.getElementById('product-delete-animations')) return;
    const style = document.createElement('style');
    style.id = 'product-delete-animations';
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .form-container { animation: fadeIn 0.3s ease-in; }
    `;
    document.head.appendChild(style);
})();
