document.addEventListener("DOMContentLoaded", () => {
  let products = [];

  const productsTable = document.querySelector('.products');
  const productSelect = document.querySelector('.product-select');
  const productQuantity = document.querySelector('.quantity-input');
  const totalRow = document.querySelector('.value-total-row');
  const hiddenInput = document.querySelector('.products-hidden');

  function setTableProducts() {
    productsTable.innerHTML = "";

    products.forEach((product, index) => {
      const tr = document.createElement('tr');

      tr.innerHTML = `
        <td>${product.name}</td>
        <td>${product.quantity}</td>
        <td>R$ ${product.value.toFixed(2)}</td>
        <td>R$ ${product.total_value.toFixed(2)}</td>
        <td><button type="button" class="delete" data-index="${index}">Excluir</button></td>
      `;

      productsTable.appendChild(tr);
    });

    const total = products.reduce((acc, p) => acc + p.total_value, 0);
    totalRow.textContent = `R$ ${total.toFixed(2)}`;
    hiddenInput.value = JSON.stringify(products);
  }

  document.querySelector('.add-product-btn').addEventListener('click', e => {
    e.preventDefault();

    const selectedOption = productSelect.selectedOptions[0];
    const name = selectedOption.dataset.name;
    const value = parseFloat(selectedOption.dataset.price);
    const quantity = parseInt(productQuantity.value);

    if(!name){
      alert("Selecione um produto!");
      return;
    }

    if (!quantity || quantity <= 0) {
      alert("Informe uma quantidade válida!");
      return;
    }

    products.push({
      id: productSelect.value,
      name,
      value,
      quantity,
      total_value: value * quantity
    });

    setTableProducts();
  });

  productsTable.addEventListener('click', e => {
    if (e.target.classList.contains('delete')) {
      const index = e.target.dataset.index;
      products.splice(index, 1);
      setTableProducts();
    }
  });
  
  const form = document.querySelector('form');
  form.addEventListener('submit', () => {
    hiddenInput.value = JSON.stringify(products);
  });
});