document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'pt-br',
        events: '/api/reunioes/', // Rota que retorna os eventos
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        eventClick: function(info) {
            // Preenche o modal com os detalhes do evento
            document.getElementById('modalTitle').innerText = info.event.title;
            document.getElementById('modalDate').innerText = info.event.start.toLocaleDateString();
            document.getElementById('modalTime').innerText = info.event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            document.getElementById('modalDescription').innerText = info.event.extendedProps.description;
            document.getElementById('modalAutor').innerText = info.event.extendedProps.autor;
            document.getElementById('modalProcesso').innerText = info.event.extendedProps.processo;
            
            // Abre o modal
            var myModal = new bootstrap.Modal(document.getElementById('eventModal'));
            myModal.show();
        }
    });
    calendar.render();
});

document.addEventListener("DOMContentLoaded", function() {
    let autorSelect = document.getElementById("id_autor");
    let processoSelect = document.getElementById("id_processo");

    autorSelect.addEventListener("change", function() {
        let autorNome = this.value;
        processoSelect.innerHTML = '<option value="">Selecione um processo</option>';

        if (autorNome) {
            fetch(`/get-processos/?autor=${encodeURIComponent(autorNome)}`)
                .then(response => response.json())
                .then(data => {
                    data.forEach(processo => {
                        let option = document.createElement("option");
                        option.value = processo.id;
                        option.textContent = `${processo.numero_processo} - ${processo.tipo_processo}`;
                        processoSelect.appendChild(option);
                    });
                })
                .catch(error => console.error("Erro ao buscar processos:", error));
        }
    });
});