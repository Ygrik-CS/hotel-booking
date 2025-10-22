// Формат "US$73.00"
const fmtUSD = (n) => "US$" + Number(n).toFixed(2);

// Ставка НДС (12%)
const VAT_RATE = 0.12;

// Чтение объекта booking из localStorage (или null)
function loadBooking() {
  const raw = localStorage.getItem("booking");
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

// Отрисовать сводку брони (вызовать на странице oplata.html)
function render() {
  const b = loadBooking() || {};

  // Значения по умолчанию
  const hotel = b.hotel || "Pana Ayusai";
  const checkIn = b.checkIn || "2025-10-21";
  const checkOut = b.checkOut || "2025-10-22";
  const nights = Number(b.nights || 1);
  const price = Number(b.pricePerNight || 73);
  const adults = b.adults || 2;

  // Заголовок и даты
  const sumHotelEl = document.getElementById("sumHotel");
  if (sumHotelEl) sumHotelEl.textContent = hotel;

  const inDate = new Date(checkIn),
    outDate = new Date(checkOut);
  const opts = { month: "short", day: "numeric" };
  const datesStr = `${inDate.toLocaleDateString(
    "en-US",
    opts
  )}, ${inDate.getFullYear()} — ${outDate.toLocaleDateString(
    "en-US",
    opts
  )}, ${outDate.getFullYear()}`;
  const sumDatesEl = document.getElementById("sumDates");
  if (sumDatesEl) sumDatesEl.textContent = datesStr;

  // Кол-во ночей и гостей
  const sumNightsEl = document.getElementById("sumNights");
  if (sumNightsEl)
    sumNightsEl.textContent = `${nights} night${nights > 1 ? "s" : ""}`;
  const sumNightCountEl = document.getElementById("sumNightCount");
  if (sumNightCountEl) sumNightCountEl.textContent = nights;
  const sumGuestsEl = document.getElementById("sumGuests");
  if (sumGuestsEl)
    sumGuestsEl.textContent = `${adults} adult${adults > 1 ? "s" : ""}`;

  // Подсчёт итогов
  const subtotal = price * nights;
  const vat = subtotal * VAT_RATE;
  const total = subtotal + vat;

  const sumSubtotalEl = document.getElementById("sumSubtotal");
  if (sumSubtotalEl) sumSubtotalEl.textContent = fmtUSD(subtotal);
  const sumVatEl = document.getElementById("sumVat");
  if (sumVatEl) sumVatEl.textContent = fmtUSD(vat);
  const sumTotalEl = document.getElementById("sumTotal");
  if (sumTotalEl) sumTotalEl.textContent = fmtUSD(total);

  // Trip Coins: 50% от суммы в "коинах" (1 coin = $0.01)
  const coins = Math.round(total * 0.5);
  const coinsEl = document.getElementById("coins");
  if (coinsEl) coinsEl.textContent = `${coins} Trip Coins`;
  const coinsUsdEl = document.getElementById("coinsUsd");
  if (coinsUsdEl) coinsUsdEl.textContent = fmtUSD(coins / 100);
}

// Промокод (демо-подсказка)
document.getElementById("applyPromo")?.addEventListener("click", () => {
  const v = document.getElementById("promo")?.value.trim();
  const note = document.getElementById("promoNote");
  if (!note) return;
  if (!v) {
    note.classList.add("hidden");
    return;
  }
  note.classList.remove("hidden");
});

// Отправка формы брони на oplata.html (демо)
document.getElementById("bookingForm")?.addEventListener("submit", (e) => {
  e.preventDefault(); // не уходим со страницы
  alert("Booking submitted ✅");
});

// Если эта страница — oplata.html, вызовем render().
// (Без ошибок на других страницах — элементы проверяются через ?. и if)
render();

(function () {
  // Имена вкладок (HTML id должен быть в формате "tab-<name>")
  const tabs = ["rooms", "reviews", "services", "policies", "location"];

  // Вешаем обработчики на кнопки табов
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const t = btn.dataset.tab; // например "reviews"

      // Сброс активных стилей у всех кнопок
      document.querySelectorAll(".tab-btn").forEach((b) => {
        b.classList.remove("border-b-2", "border-blue-600", "text-blue-600");
        b.classList.add("text-slate-600");
      });

      // Активный стиль текущей кнопке
      btn.classList.add("border-b-2", "border-blue-600", "text-blue-600");

      // Скрыть все вкладки
      tabs.forEach((id) =>
        document.getElementById(`tab-${id}`)?.classList.add("hidden")
      );

      // Показать выбранную вкладку
      document.getElementById(`tab-${t}`)?.classList.remove("hidden");
    });
  });
})();

