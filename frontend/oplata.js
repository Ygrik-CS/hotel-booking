// Форматирует число в доллары, например 73 → US$73.00
const fmtUSD = (n) => "US$" + n.toFixed(2);

// Ставка НДС (12%)
const VAT_RATE = 0.12;

// Загружает данные брони из localStorage
function loadBooking() {
  const raw = localStorage.getItem("booking"); // берём строку
  if (!raw) return null; // если ничего нет — возвращаем null
  try {
    return JSON.parse(raw); // пробуем превратить строку в объект
  } catch {
    return null; // если ошибка — тоже null
  }
}

// Основная функция для отображения данных брони
function render() {
  const b = loadBooking() || {}; // берём бронь или пустой объект

  // Значения по умолчанию, если данных нет
  const hotel = b.hotel || "Pana Ayusai";
  const checkIn = b.checkIn || "2025-10-21";
  const checkOut = b.checkOut || "2025-10-22";
  const nights = Number(b.nights || 1);
  const price = Number(b.pricePerNight || 73);
  const adults = b.adults || 2;

  // Отображаем краткую информацию о брони
  document.getElementById("sumHotel").textContent = hotel;

  // Преобразуем даты в удобный формат
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
  document.getElementById("sumDates").textContent = datesStr;

  // Количество ночей и гостей
  document.getElementById("sumNights").textContent = `${nights} night${
    nights > 1 ? "s" : ""
  }`;
  document.getElementById("sumNightCount").textContent = nights;
  document.getElementById("sumGuests").textContent = `${adults} adult${
    adults > 1 ? "s" : ""
  }`;

  // Подсчёт итогов
  const subtotal = price * nights; // цена за все ночи
  const vat = subtotal * VAT_RATE; // налог
  const total = subtotal + vat; // общая сумма

  // Выводим суммы в HTML
  document.getElementById("sumSubtotal").textContent = fmtUSD(subtotal);
  document.getElementById("sumVat").textContent = fmtUSD(vat);
  document.getElementById("sumTotal").textContent = fmtUSD(total);

  // Trip Coins (как бонусы)
  const coins = Math.round(total * 0.5); // начисляем 0.5% от суммы
  document.getElementById("coins").textContent = `${coins} Trip Coins`;
  document.getElementById("coinsUsd").textContent = fmtUSD(coins / 100);
}

// Промокод
document.getElementById("applyPromo").addEventListener("click", () => {
  const v = document.getElementById("promo").value.trim(); // читаем ввод
  const note = document.getElementById("promoNote");
  if (!v) {
    // если поле пустое — скрываем уведомление
    note.classList.add("hidden");
    return;
  }
  // иначе показываем сообщение
  note.classList.remove("hidden");
});

// Отправка формы
document.getElementById("bookingForm").addEventListener("submit", (e) => {
  e.preventDefault(); // блокируем стандартную отправку
  alert("Booking submitted ✅"); // показываем сообщение
});

// Запуск отрисовки при загрузке страницы
render();
