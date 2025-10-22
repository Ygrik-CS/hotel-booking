// Утилиты для выбора элементов: $ — один элемент, $$ — список элементов
const $ = (s, p = document) => p.querySelector(s);
const $$ = (s, p = document) => [...p.querySelectorAll(s)];
// Функция, возвращающая все карточки отелей (article внутри #list)
const cards = () => $$("#list article");

// Счётчик ночей (устойчивый/robust)
const inEl = $("#qIn"), // инпут даты заезда
  outEl = $("#qOut"), // инпут даты выезда
  nightsEl = $("#qNights"); // элемент, где показываем N nights

// Устанавливаем даты по умолчанию: завтра — заезд, через 10 дней — выезд
function setDefaultDates() {
  const today = new Date();
  const inDate = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate() + 1 // +1 день от сегодня
  );
  const outDate = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate() + 10 // +10 дней от сегодня
  );
  // valueAsDate удобно задаёт дату для input[type=date]
  inEl.valueAsDate = inDate;
  outEl.valueAsDate = outDate;
  updNights(); // сразу посчитать ночи
}

// Вспомогательная разница в днях между двумя Date
function daysBetween(a, b) {
  return Math.round((b - a) / (1000 * 60 * 60 * 24));
}

// Обновляем отображение количества ночей
function updNights() {
  const a = new Date(inEl.value),
    b = new Date(outEl.value);
  // Проверяем, что обе даты валидны и выезд позже заезда
  if (!isNaN(a) && !isNaN(b) && b > a) {
    // Минимум 1 ночь (на случай округлений/ошибок)
    const n = Math.max(1, daysBetween(a, b));
    // Пишем "1 night" или "2 nights"
    nightsEl.textContent = `${n} night${n > 1 ? "s" : ""}`;
    // Синхронно обновляем число ночей у всех элементов с классом .nights (на карточках)
    $$(".nights").forEach((el) => (el.textContent = n));
  } else {
    // Если дата некорректна очищаем поле
    nightsEl.textContent = "";
  }
}

// Когда пользователь меняет дату заезда:
inEl.addEventListener("change", () => {
  // Если дата выезда не задана или <= заезда — сдвигаем выезд на +1 день от заезда
  if (outEl.value && new Date(outEl.value) <= new Date(inEl.value)) {
    const d = new Date(inEl.value);
    d.setDate(d.getDate() + 1);
    outEl.valueAsDate = d;
  }
  updNights(); // пересчитать ночи
});

// Обновляем ночи при изменении даты выезда
outEl.addEventListener("change", updNights);

// Инициализация дефолтных дат при загрузке
setDefaultDates();

// Фильтры
const priceRange = $("#fPrice"), // range для максимальной цены
  priceLabel = $("#priceLabel"); // подпись к слайдеру (например, "$180")
const cityTag = $("#cityTag"); // бейдж с выбранным городом

// Подсчитать и показать, сколько карточек сейчас видно (не .hidden)
function updateFound() {
  const visible = cards().filter((c) => !c.classList.contains("hidden")).length;
  $("#found").textContent = visible;
}

// Применение фильтров ко всем карточкам
function applyFilters() {
  const name = $("#fName").value.trim().toLowerCase(); // фильтр по названию
  const city = $("#fCity").value; // точный город из селекта
  const priceMax = +priceRange.value; // максимальная цена из слайдера
  // Булевы фильтры-признаки
  const flags = {
    breakfast: $("#aBreakfast").checked,
    pool: $("#aPool").checked,
    museum: $("#aMuseum").checked,
    great: $("#aGreat").checked,
    hotel: $("#aHotel").checked,
  };

  // Отобразить выбранный город в бейдже и учесть город из строки поиска
  cityTag.textContent = city || $("#qCity").value || "Any";
  let qCity = $("#qCity").value.trim().toLowerCase(); // "мягкий" поиск по городу

  // Пробегаемся по всем карточкам и решаем, скрывать или показывать
  cards().forEach((c) => {
    0 // Проверки по датасетам карточки
    const okName = !name || c.dataset.name.toLowerCase().includes(name);
    const okCity = !city || c.dataset.city === city; // точное совпадение селекта
    const okQCity = !qCity || c.dataset.city.toLowerCase().includes(qCity); // "мягкий" поиск
    const okPrice = +c.dataset.price <= priceMax;
    const okBreakfast = !flags.breakfast || c.dataset.breakfast === "true";
    const okPool = !flags.pool || c.dataset.pool === "true";
    const okMuseum = !flags.museum || c.dataset.museum === "true";
    const okGreat = !flags.great || c.dataset.great === "true";
    const okHotel = !flags.hotel || c.dataset.hotel === "true";

    // Карточка проходит, только если прошла все активные фильтры
    const ok =
      okName &&
      okCity &&
      okQCity &&
      okPrice &&
      okBreakfast &&
      okPool &&
      okMuseum &&
      okGreat &&
      okHotel;

    // Переключаем класс hidden (true => скрыть)
    c.classList.toggle("hidden", !ok);
  });

  updateFound(); // обновить счётчик найденных
  sortCards(); // сохранить порядок после фильтрации (пересортировать видимые)
}

// Живое обновление подписи слайдера цены при движении ползунка
priceRange.addEventListener(
  "input",
  (e) => (priceLabel.textContent = "$" + e.target.value)
);

// Кнопки Применить и Сбросить фильтры
$("#applyBtn").addEventListener("click", applyFilters);
$("#resetBtn").addEventListener("click", () => {
  // Сбрасываем значения всех контролов к дефолтным
  $("#fName").value = "";
  $("#fCity").value = "Almaty";
  $("#aBreakfast").checked = false;
  $("#aPool").checked = false;
  $("#aMuseum").checked = false;
  $("#aGreat").checked = false;
  $("#aHotel").checked = false;
  priceRange.value = 280;
  priceLabel.textContent = "$280";
  applyFilters(); // и сразу применяем
});

// Быстрый поиск из верхней панели: кнопка и инпут города
$("#qSearch").addEventListener("click", applyFilters);
$("#qCity").addEventListener("input", applyFilters);

// Сортировка карточек
function sortCards() {
  const mode = $("#sort").value; // режим сортировки из селекта
  const list = $("#list"); // контейнер со списком карточек
  // Берём только видимые карточки (иначе спрятанные «перемешаются» зря)
  const items = cards().filter((c) => !c.classList.contains("hidden"));

  // Сортировка по выбранному критерию
  items.sort((a, b) => {
    const pa = +a.dataset.price,
      pb = +b.dataset.price; // цены
    const ra = +a.dataset.rating,
      rb = +b.dataset.rating; // рейтинги
    if (mode === "priceAsc") return pa - pb; // по цене возр
    if (mode === "priceDesc") return pb - pa; // по цене убыв
    if (mode === "ratingDesc") return rb - ra; // по рейтингу убыв
    return 0; // без изменений
  });

  // Переупорядочиваем элементы в DOM в новом порядке
  items.forEach((el) => list.appendChild(el));
}

// Обновлять порядок при смене селекта сортировки
$("#sort").addEventListener("change", sortCards);

// Первичная инициализация: применить фильтры сразу
applyFilters();