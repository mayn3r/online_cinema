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