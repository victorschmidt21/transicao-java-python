document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('deleteModal');
  const cancelButton = document.getElementById('cancelDelete');
  const confirmButton = document.getElementById('confirmDelete');
  const customerNameElement = modal.querySelector('.budget-name');
  let budgetToDelete = null;

  // Abrir modal ao clicar no botão "Excluir"
  document.addEventListener('click', (e) => {
    const button = e.target.closest('.delete');
    if (!button) return;

    e.preventDefault();

    budgetToDelete = {
      id: button.getAttribute('data-budget-id'),
      name: button.getAttribute('data-budget-name')
    };

    console.log(budgetToDelete)

    // Atualiza o nome no modal
    customerNameElement.textContent = `Orçamento: ${budgetToDelete.name}`;

    // Exibe o modal
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  });

  // Cancelar exclusão
  cancelButton.addEventListener('click', () => {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    budgetToDelete = null;
  });

  // Confirmar exclusão
  confirmButton.addEventListener('click', async () => {
    if (!budgetToDelete) return;

    confirmButton.textContent = 'Excluindo...';
    confirmButton.disabled = true;

    try {
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

      const response = await fetch(`/budget/delete/${budgetToDelete.id}/`, {
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
          `button[data-budget-id="${budgetToDelete.id}"]`
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
      budgetToDelete = null;
    }
  });

  // Fechar modal ao clicar fora dele
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
      document.body.style.overflow = 'auto';
      budgetToDelete = null;
    }
  });
});
