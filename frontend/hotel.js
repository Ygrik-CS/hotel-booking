// Утилиты
const $ = (s, p = document) => p.querySelector(s);
const $$ = (s, p = document) => [...p.querySelectorAll(s)];
const cards = () => $$("#list article");

// Счётчик ночей
const inEl = $("#qIn"), outEl = $("#qOut"), nightsEl = $("#qNights");

// дефолтные даты
function setDefaultDates() {
  const today = new Date();
  const inDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1);
  const outDate = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 10);
  inEl.valueAsDate = inDate;
  outEl.valueAsDate = outDate;
  updNights();
}

function daysBetween(a, b) { return Math.round((b - a) / (1000 * 60 * 60 * 24)); }

function updNights() {
  const a = new Date(inEl.value), b = new Date(outEl.value);
  if (!isNaN(a) && !isNaN(b) && b > a) {
    const n = Math.max(1, daysBetween(a, b));
    if (nightsEl) nightsEl.textContent = `${n} night${n > 1 ? "s" : ""}`;
    $$(".nights").forEach((el) => (el.textContent = n));
  } else {
    if (nightsEl) nightsEl.textContent = "";
  }
}

inEl.addEventListener("change", () => {
  if (outEl.value && new Date(outEl.value) <= new Date(inEl.value)) {
    const d = new Date(inEl.value);
    d.setDate(d.getDate() + 1);
    outEl.valueAsDate = d;
  }
  updNights();
});
outEl.addEventListener("change", updNights);
setDefaultDates();

// Фильтры
const priceRange = $("#fPrice"),
      priceLabel = $("#priceLabel"),
      cityTag = $("#cityTag");

function updateFound() {
  const visible = cards().filter((c) => !c.classList.contains("hidden")).length;
  $("#found").textContent = visible;
}

function applyFilters() {
  const name = $("#fName").value.trim().toLowerCase();
  const city = $("#fCity").value;
  const priceMax = +priceRange.value;

  const flags = {
    breakfast: $("#aBreakfast").checked,
    pool: $("#aPool").checked,
    museum: $("#aMuseum").checked,
    great: $("#aGreat").checked,
    hotel: $("#aHotel").checked,
  };

  cityTag.textContent = city || $("#qCity").value || "Any";
  let qCity = $("#qCity").value.trim().toLowerCase();

  cards().forEach((c) => {
    // проверки по датасетам карточки
    const okName = !name || c.dataset.name.toLowerCase().includes(name);
    const okCity = !city || c.dataset.city === city;
    const okQCity = !qCity || c.dataset.city.toLowerCase().includes(qCity);
    const okPrice = +c.dataset.price <= priceMax;
    const okBreakfast = !flags.breakfast || c.dataset.breakfast === "true";
    const okPool = !flags.pool || c.dataset.pool === "true";
    const okMuseum = !flags.museum || c.dataset.museum === "true";
    const okGreat = !flags.great || c.dataset.great === "true";
    const okHotel = !flags.hotel || c.dataset.hotel === "true";

    const ok = okName && okCity && okQCity && okPrice && okBreakfast && okPool && okMuseum && okGreat && okHotel;
    c.classList.toggle("hidden", !ok);
  });

  updateFound();
  sortCards();
}

// подпись к слайдеру цены
priceRange.addEventListener("input", (e) => {
  priceLabel.textContent = "$" + e.target.value;
  applyFilters(); // live по цене
});

// кнопки
$("#applyBtn").addEventListener("click", applyFilters);
$("#resetBtn").addEventListener("click", () => {
  $("#fName").value = "";
  $("#fCity").value = "Almaty";
  $("#aBreakfast").checked = false;
  $("#aPool").checked = false;
  $("#aMuseum").checked = false;
  $("#aGreat").checked = false;
  $("#aHotel").checked = false;
  priceRange.value = 280;
  priceLabel.textContent = "$280";
  // показать все
  cards().forEach((c) => c.classList.remove("hidden"));
  updateFound();
  sortCards();
});

// быстрый поиск
$("#qSearch").addEventListener("click", applyFilters);
$("#qCity").addEventListener("input", applyFilters);

// применяем при клике на чекбоксы
$("#aBreakfast").addEventListener("change", applyFilters);
$("#aPool").addEventListener("change", applyFilters);
$("#aMuseum").addEventListener("change", applyFilters);
$("#aGreat").addEventListener("change", applyFilters);
$("#aHotel").addEventListener("change", applyFilters);

// сортировка
function sortCards() {
  const mode = $("#sort").value;
  const list = $("#list");
  const items = cards().filter((c) => !c.classList.contains("hidden"));

  items.sort((a, b) => {
    const pa = +a.dataset.price, pb = +b.dataset.price;
    const ra = +a.dataset.rating, rb = +b.dataset.rating;
    if (mode === "priceAsc") return pa - pb;
    if (mode === "priceDesc") return pb - pa;
    if (mode === "ratingDesc") return rb - ra;
    return 0;
  });

  items.forEach((el) => list.appendChild(el));
}
$("#sort").addEventListener("change", sortCards);

// первичная инициализация
applyFilters();
// ===== Перенос данных на booking.html =====

