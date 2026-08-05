(() => {
    'use strict';

    const toggle = document.querySelector('[data-action="toggle-nav"]');
    const nav = document.getElementById('tpl-main-nav');

    if (!toggle || !nav) {
        return;
    }

    toggle.addEventListener('click', () => {
        const isOpen = nav.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', String(isOpen));
    });
})();
