window.addEventListener('DOMContentLoaded', event => {
    const modalLoignButton = document.querySelector('#loginModalButton');
    modalLoignButton.addEventListener('click', () => {
        const modalLoign = document.querySelector('#loginModal');
        modalLoign.classList.add('modal-open');
    });
});