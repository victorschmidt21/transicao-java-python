document.addEventListener("DOMContentLoaded", () => {
  const cnpjInput = document.querySelector("#id_cnpj");

  cnpjInput.addEventListener("input", () => {
    let v = cnpjInput.value.replace(/\D/g, "");
    if (v.length > 14) v = v.slice(0, 14);

    cnpjInput.value = v
      .replace(/^(\d{2})(\d)/, "$1.$2")
      .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
      .replace(/\.(\d{3})(\d)/, ".$1/$2")
      .replace(/(\d{4})(\d)/, "$1-$2");
  });
});
