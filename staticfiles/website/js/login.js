const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');
registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});
loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

const messageCloseButtons =
    document.querySelectorAll(".message-close");


messageCloseButtons.forEach((button) => {

    button.addEventListener("click", () => {

        const message =
            button.closest(".auth-message");

        message.remove();

    });

});