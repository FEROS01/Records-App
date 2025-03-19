const set_timezone = () => {
    timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    timezone_input = document.querySelector("[name='timezone']");
    timezone_input.value = timeZone;
    htmx.trigger("#timezone", 'change');
};

document.addEventListener("DOMContentLoaded", set_timezone);