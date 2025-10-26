// Scripts para a página de confirmação de exclusão

document.addEventListener('DOMContentLoaded', function() {
    // Confirmação adicional de exclusão
    const deleteForm = document.querySelector('form[method="POST"]');
    if (deleteForm) {
        deleteForm.addEventListener('submit', function(e) {
            const customerName = document.querySelector('strong').textContent;
            
            if (!confirm(`Tem certeza absoluta que deseja excluir o cliente "${customerName}"?\n\nEsta ação não pode ser desfeita.`)) {
                e.preventDefault();
                return false;
            }
            
            // Adiciona efeito visual de carregamento
            const submitButton = this.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            
            submitButton.textContent = 'Excluindo...';
            submitButton.disabled = true;
            submitButton.style.opacity = '0.7';
            
            // Se o usuário cancelar, restaura o botão
            setTimeout(() => {
                if (submitButton.disabled) {
                    submitButton.textContent = originalText;
                    submitButton.disabled = false;
                    submitButton.style.opacity = '1';
                }
            }, 5000);
        });
    }

    // Efeito de destaque no nome do cliente
    const customerName = document.querySelector('strong');
    if (customerName) {
        customerName.style.color = '#ef4444';
        customerName.style.fontWeight = 'bold';
        
        // Adiciona animação de piscar
        let blinkCount = 0;
        const blinkInterval = setInterval(() => {
            customerName.style.opacity = customerName.style.opacity === '0.5' ? '1' : '0.5';
            blinkCount++;
            
            if (blinkCount >= 6) {
                clearInterval(blinkInterval);
                customerName.style.opacity = '1';
            }
        }, 300);
    }

    // Prevenção de duplo clique
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

    // Atalho de teclado para cancelar (ESC)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const cancelButton = document.querySelector('a[href*="customer_list"]');
            if (cancelButton) {
                cancelButton.click();
            }
        }
    });

    // Adiciona classe de animação ao container
    const container = document.querySelector('.form-container');
    if (container) {
        container.style.animation = 'fadeIn 0.3s ease-in';
    }
});

// Adiciona estilos de animação
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .form-container {
        animation: fadeIn 0.3s ease-in;
    }
`;
document.head.appendChild(style);
