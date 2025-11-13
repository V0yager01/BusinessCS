function initLogin() {
    const form = document.getElementById("loginForm");
    const msg = document.getElementById("loginMessage");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        msg.textContent = "";
        msg.style.color = "";

        try {
        const data = {
            email: form.email.value,
            password: form.password.value,
        };

            await UserAPI.login(data);
            msg.style.color = "green";
            msg.textContent = "Успешный вход! Перенаправление...";
            setTimeout(() => window.location.href = "/", 1000);
        } catch (error) {
            msg.style.color = "red";
            msg.textContent = error.message || "Неверные учетные данные.";
        }
    });
}

function initRegister() {
    const form = document.getElementById("registerForm");
    const msg = document.getElementById("registerMessage");

    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        msg.textContent = "";
        msg.style.color = "";

        try {
        const data = {
            username: form.username.value,
            email: form.email.value,
            password: form.password.value,
        };

            await UserAPI.register(data);
            msg.style.color = "green";
            msg.textContent = "Регистрация успешна! Теперь войдите.";
            setTimeout(() => window.location.href = "/login", 1000);
        } catch (error) {
            msg.style.color = "red";
            msg.textContent = error.message || "Ошибка регистрации.";
        }
    });
}
