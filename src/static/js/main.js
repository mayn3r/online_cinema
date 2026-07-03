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
    // cards.forEach(card => {
    //     card.addEventListener("click", () => {
    //         const title = card.getAttribute("data-title");
    //         alert(`Вы выбрали фильм: "${title}"\n\nСтраница просмотра находится в разработке.`);
    //     });
    });



async function LoginFormHandler(e) {
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
};


// document.getElementById('registerForm').addEventListener('submit', async function(e) {
async function registerFormHandler(e) { 
    e.preventDefault(); // Отменяем стандартную отправку
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;
    const name = document.getElementById('name').value;
    const username = null; // Имя пользователя не передается на клиенте

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
        body: JSON.stringify({ email, password, name }),
        credentials: 'include'  // Для cookies
    });
    
    if (response.ok) {
        const data = await response.json();
        console.log('Register success:', data);
        // Редирект на страницу входа
        window.location.href = '/';
    } else {
        const error = await response.json();
        alert('Ошибка: ' + (error.detail || 'Неверные данные'));
    }
};


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


async function AddToWatchListHandler(e) {
    e.preventDefault(); // Отменяем стандартную отправку
    
    movie_id = document.getElementById("movie-id").getAttribute("data")
    console.log(movie_id)
    
    const response = await fetch('/api/watchlist/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ movie_id }),
        credentials: 'include'  // Для cookies
    });
    
    if (response.ok) {
        const data = await response.json();
        console.log('Login success:', data);
        // Редирект или обновление страницы
        window.location.href = '/movie/' + movie_id;
    } else {
        const error = await response.json();
        console.log("Error: ", error);
    }
};


async function RemoveToWatchListHandler(e) {
    e.preventDefault(); // Отменяем стандартную отправку
    
    movie_id = document.getElementById("movie-id").getAttribute("data")
    
    const response = await fetch('/api/watchlist/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ movie_id }),
        credentials: 'include'  // Для cookies
    });
    
    if (response.ok) {
        const data = await response.json();
        console.log('Login success:', data);
        // Редирект или обновление страницы
        window.location.href = '/movie/' + movie_id;
    } else {
        const error = await response.json();
        console.log("Error: ", error);
    }
};


// src/static/js/main.js (добавить в конец)

// Фильтрация фильмов на странице каталога
const filterChips = document.querySelectorAll('.filter-chip');
const movieCards = document.querySelectorAll('.movie-card');

if (filterChips.length > 0) {
    filterChips.forEach(chip => {
        chip.addEventListener('click', () => {
            // 1. Убираем класс active у всех кнопок
            filterChips.forEach(c => c.classList.remove('active'));
            // 2. Добавляем active нажатой кнопке
            chip.classList.add('active');

            const selectedGenre = chip.getAttribute('data-genre');

            // 3. Фильтруем карточки
            movieCards.forEach(card => {
                const cardGenre = card.getAttribute('data-genre');
                
                if (selectedGenre === 'all' || cardGenre === selectedGenre) {
                    card.style.display = 'flex'; // Показываем
                } else {
                    card.style.display = 'none'; // Скрываем
                }
            });
        });
    });
}