import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from datetime import date
from functools import lru_cache
import time

st.set_page_config(page_title="Hotel Booking System", layout="centered")
st.title("Hotel Booking System")
st.subheader("Бронирование отелей")

@lru_cache(maxsize=500)
def quote_offer(hotel_id, room_type, checkin, checkout, guests):
    base_prices = {"Стандарт":18000,"Люкс":29000,"Семейный":24000}
    availability = {"Стандарт":3,"Люкс":0,"Семейный":2}
    tax=0.12
    markup=0.05
    days=(date.fromisoformat(checkout)-date.fromisoformat(checkin)).days
    base_price=base_prices.get(room_type,18000)
    total=int(base_price*days*(1+tax+markup))
    available=availability.get(room_type,0)>0
    return total,available

st.sidebar.header("Навигация")
page=st.sidebar.radio("Разделы",["Главная","Оценка предложения","Отчёты"])

if page=="Главная":
    st.write("Пример системы бронирования с использованием мемоизации для ускорения расчётов.")

elif page=="Оценка предложения":
    with st.form("quote_form"):
        name=st.text_input("Имя клиента")
        hotel_id=st.text_input("ID отеля","hotel_001")
        room_type=st.selectbox("Тип номера",["Стандарт","Люкс","Семейный"])
        checkin=st.date_input("Дата заезда",value=date(2025,10,1))
        checkout=st.date_input("Дата выезда",value=date(2025,10,5))
        guests=st.number_input("Количество гостей",1,6,2)
        submit=st.form_submit_button("Рассчитать")

    if submit:
        if checkout<=checkin:
            st.error("Дата выезда должна быть позже даты заезда")
        else:
            t1=time.perf_counter()
            total,available=quote_offer(hotel_id,room_type,str(checkin),str(checkout),guests)
            t2=time.perf_counter()
            st.write(f"Время расчёта: {(t2-t1)*1000:.2f} мс")
            if not available:
                st.warning(f"Номера типа «{room_type}» недоступны")
            else:
                st.success(f"Предложение для {name}: {room_type}, {checkin}–{checkout}, гостей: {guests}, цена: {total} ₸")

elif page=="Отчёты":
    st.write("При повторных запросах того же номера расчёт происходит быстрее за счёт кэширования lru_cache.")
