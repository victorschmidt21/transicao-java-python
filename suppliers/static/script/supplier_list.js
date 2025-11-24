document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('deleteModal');
  const cancelButton = document.getElementById('cancelDelete');
  const confirmButton = document.getElementById('confirmDelete');
  const supplierNameElement = modal.querySelector('.supplier-name');
  let supplierToDelete = null;

  // Abrir modal ao clicar no botão "Excluir"
  document.addEventListener('click', (e) => {
    const button = e.target.closest('.delete');
    if (!button) return;

    e.preventDefault();

    supplierToDelete = {
      id: button.getAttribute('data-supplier-id'),
      name: button.getAttribute('data-supplier-name')
    };

    console.log(supplierToDelete)

    // Atualiza o nome no modal
    supplierNameElement.textContent = `Fornecedor: ${supplierToDelete.name}`;

    // Exibe o modal
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  });

  // Cancelar exclusão
  cancelButton.addEventListener('click', () => {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    supplierToDelete = null;
  });

  // Confirmar exclusão
  confirmButton.addEventListener('click', async () => {
    if (!supplierToDelete) return;

    confirmButton.textContent = 'Excluindo...';
    confirmButton.disabled = true;

    try {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

      const response = await fetch(`/suppliers/delete/${supplierToDelete.id}/`, {
        method: 'POST', // Django normalmente trata POST com _method override
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ _method: 'DELETE' }), // opcional
      });

      if (response.ok) {
        // Remove linha da tabela (caso esteja numa lista)
        const row = document.querySelector(
          `button[data-supplier-id="${supplierToDelete.id}"]`
        )?.closest('tr');

        if (row) {
          row.style.transition = 'opacity 0.3s ease';
          row.style.opacity = '0';
          setTimeout(() => row.remove(), 300);
        }

        // Fecha modal
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';

        showNotification('Orçamento excluído com sucesso!', 'success');
      } else {
        showNotification('Erro ao excluir orçamento.', 'error');
      }
    } catch (error) {
      console.error(error);
      showNotification('Erro ao comunicar com o servidor.', 'error');
    } finally {
      confirmButton.textContent = 'Confirmar';
      confirmButton.disabled = false;
      supplierToDelete = null;
    }
  });

  // Fechar modal ao clicar fora dele
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      document.body.style.overflow = 'auto';
      supplierToDelete = null;
    }
  });
});
