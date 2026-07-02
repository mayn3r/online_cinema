document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".movie-card");

    // 1. Анимация появления при скролле (Intersection Observer)
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target); // Перестаем следить, чтобы не повторять
            }
        });
    }, { threshold: 0.1 }); // Срабатывает, когда 10% элемента видно

    cards.forEach(card => {
        card.classList.add("fade-in"); // Добавляем начальный класс (прозрачность 0)
        observer.observe(card);
    });

    // 2. Обработка клика на карточку (Заглушка)
    cards.forEach(card => {
        card.addEventListener("click", () => {
            const title = card.getAttribute("data-title");
            alert(`Вы выбрали фильм: "${title}"\n\nСтраница просмотра находится в разработке.`);
        });
    });
});


// src/static/js/main.js (добавить в конец)

// Валидация формы регистрации
const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", function(event) {
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;
        const errorText = document.getElementById("passwordError");

        if (password !== confirmPassword) {
            event.preventDefault(); // Отменяем отправку формы
            errorText.style.display = "block"; // Показываем ошибку
            document.getElementById("confirm_password").style.borderColor = "#ff4d4d";
        } else {
            errorText.style.display = "none";
            document.getElementById("confirm_password").style.borderColor = "#444";
        }
    });
}


document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // Отменяем стандартную отправку
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include'  // Для cookies
    });
    
    if (response.ok) {
        const data = await response.json();
        console.log('Login success:', data);
        // Редирект или обновление страницы
        window.location.href = '/';
    } else {
        const error = await response.json();
        alert('Ошибка: Неверный пароль или email');
    }
});


document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // Отменяем стандартную отправку
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;
    
    // Простая проверка на клиенте
    if (password !== confirm_password) {
        alert('Пароли не совпадают!');
        return;
    }
    
    if (password.length < 6) {
        alert('Пароль должен содержать минимум 6 символов');
        return;
    }
    
    const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include'  // Для cookies
    });
    
    if (response.ok) {
        const data = await response.json();
        console.log('Register success:', data);
        alert('Регистрация успешна!');
        // Редирект на страницу входа
        window.location.href = '/login';
    } else {
        const error = await response.json();
        alert('Ошибка: ' + (error.detail || 'Неверные данные'));
    }
});


async function logoutBtn(e) {
    console.log('Logout button clicked');
    e.preventDefault(); // Отменяем стандартное действие
    const response = await fetch('/api/auth/logout', {
        method: 'POST',
        credentials: 'include'  // Для cookies
    });
    if (response.ok) {
        window.location.href = '/login';
    }
};