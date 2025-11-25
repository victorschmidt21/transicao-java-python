// product_list.js
// Scripts para a lista de produtos (busca local, modal de exclusão, delete via fetch, ordenação)

document.addEventListener('DOMContentLoaded', function() {
    // Busca em tempo real (client-side)
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function(e) {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => performSearch(e.target.value), 300);
        });
    }

    // Modal de exclusão
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const modal = document.getElementById('deleteModal');
    const cancelButton = document.getElementById('cancelDelete');
    const confirmButton = document.getElementById('confirmDelete');
    const productNameElement = document.querySelector('.product-name');

    let productToDelete = null;

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            productToDelete = {
                id: this.getAttribute('data-product-id'),
                name: this.getAttribute('data-product-name')
            };

            if (productNameElement) productNameElement.textContent = `Produto: ${productToDelete.name}`;

            // mostrar modal
            if (modal) {
                modal.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            }
        });
    });

    // cancelar modal
    if (cancelButton) {
        cancelButton.addEventListener('click', function() {
            closeModal();
        });
    }

    // confirmar exclusão (usa DELETE)
    if (confirmButton) {
        confirmButton.addEventListener('click', function() {
            if (!productToDelete) return;

            const originalText = confirmButton.textContent;
            confirmButton.textContent = 'Excluindo...';
            confirmButton.disabled = true;

            const csrfTokenEl = document.querySelector('[name=csrfmiddlewaretoken]');
            const csrfToken = csrfTokenEl ? csrfTokenEl.value : '';

            fetch(`/product/delete/${productToDelete.id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (response.ok) {
                    // fechar modal
                    closeModal();

                    // notificação de sucesso
                    showNotification('Produto excluído com sucesso!', 'success');

                    // remover linha da tabela
                    const triggerBtn = document.querySelector(`button[data-product-id="${productToDelete.id}"]`);
                    if (triggerBtn) {
                        const tr = triggerBtn.closest('tr');
                        if (tr) {
                            tr.style.transition = 'opacity 0.3s ease';
                            tr.style.opacity = '0';
                            setTimeout(() => tr.remove(), 300);
                        }
                    }

                    productToDelete = null;
                } else {
                    showNotification('Erro ao excluir produto', 'error');
                }
            })
            .catch(err => {
                console.error('Erro ao excluir produto:', err);
                showNotification('Erro ao excluir produto', 'error');
            })
            .finally(() => {
                confirmButton.textContent = originalText;
                confirmButton.disabled = false;
            });
        });
    }

    // Fechar modal clicando fora
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) closeModal();
        });
    }

    // ESC para fechar modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal && modal.style.display === 'flex') {
            closeModal();
        }
    });

    // Destaque linhas
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#374151';
        });
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    // Ordenação simples por coluna (exceto Ações)
    const tableHeaders = document.querySelectorAll('.data-table th');
    tableHeaders.forEach(header => {
        if (header.textContent.trim() !== 'Ações') {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(this);
            });
        }
    });
});

// Funções utilitárias

function closeModal() {
    const modal = document.getElementById('deleteModal');
    if (!modal) return;
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Busca client-side
function performSearch(query) {
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    const searchTerm = query.toLowerCase();

    tableRows.forEach(row => {
        const cells = row.querySelectorAll('td');
        let found = false;
        cells.forEach(cell => {
            if (cell.textContent.toLowerCase().includes(searchTerm)) found = true;
        });
        row.style.display = found || searchTerm === '' ? '' : 'none';
    });
}

// Ordenação de tabela
function sortTable(header) {
    const table = header.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    const isAscending = header.classList.contains('sort-asc');

    table.querySelectorAll('th').forEach(th => th.classList.remove('sort-asc', 'sort-desc'));

    rows.sort((a, b) => {
        const aText = a.children[columnIndex].textContent.trim();
        const bText = b.children[columnIndex].textContent.trim();
        return isAscending ? bText.localeCompare(aText) : aText.localeCompare(bText);
    });

    rows.forEach(r => tbody.appendChild(r));
    header.classList.add(isAscending ? 'sort-desc' : 'sort-asc');
}

// Exportar CSV
function exportToCSV(filename = 'produtos.csv') {
    const table = document.querySelector('.data-table');
    if (!table) return;
    const rows = Array.from(table.querySelectorAll('tr'));
    let csv = '';
    rows.forEach(row => {
        const cols = Array.from(row.querySelectorAll('th, td'));
        const rowData = cols.map(cell => `"${cell.textContent.trim().replace(/"/g, '""')}"`).join(',');
        csv += rowData + '\n';
    });

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

// Notificações (se não houver global)
function showNotification(message, type = 'info') {
    if (typeof window.showNotification === 'function') {
        window.showNotification(message, type);
        return;
    }

    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <div class="notification-icon">${type === 'success' ? '✓' : '!'}</div>
            <div class="notification-message">${message}</div>
            <button class="notification-close" title="Fechar">×</button>
        </div>
    `;

    if (!document.querySelector('#product-notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'product-notification-styles';
        styles.textContent = `
            .notification { position: fixed; top: 20px; right: 20px; z-index: 10000; max-width: 400px; border-radius: 8px; padding: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); }
            .notification-success { background: #10b981; color: #fff; }
            .notification-error { background: #ef4444; color: #fff; }
            .notification-content { display:flex; gap:12px; align-items:center; }
            .notification-close { background:none; border:none; color:inherit; cursor:pointer; font-size:16px; }
        `;
        document.head.appendChild(styles);
    }

    document.body.appendChild(notification);
    notification.querySelector('.notification-close').addEventListener('click', () => notification.remove());
    setTimeout(() => { if (notification.parentElement) notification.remove(); }, 5000);
}
