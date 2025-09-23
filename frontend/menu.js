const slides = [
  { src: "images/pexels-fotoaibe-1743231.jpg", link: "https://example1.com" },
  { src: "images/pexels-karlsolano-2883047.jpg", link: "https://example2.com" },
  { src: "images/pexels-pixabay-164595.jpg", link: "https://example3.com" },
];

document.addEventListener("DOMContentLoaded", () => {
  const img = document.getElementById("heroCarouselImg");
  const link = document.getElementById("heroCarouselLink");

  // Прелоад, чтобы не было «миганий»
  slides.forEach((s) => {
    const im = new Image();
    im.src = s.src;
  });

  // Стартовые значения
  let i = 0;
  img.src = slides[i].src;
  link.href = slides[i].link;

  function show(idx) {
    // плавно скрываем
    img.style.opacity = "0";
    img.addEventListener(
      "transitionend",
      function onFadeOut() {
        img.removeEventListener("transitionend", onFadeOut);
        // меняем картинку и ссылку
        img.src = slides[idx].src;
        link.href = slides[idx].link;
        // следующий кадр — плавно показываем
        requestAnimationFrame(() => {
          img.style.opacity = "1";
        });
      },
      { once: true }
    );
  }

  // Автосмена каждые 3 секунды
  setInterval(() => {
    i = (i + 1) % slides.length;
    show(i);
  }, 3000);
});
// Поиск города
document.getElementById('searchBtn').addEventListener('click', goSearch);
document.getElementById('cityInput').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') goSearch();
});

function goSearch() {
  const input = document.getElementById('cityInput').value.trim().toLowerCase();

  if (input.includes("almaty") || input.includes("алматы")) {
    window.location.href = "hotels.html?city=almaty";
  } else if (input.includes("astana") || input.includes("астана")) {
    window.location.href = "hotels.html?city=astana";
  } else if (input.includes("aktau") || input.includes("актау")) {
    window.location.href = "hotels.html?city=aktau";
  } else {
    alert("Город не найден. Введите Almaty, Astana или Aktau.");
  }
}
