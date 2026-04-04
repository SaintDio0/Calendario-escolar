(() => {
    const config = window.calendarConfig;
    if (!config) return;

    const tipoEl = document.querySelector(config.filters.tipo);
    const turmaEl = document.querySelector(config.filters.turma);
    const mesEl = document.querySelector(config.filters.mes);
    const triggerEl = document.querySelector(config.filters.trigger);

    const calendarEl = document.querySelector(config.target);
    if (!calendarEl) return;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        locale: "pt-br",
        initialView: "dayGridMonth",
        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,timeGridWeek,listWeek",
        },
        events(fetchInfo, successCallback, failureCallback) {
            const params = new URLSearchParams({
                start: fetchInfo.startStr,
                end: fetchInfo.endStr,
            });

            if (tipoEl?.value) params.append("tipo_evento", tipoEl.value);
            if (turmaEl?.value) params.append("turma", turmaEl.value);
            if (mesEl?.value) params.append("mes", mesEl.value);

            fetch(`${config.eventsUrl}?${params.toString()}`)
                .then((res) => res.json())
                .then((data) => successCallback(data))
                .catch((error) => failureCallback(error));
        },
        eventClick(info) {
            if (info.event.url) {
                info.jsEvent.preventDefault();
                window.location.href = info.event.url;
            }
        },
    });

    triggerEl?.addEventListener("click", (e) => {
        e.preventDefault();
        calendar.refetchEvents();
    });

    calendar.render();
})();

