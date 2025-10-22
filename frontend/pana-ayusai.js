(function () {
    // Идентификаторы секций, у которых в разметке есть id вида tab-rooms, tab-reviews и т.д.
    const tabs = ["rooms", "reviews", "services", "policies", "location"];

    // Находим все кнопки-табы
    document.querySelectorAll(".tab-btn").forEach((btn) => {
        // Вешаем обработчик клика на каждую
        btn.addEventListener("click", () => {
            // Какую вкладку открыть — берём из data-tab на нажатой кнопке (например, "reviews")
            const t = btn.dataset.tab;

            // Оформление заголовков (хедера табов) 
            // Сначала снимаем стили «активной» кнопки со всех таб-кнопок
            document.querySelectorAll(".tab-btn").forEach((b) => {
                b.classList.remove("border-b-2", "border-blue-600", "text-blue-600");
                b.classList.add("text-slate-600");
            });
            // А на текущую кнопку добавляем стили активной
            btn.classList.add("border-b-2", "border-blue-600", "text-blue-600");

            // Переключение контента
            // Прячем все секции табов (tab-rooms, tab-reviews, ...)
            tabs.forEach((id) =>
                document.getElementById(`tab-${id}`)?.classList.add("hidden")
            );
            // Показываем нужную секцию
            document.getElementById(`tab-${t}`)?.classList.remove("hidden");
        });
    });
})();

//Отзывы гостей
(function () {
    // Сам модал, кнопки открытия/закрытия
    const modal = document.getElementById("reviewsModal");
    const openBtn = document.getElementById("openReviewsModal");
    const closeBtn = document.getElementById("closeReviewsModal");
    // Ищем внутри модала элемент с атрибутом data-close (клик по нему закрывает модал)
    const overlay = modal?.querySelector("[data-close]");

    // Открыть модал убрать .hidden, добавить .flex, заблокировать скролл body
    function open() {
        modal.classList.remove("hidden");
        modal.classList.add("flex"); // выравнивание по центру через flex-контейнер
        document.body.style.overflow = "hidden"; // запрещаем скролл основного документа
    }

    // Закрыть модал вернуть .hidden, убрать .flex, вернуть скролл body
    function close() {
        modal.classList.add("hidden");
        modal.classList.remove("flex");
        document.body.style.overflow = "";
    }

    // Кнопка открытия (если есть на странице)
    openBtn?.addEventListener("click", (e) => {
        e.preventDefault(); // чтобы ссылка/кнопка не делала переход
        open();
    });

    // Кнопка крестик закрыть
    closeBtn?.addEventListener("click", close);

    // Закрытие по клавише Esc
    window.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && !modal.classList.contains("hidden")) close();
    });
})();