const baseUrl = `http://${document.location.host}`;

window.addEventListener('DOMContentLoaded', () => {
    tippy('#profileLink', {
        content: '<a type="button" class="btn btn-danger" id="logoutButton" href="/logout">Выйти из профиля</button>',
        allowHTML: true,
        interactive: true
    });

    // document.querySelector('#tippy-1').addEventListener('click', (e) => {
    //     e.preventDefault();
    //     console.log(document.querySelector('#logoutButton'));
    // });

    let navbarShrink = () => {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }
    };

    navbarShrink();
    document.addEventListener('scroll', navbarShrink);

    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );

    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });
});
