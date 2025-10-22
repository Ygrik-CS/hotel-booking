// Массив слайдов для карусели каждая запись это объект с путём к картинке
const slides = [
  { src: "images/pexels-fotoaibe-1743231.jpg", link: "https://example1.com" },
  { src: "images/pexels-karlsolano-2883047.jpg", link: "https://example2.com" },
  { src: "images/pexels-pixabay-164595.jpg", link: "https://example3.com" },
];

// Код запускается, когда вся страница полностью загружена
document.addEventListener("DOMContentLoaded", () => {
  // Находим элементы изображения и ссылки
  const img = document.getElementById("heroCarouselImg");
  const link = document.getElementById("heroCarouselLink");

  // Прелоад изображений
  // Это нужно, чтобы картинки заранее загрузились
  slides.forEach((s) => {
    const im = new Image(); // создаём объект картинки
    im.src = s.src;         // указываем путь к файлу, браузер подгружает его в кэш
  });

  // Начальные значения 
  // С какого слайда начинаем (индекс 0 — первый элемент массива)
  let i = 0;
  // Устанавливаем первую картинку и её ссылку
  img.src = slides[i].src;
  link.href = slides[i].link;

  // Поиск города
  document.getElementById('searchBtn').addEventListener('click', goSearch); // при клике на кнопку
  document.getElementById('cityInput').addEventListener('keydown', (e) => {
    // если пользователь нажал Enter — тоже запускаем поиск
    if (e.key === 'Enter') goSearch();
  });

  // Функция поиска
  function goSearch() {
    // Получаем значение из поля ввода, убираем пробелы и переводим в нижний регистр
    const input = document.getElementById('cityInput').value.trim().toLowerCase();

    // Проверяем, содержит ли ввод название одного из доступных городов
    if (input.includes("almaty") || input.includes("алматы")) {
      // Если да переходим на страницу отелей для этого города
      window.location.href = "hotels.html?city=almaty";
    } else if (input.includes("astana") || input.includes("астана")) {
      window.location.href = "hotels.html?city=astana";
    } else if (input.includes("aktau") || input.includes("актау")) {
      window.location.href = "hotels.html?city=aktau";
    } else {
      // Если город не найден — показываем сообщение пользователю
      alert("Город не найден. Введите Almaty, Astana или Aktau.");
    }
  }
});