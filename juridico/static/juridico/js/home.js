var detailsModal = document.getElementById('detailsModal');

detailsModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget;

    var unidade = button.getAttribute('data-unidade');
    var tipoProcesso = button.getAttribute('data-tipo_processo');
    var acao = button.getAttribute('data-acao');
    var contratoEnvolvido = button.getAttribute('data-contrato_envolvido');
    var cidade = button.getAttribute('data-cidade');
    var valorCausa = button.getAttribute('data-valor_causa');
    var vara = button.getAttribute('data-vara');
    var fase = button.getAttribute('data-fase');
    var instancia = button.getAttribute('data-instancia');
    var dataPropositura = button.getAttribute('data-data_propositura');
    var advogado = button.getAttribute('data-advogado');
    var status = button.getAttribute('data-status');
    var nomeAutor = button.getAttribute('data-nome_autor');
    var cpfAutor = button.getAttribute('data-cpf_autor');
    var dataUltimaModificacao = button.getAttribute('data-data_ultima_modificacao');
    var juiz = button.getAttribute('data-juiz');
    var numeroProcesso = button.getAttribute('data-numero_processo');
    var descricao = button.getAttribute('data-descricao');

    detailsModal.querySelector('#modal-unidade').textContent = unidade;
    detailsModal.querySelector('#modal-tipo_processo').textContent = tipoProcesso;
    detailsModal.querySelector('#modal-acao').textContent = acao;
    detailsModal.querySelector('#modal-contrato_envolvido').textContent = contratoEnvolvido;
    detailsModal.querySelector('#modal-cidade').textContent = cidade;
    detailsModal.querySelector('#modal-valor_causa').textContent = valorCausa;
    detailsModal.querySelector('#modal-vara').textContent = vara;
    detailsModal.querySelector('#modal-fase').textContent = fase;
    detailsModal.querySelector('#modal-instancia').textContent = instancia;
    detailsModal.querySelector('#modal-data_propositura').textContent = dataPropositura;
    detailsModal.querySelector('#modal-advogado').textContent = advogado;
    detailsModal.querySelector('#modal-status').textContent = status;
    detailsModal.querySelector('#modal-nome_autor').textContent = nomeAutor;
    detailsModal.querySelector('#modal-cpf_autor').textContent = cpfAutor;
    detailsModal.querySelector('#modal-data_ultima_modificacao').textContent = dataUltimaModificacao;
    detailsModal.querySelector('#modal-juiz').textContent = juiz;
    detailsModal.querySelector('#modal-numero_processo').textContent = numeroProcesso;
    detailsModal.querySelector('#modal-descricao').textContent = descricao;
});



document.addEventListener("DOMContentLoaded", function() {
    const editModal = new bootstrap.Modal(document.getElementById("editModal"));
    const editForm = document.getElementById("editForm");

    // Abrir modal de edição
    document.querySelectorAll(".edit-details").forEach(button => {
        button.addEventListener("click", function() {
            document.getElementById("edit-id").value = this.getAttribute("data-id");
            document.getElementById("edit-unidade").value = this.getAttribute("data-unidade");
            document.getElementById("edit-tipo_processo").value = this.getAttribute("data-tipo_processo");
            document.getElementById("edit-acao").value = this.getAttribute("data-acao");
            document.getElementById("edit-contrato_envolvido").value = this.getAttribute("data-contrato_envolvido");
            document.getElementById("edit-cidade").value = this.getAttribute("data-cidade");
            document.getElementById("edit-valor_causa").value = this.getAttribute("data-valor_causa");
            document.getElementById("edit-vara").value = this.getAttribute("data-vara");
            document.getElementById("edit-fase").value = this.getAttribute("data-fase");
            document.getElementById("edit-instancia").value = this.getAttribute("data-instancia");
            document.getElementById("edit-data_propositura").value = this.getAttribute("data-data_propositura");
            document.getElementById("edit-status").value = this.getAttribute("data-status");
            document.getElementById("edit-nome_autor").value = this.getAttribute("data-nome_autor");
            document.getElementById("edit-cpf_autor").value = this.getAttribute("data-cpf_autor");
            document.getElementById("edit-data_ultima_modificacao").value = this.getAttribute("data-data_ultima_modificacao");
            document.getElementById("edit-juiz").value = this.getAttribute("data-juiz");
            document.getElementById("edit-numero_processo").value = this.getAttribute("data-numero_processo");
            document.getElementById("edit-descricao").value = this.getAttribute("data-descricao");

            let advogado1ID = this.getAttribute("data-advogado");
            let select = document.getElementById("edit-advogado");

            for (let option of select.options) {
                if (option.value == advogado1ID) {
                    option.selected = true;
                    break;
                }
            }

            editModal.show();
        });
    });

    // Enviar formulário de edição
    editForm.addEventListener("submit", function(event) {
        event.preventDefault();

        // Converter campos de texto para letras maiúsculas
        let camposParaMaiusculas = [
            "edit-unidade", "edit-tipo_processo", "edit-acao", "edit-contrato_envolvido", 
            "edit-cidade", "edit-vara", "edit-fase", "edit-instancia", "edit-status", 
            "edit-nome_autor", "edit-juiz", "edit-numero_processo", "edit-descricao"
        ];

        camposParaMaiusculas.forEach(campo => {
            let input = document.getElementById(campo);
            if (input && input.value) {
                input.value = input.value.toUpperCase();
            }
        });

        let formData = new FormData(editForm);
        let url = editForm.getAttribute("data-url");

        fetch(url, {  
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                console.error("Erro no backend:", data.error);
                alert("Erro ao atualizar o processo: " + data.error);
            }
        })
        .catch(error => console.error("Erro ao enviar requisição:", error));
    });
});
