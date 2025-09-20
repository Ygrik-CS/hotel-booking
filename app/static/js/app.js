// Простой фронтенд: получает отели → комнаты → делает бронирование (fetch)
document.addEventListener("DOMContentLoaded", function() {
  const hotelSelect = document.getElementById("hotelSelect");
  const roomsList = document.getElementById("roomsList");
  const bookingForm = document.getElementById("bookingForm");
  const bookingResult = document.getElementById("bookingResult");
  const allBookings = document.getElementById("allBookings");

  function loadHotels() {
    fetch("/api/hotels")
      .then(r => r.json())
      .then(data => {
        hotelSelect.innerHTML = "<option value=''>-- выберите отель --</option>";
        data.forEach(h => {
          const opt = document.createElement("option");
          opt.value = h.id;
          opt.textContent = `${h.name} — ${h.city} (${h.stars}★)`;
          hotelSelect.appendChild(opt);
        });
      })
      .catch(e => console.error(e));
  }

  function loadRooms(hotelId) {
    if (!hotelId) {
      roomsList.innerHTML = "Выберите отель, чтобы увидеть комнаты";
      return;
    }
    fetch(`/api/rooms/hotel/${hotelId}`)
      .then(r => r.json())
      .then(data => {
        if (!data.length) {
          roomsList.innerHTML = "Комнат не найдено";
          return;
        }
        roomsList.innerHTML = "";
        data.forEach(room => {
          const div = document.createElement("div");
          div.innerHTML = `<strong>Комната ${room.number}</strong> (ID ${room.id}) — вмещает ${room.capacity}, цена ${room.price} USD<br>${room.description}`;
          roomsList.appendChild(div);
        });
      })
      .catch(e => console.error(e));
  }

  function loadAllBookings() {
    fetch("/api/bookings")
      .then(r => r.json())
      .then(data => {
        if (!data.length) {
          allBookings.innerHTML = "Список бронирований пуст";
          return;
        }
        allBookings.innerHTML = "";
        data.forEach(b => {
          const div = document.createElement("div");
          div.textContent = `ID ${b.id} — Room ${b.room_id} — ${b.guest_name} — ${b.date_from} → ${b.date_to}`;
          allBookings.appendChild(div);
        });
      })
      .catch(e => console.error(e));
  }

  hotelSelect.addEventListener("change", function() {
    loadRooms(this.value);
  });

  bookingForm.addEventListener("submit", function(ev) {
    ev.preventDefault();
    bookingResult.textContent = "Отправка...";
    const payload = {
      room_id: parseInt(document.getElementById("roomId").value, 10),
      guest_name: document.getElementById("guestName").value,
      date_from: document.getElementById("dateFrom").value,
      date_to: document.getElementById("dateTo").value
    };
    fetch("/api/bookings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
    .then(async res => {
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Ошибка");
      }
      return res.json();
    })
    .then(b => {
      bookingResult.textContent = `Успех: бронирование ID ${b.id}`;
      loadAllBookings();
    })
    .catch(err => {
      bookingResult.textContent = `Ошибка: ${err.message}`;
    });
  });

  // начальная загрузка
  loadHotels();
  loadAllBookings();
});
