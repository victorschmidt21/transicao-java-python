// product_form.js
// Validações e máscaras do formulário de produtos

document.addEventListener('DOMContentLoaded', function() {
    const priceInput = document.querySelector('input[name="price"]');
    const qtyInput = document.querySelector('input[name="qty_stock"]');
    const descriptionInput = document.querySelector('input[name="description"]');
    const form = document.querySelector('.form-container form');

    // Mascara simples para preço: permite apenas números e ponto, formata com 2 decimais ao perder foco
    if (priceInput) {
        priceInput.addEventListener('input', function(e) {
            // permite dígitos e ponto
            this.value = this.value.replace(/[^0-9.,]/g, '').replace(',', '.');
        });

        priceInput.addEventListener('blur', function() {
            if (!this.value) return;
            const n = parseFloat(this.value);
            if (!isNaN(n)) {
                this.value = n.toFixed(2);
            }
        });
    }

    // Garantir que qty seja inteiro não-negativo
    if (qtyInput) {
        qtyInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '');
        });
    }

    // Validar descrição mínima no cliente (servidor valida também)
    if (descriptionInput) {
        descriptionInput.addEventListener('blur', function() {
            const v = this.value.trim();
            if (v.length > 0 && v.length < 3) {
                showFieldError(this, 'Descrição muito curta');
            } else {
                clearFieldError(this);
            }
        });
    }

    // Prevent submit se tiver erros simples no front
    if (form) {
        form.addEventListener('submit', function(e) {
            let hasError = false;

            // checar descrição
            if (descriptionInput) {
                const v = descriptionInput.value.trim();
                if (!v || v.length < 3) {
                    showFieldError(descriptionInput, 'Descrição inválida');
                    hasError = true;
                }
            }

            // checar price
            if (priceInput) {
                const v = priceInput.value.replace(',', '.');
                const n = parseFloat(v);
                if (isNaN(n) || n <= 0) {
                    showFieldError(priceInput, 'Preço inválido');
                    hasError = true;
                } else {
                    // formata antes de enviar
                    priceInput.value = n.toFixed(2);
                }
            }

            // checar qty
            if (qtyInput) {
                const q = parseInt(qtyInput.value || '0', 10);
                if (isNaN(q) || q < 0) {
                    showFieldError(qtyInput, 'Quantidade inválida');
                    hasError = true;
                }
            }

            if (hasError) {
                e.preventDefault();
                showNotification('Corrija os erros do formulário', 'error');
                return false;
            }

            // desabilitar botões para prevenir duplo submit
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Salvando...';
            }
        });
    }
});

// Reaproveita funções do cliente para mostrar/limpar erro e notificação

function showFieldError(field, message) {
    clearFieldError(field);

    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.color = '#ef4444';
    errorDiv.style.fontSize = '0.875rem';
    errorDiv.style.marginTop = '0.25rem';

    field.parentNode.appendChild(errorDiv);
    field.style.borderColor = '#ef4444';
}

function clearFieldError(field) {
    if (!field || !field.parentNode) return;
    const existingError = field.parentNode.querySelector('.error-message');
    if (existingError) existingError.remove();
    field.style.borderColor = '#374151';
}

// Notificações simples — mesma função usada na lista, se já existir será reaproveitada
function showNotification(message, type = 'info') {
    // se já existe a função global (ex.: lista), usa ela
    if (typeof window.showNotification === 'function') {
        window.showNotification(message, type);
        return;
    }

    // senão, cria uma notificação temporária
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <div class="notification-icon">${type === 'success' ? '✓' : '!'}</div>
            <div class="notification-message">${message}</div>
            <button class="notification-close" title="Fechar">×</button>
        </div>
    `;
    // estilos básicos
    if (!document.querySelector('#product-notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'product-notification-styles';
        styles.textContent = `
            .notification { position: fixed; top: 20px; right: 20px; z-index: 10000; max-width: 400px; border-radius: 8px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); padding: 12px; }
            .notification-success { background: #10b981; color: white; }
            .notification-error { background: #ef4444; color: white; }
            .notification-content { display:flex; gap:12px; align-items:center; }
            .notification-close { background: none; border: none; color: inherit; cursor:pointer; font-size: 16px; }
        `;
        document.head.appendChild(styles);
    }

    document.body.appendChild(notification);
    notification.querySelector('.notification-close').addEventListener('click', () => notification.remove());
    setTimeout(() => { if (notification.parentElement) notification.remove(); }, 5000);
}
