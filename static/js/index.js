const registerForm = document.querySelector('#registerForm');
const loginForm = document.querySelector('#loginForm');

registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(registerForm);

    registerPost({
        name: formData.get('name'),
        email: formData.get('email'),
        password: formData.get('password'),
        password2: formData.get('password2'),
    });
});

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(loginForm);

    loginPost({
        email: formData.get('email'),
        password: formData.get('password'),
    });
});

async function loginPost(data = {}) {
    await fetch(`${baseUrl}/login`, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    })
        .then(data => data.json())
        .then(data => loginEvent(data, '#ModalFormLogin'))
        .catch(error => console.warn(error));
}

async function registerPost(data = {}) {
    await fetch(`${baseUrl}/register`, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    })
        .then(data => data.json())
        .then(data => loginEvent(data, '#ModalFormRegister'))
        .catch(error => console.warn(error));
}

function loginEvent(data, formSelector) {
    if (data.category == 'Success') {
        const profileNavLink = document.querySelector('#profileLinkNone'),
            profileButtonLink = document.querySelector('#loginModalButton');

        profileNavLink.textContent = data.name;
        profileNavLink.setAttribute('href', '/profile');
        profileNavLink.removeAttribute('data-bs-toggle');
        profileNavLink.removeAttribute('data-bs-target');
        profileNavLink.id = 'profileLink';

        profileButtonLink.textContent = `Перейти в профиль ${data.name}`;
        profileButtonLink.setAttribute('href', '/profile');
        profileButtonLink.removeAttribute('data-bs-toggle');
        profileButtonLink.removeAttribute('data-bs-target');

        $(formSelector).modal('toggle');

        tippy('#profileLink', {
            content: '<a type="button" class="btn btn-danger" id="logoutButton" href="/logout">Выйти из профиля</button>',
            allowHTML: true,
            interactive: true
        });
    }

    $.jGrowl(data.msg, {
        header: data.category,
        life: 10000,
        position: 'bottom-right'
    });
}