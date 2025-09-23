const $ = (s, p = document) => p.querySelector(s);
const $$ = (s, p = document) => [...p.querySelectorAll(s)];
const cards = () => $$("#list article");

// ===== Nights counter (robust) =====
const inEl = $("#qIn"),
  outEl = $("#qOut"),
  nightsEl = $("#qNights");
function setDefaultDates() {
  const today = new Date();
  const inDate = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate() + 1
  );
  const outDate = new Date(
    today.getFullYear(),
    today.getMonth(),
    today.getDate() + 10
  );
  inEl.valueAsDate = inDate;
  outEl.valueAsDate = outDate;
  updNights();
}
function daysBetween(a, b) {
  return Math.round((b - a) / (1000 * 60 * 60 * 24));
}
function updNights() {
  const a = new Date(inEl.value),
    b = new Date(outEl.value);
  if (!isNaN(a) && !isNaN(b) && b > a) {
    const n = Math.max(1, daysBetween(a, b));
    nightsEl.textContent = `${n} night${n > 1 ? "s" : ""}`;
    // reflect the same number inside cards (where shown)
    $$(".nights").forEach((el) => (el.textContent = n));
  } else {
    nightsEl.textContent = "";
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

// ===== Filters =====
const priceRange = $("#fPrice"),
  priceLabel = $("#priceLabel");
const cityTag = $("#cityTag");
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
  // reflect city tag + search bar city
  cityTag.textContent = city || $("#qCity").value || "Any";
  let qCity = $("#qCity").value.trim().toLowerCase();

  cards().forEach((c) => {
    const okName = !name || c.dataset.name.toLowerCase().includes(name);
    const okCity = !city || c.dataset.city === city;
    const okQCity = !qCity || c.dataset.city.toLowerCase().includes(qCity);
    const okPrice = +c.dataset.price <= priceMax;
    const okBreakfast = !flags.breakfast || c.dataset.breakfast === "true";
    const okPool = !flags.pool || c.dataset.pool === "true";
    const okMuseum = !flags.museum || c.dataset.museum === "true";
    const okGreat = !flags.great || c.dataset.great === "true";
    const okHotel = !flags.hotel || c.dataset.hotel === "true";

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
    c.classList.toggle("hidden", !ok);
  });
  updateFound();
  sortCards(); // keep order after filter
}
priceRange.addEventListener(
  "input",
  (e) => (priceLabel.textContent = "$" + e.target.value)
);
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
  applyFilters();
});
$("#qSearch").addEventListener("click", applyFilters);
$("#qCity").addEventListener("input", applyFilters);

// ===== Sorting =====
function sortCards() {
  const mode = $("#sort").value;
  const list = $("#list");
  const items = cards().filter((c) => !c.classList.contains("hidden"));
  items.sort((a, b) => {
    const pa = +a.dataset.price,
      pb = +b.dataset.price;
    const ra = +a.dataset.rating,
      rb = +b.dataset.rating;
    if (mode === "priceAsc") return pa - pb;
    if (mode === "priceDesc") return pb - pa;
    if (mode === "ratingDesc") return rb - ra;
    return 0;
  });
  items.forEach((el) => list.appendChild(el));
}
$("#sort").addEventListener("change", sortCards);

// init
applyFilters();

document.addEventListener('DOMContentLoaded', () => {
  const urlParams = new URLSearchParams(window.location.search);
  const city = urlParams.get('city'); // almaty / astana / aktau

  const cards = document.querySelectorAll('.hotel-card');
  let shown = 0;

  cards.forEach(card => {
    if (!city || card.dataset.city === city) {
      card.classList.remove('hidden');
      shown++;
    } else {
      card.classList.add('hidden');
    }
  });

  if (shown === 0) {
    document.body.insertAdjacentHTML("beforeend",
      "<p class='text-center text-slate-500 mt-10'>Нет отелей для этого города</p>");
  }
})
