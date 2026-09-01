// Instant Client-Side Fuzzy Search Filter
function filterList(inputId, listClass, itemSelector) {
    const query = document.getElementById(inputId).value.toLowerCase();
    document.querySelectorAll(`.${listClass} ${itemSelector}`).forEach(el => {
        const text = el.textContent.toLowerCase();
        el.style.display = text.includes(query) ? '' : 'none';
    });
}
