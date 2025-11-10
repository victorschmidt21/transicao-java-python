// Scripts para a lista de clientes

document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidade de busca em tempo real
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function(e) {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                performSearch(e.target.value);
            }, 300);
        });
    }

    // Funcionalidade do modal de confirmação de exclusão
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const modal = document.getElementById('deleteModal');
    const cancelButton = document.getElementById('cancelDelete');
    const confirmButton = document.getElementById('confirmDelete');
    const customerNameElement = document.querySelector('.customer-name');
    
    let customerToDelete = null;

    // Interceptar cliques nos botões de excluir
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            customerToDelete = {
                id: this.getAttribute('data-customer-id'),
                name: this.getAttribute('data-customer-name')
            };
            
            // Atualizar o nome do cliente no modal
            customerNameElement.textContent = `Cliente: ${customerToDelete.name}`;
            
            // Mostrar o modal
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    });

    // Fechar modal ao clicar em cancelar
    cancelButton.addEventListener('click', function() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        customerToDelete = null;
    });

    // Confirmar exclusão
    confirmButton.addEventListener('click', function() {
        if (customerToDelete) {
            // Mostrar loading no botão
            const originalText = confirmButton.textContent;
            confirmButton.textContent = 'Excluindo...';
            confirmButton.disabled = true;
            
            // Fazer requisição DELETE
            fetch(`/customers/delete/${customerToDelete.id}/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (response.ok) {
                    // Fechar modal
                    modal.style.display = 'none';
                    document.body.style.overflow = 'auto';
                    
                    // Mostrar notificação de sucesso
                    showNotification('Cliente excluído com sucesso!', 'success');
                    
                    // Remover linha da tabela
                    const tableRow = document.querySelector(`button[data-customer-id="${customerToDelete.id}"]`).closest('tr');
                    if (tableRow) {
                        tableRow.style.transition = 'opacity 0.3s ease';
                        tableRow.style.opacity = '0';
                        setTimeout(() => {
                            tableRow.remove();
                        }, 300);
                    }
                    
                    customerToDelete = null;
                } else {
                    // Mostrar notificação de erro
                    showNotification('Erro ao excluir cliente', 'error');
                }
            })
            .catch(error => {
                console.error('Erro ao excluir cliente:', error);
                showNotification('Erro ao excluir cliente', 'error');
            })
            .finally(() => {
                // Restaurar botão
                confirmButton.textContent = originalText;
                confirmButton.disabled = false;
            });
        }
    });

    // Fechar modal ao clicar fora dele
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            customerToDelete = null;
        }
    });

    // Fechar modal com tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            customerToDelete = null;
        }
    });

    // Destaque de linhas na tabela
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = '#374151';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });

    // Ordenação de colunas (funcionalidade básica)
    const tableHeaders = document.querySelectorAll('.data-table th');
    tableHeaders.forEach(header => {
        if (header.textContent !== 'Ações') {
            header.style.cursor = 'pointer';
            header.addEventListener('click', function() {
                sortTable(this);
            });
        }
    });
});

// Função para realizar busca
function performSearch(query) {
    const tableRows = document.querySelectorAll('.data-table tbody tr');
    const searchTerm = query.toLowerCase();
    
    tableRows.forEach(row => {
        const cells = row.querySelectorAll('td');
        let found = false;
        
        cells.forEach(cell => {
            if (cell.textContent.toLowerCase().includes(searchTerm)) {
                found = true;
            }
        });
        
        if (found || searchTerm === '') {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Função para ordenar tabela
function sortTable(header) {
    const table = header.closest('table');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = Array.from(header.parentNode.children).indexOf(header);
    
    const isAscending = header.classList.contains('sort-asc');
    
    // Remove classes de ordenação de todos os headers
    table.querySelectorAll('th').forEach(th => {
        th.classList.remove('sort-asc', 'sort-desc');
    });
    
    // Ordena as linhas
    rows.sort((a, b) => {
        const aText = a.children[columnIndex].textContent.trim();
        const bText = b.children[columnIndex].textContent.trim();
        
        if (isAscending) {
            return bText.localeCompare(aText);
        } else {
            return aText.localeCompare(bText);
        }
    });
    
    // Reordena as linhas na tabela
    rows.forEach(row => tbody.appendChild(row));
    
    // Adiciona classe de ordenação
    header.classList.add(isAscending ? 'sort-desc' : 'sort-asc');
}

// Função para exportar dados (funcionalidade adicional)
function exportToCSV() {
    const table = document.querySelector('.data-table');
    const rows = Array.from(table.querySelectorAll('tr'));
    
    let csv = '';
    rows.forEach(row => {
        const cells = Array.from(row.querySelectorAll('th, td'));
        const rowData = cells.map(cell => `"${cell.textContent.trim()}"`).join(',');
        csv += rowData + '\n';
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'clientes.csv';
    a.click();
    window.URL.revokeObjectURL(url);
}

// Função para mostrar notificações
function showNotification(message, type = 'info') {
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <div class="notification-icon">
                ${type === 'success' ? 
                    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' :
                    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 9V13M12 17H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                }
            </div>
            <div class="notification-message">${message}</div>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
        </div>
    `;
    
    // Adicionar estilos se não existirem
    if (!document.querySelector('#notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 10000;
                max-width: 400px;
                border-radius: 8px;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
                animation: slideInRight 0.3s ease-out;
            }
            
            .notification-success {
                background: #10b981;
                color: white;
            }
            
            .notification-error {
                background: #ef4444;
                color: white;
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                padding: 16px;
                gap: 12px;
            }
            
            .notification-icon {
                flex-shrink: 0;
            }
            
            .notification-message {
                flex: 1;
                font-weight: 500;
            }
            
            .notification-close {
                background: none;
                border: none;
                color: inherit;
                cursor: pointer;
                padding: 4px;
                border-radius: 4px;
                transition: background 0.2s;
            }
            
            .notification-close:hover {
                background: rgba(255, 255, 255, 0.2);
            }
            
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @media (max-width: 768px) {
                .notification {
                    top: 10px;
                    right: 10px;
                    left: 10px;
                    max-width: none;
                }
            }
        `;
        document.head.appendChild(styles);
    }
    
    // Adicionar notificação ao DOM
    document.body.appendChild(notification);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideInRight 0.3s ease-out reverse';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }
    }, 5000);
}