(function () {
  // Элементы модального окна
  const modal = document.getElementById("reviewsModal");
  const openBtn = document.getElementById("openReviewsModal");
  const closeBtn = document.getElementById("closeReviewsModal");
  const overlay = modal?.querySelector("[data-close]"); // затемнение

  // Открыть модалку
  function open() {
    if (!modal) return;
    modal.classList.remove("hidden");
    modal.classList.add("flex");
    document.body.style.overflow = "hidden"; // блокируем прокрутку
  }

  // Закрыть модалку
  function close() {
    if (!modal) return;
    modal.classList.add("hidden");
    modal.classList.remove("flex");
    document.body.style.overflow = ""; // возвращаем прокрутку
  }

  // Клики по кнопкам
  openBtn?.addEventListener("click", (e) => {
    e.preventDefault();
    open();
  });
  closeBtn?.addEventListener("click", close);
  overlay?.addEventListener("click", close);

  // Закрытие по ESC
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && modal && !modal.classList.contains("hidden"))
      close();
  });
})();

(function () {
  // мини-хелперы для выборок
  const $ = (s, p = document) => p.querySelector(s);
  const $$ = (s, p = document) => [...p.querySelectorAll(s)];

  // Извлекаем число из строки: "US$73 per night" → 73
  const numFromText = (t) => {
    const n = parseFloat(String(t || "").replace(/[^\d.]/g, ""));
    return isFinite(n) ? n : 0;
  };

  // Дата → YYYY-MM-DD
  const isoDate = (d) => {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    return `${y}-${m}-${day}`;
  };

  // На этой странице нет выбора дат — ставим сегодня/завтра
  function getDefaultDates() {
    const today = new Date();
    const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);
    return { inVal: isoDate(today), outVal: isoDate(tomorrow), nights: 1 };
  }

  // Название отеля (берём из id="hotelTitle" или H1/H2)
  function getHotelName() {
    return (
      $("#hotelTitle")?.textContent?.trim() ||
      $("h1")?.textContent?.trim() ||
      $("h2")?.textContent?.trim() ||
      "Hotel"
    )
      .replace(/\s+★+$/, "")
      .trim(); // убираем " ★★★★"
  }

  // Сохранить и перейти на оплату
  function saveAndGo({ hotel, roomName, pricePerNight, dates, adults }) {
    const payload = {
      hotel,
      room: roomName,
      pricePerNight,
      checkIn: dates.inVal,
      checkOut: dates.outVal,
      nights: dates.nights,
      adults,
    };
    localStorage.setItem("booking", JSON.stringify(payload));
    window.location.href = "oplata.html";
  }

  // Находим потенциальные кнопки "Reserve"
  const candidates = new Set([
    ...$$("button"),
    ...$$("a"),
    ...$$(".reserve-btn"),
  ]);

  candidates.forEach((btn) => {
    const txt = (btn.textContent || "").trim().toLowerCase();
    if (!txt.includes("reserve")) return; // пропускаем нецелевые кнопки

    btn.addEventListener("click", (e) => {
      e.preventDefault();

      // Ищем контейнер комнаты рядом с кнопкой
      const row =
        btn.closest("[data-room]") ||
        btn.closest(".room-card") ||
        btn.closest(".room-row") ||
        btn.closest("article") ||
        btn.closest("li") ||
        btn.parentElement;

      // Имя номера
      const roomName =
        row?.querySelector("[data-room-name]")?.dataset.roomName ||
        row?.querySelector(".room-name,h3,.title")?.textContent?.trim() ||
        "Room";

      // Цена за ночь
      const priceAttr = row?.dataset.price || row?.dataset.pricePerNight;
      const priceEl =
        row?.querySelector("[data-price]") ||
        row?.querySelector(".room-price,.price,[class*='price']");
      const pricePerNight = priceAttr
        ? +priceAttr
        : numFromText(priceEl?.textContent);

      // Даты/гости по умолчанию
      const dates = getDefaultDates();
      const adults = 2;

      // Название отеля
      const hotel = getHotelName();

      // Сохраняем и переходим
      saveAndGo({ hotel, roomName, pricePerNight, dates, adults });
    });
  });
})();
