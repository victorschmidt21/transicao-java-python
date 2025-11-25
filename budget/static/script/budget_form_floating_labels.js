document.addEventListener('DOMContentLoaded', function() {
  // Função para controlar floating labels
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
      if (input) {
        handleFloatingLabel(input);
      }
    });
  };

  // Aplicar a todos os inputs e selects
  const inputs = document.querySelectorAll('.floating-label input, .floating-label select');
  
  inputs.forEach(input => {
    // Verificar estado inicial
    handleFloatingLabel(input);
    
    // Eventos para controlar o floating
    input.addEventListener('focus', function() {
      const label = this.nextElementSibling;
      if (label && label.tagName === 'LABEL') {
        label.classList.add('floating');
      }
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
