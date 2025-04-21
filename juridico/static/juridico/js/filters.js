const form = document.getElementById('filter-form');
const tabelaContainer = document.getElementById('processo-tabela');

form.addEventListener('change', function () {
    const formData = new FormData(form);
    const queryString = new URLSearchParams(formData).toString();

    const url = form.getAttribute('data-url');  // Captura a URL passada no template

    fetch(url + "?" + queryString, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.text())
    .then(html => {
        tabelaContainer.innerHTML = html;
    });
});
