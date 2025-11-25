// Scripts para a lista de funcionários

document.addEventListener('DOMContentLoaded', function () {
    // Funcionalidade do modal de confirmação de exclusão
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const modal = document.getElementById('deleteModal');
    const cancelButton = document.getElementById('cancelDelete');
    const confirmButton = document.getElementById('confirmDelete');
    const employeeNameElement = document.querySelector('.employee-name');

    let employeeToDelete = null;

    // Interceptar cliques nos botões de excluir
    deleteButtons.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            employeeToDelete = {
                id: this.getAttribute('data-employee-id'),
                name: this.getAttribute('data-employee-name')
            };

            // Atualizar o nome do funcionário no modal
            employeeNameElement.textContent = `Funcionário: ${employeeToDelete.name}`;

            // Mostrar o modal
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    });

    // Fechar modal ao clicar em cancelar
    if (cancelButton) {
        cancelButton.addEventListener('click', function () {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            employeeToDelete = null;
        });
    }

    // Confirmar exclusão
    if (confirmButton) {
        confirmButton.addEventListener('click', function () {
            if (employeeToDelete) {
                // Criar formulário para enviar DELETE request
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = `/employee/delete/${employeeToDelete.id}/`;

                // Adicionar CSRF token
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;
                form.appendChild(csrfInput);

                // Adicionar ao body e submeter
                document.body.appendChild(form);
                form.submit();
            }
        });
    }

    // Fechar modal ao clicar fora dele
    if (modal) {
        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
                employeeToDelete = null;
            }
        });
    }

    // Fechar modal com tecla ESC
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal && modal.style.display === 'flex') {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            employeeToDelete = null;
        }
    });
});
