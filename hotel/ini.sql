-- Создание таблицы номеров отеля
CREATE TABLE hotel_booking_hotelroom (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    price_per_night DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Создание таблицы бронирований
CREATE TABLE hotel_booking_booking (
    id SERIAL PRIMARY KEY,
    room_id INTEGER NOT NULL,
    date_start DATE NOT NULL,
    date_end DATE NOT NULL,
    FOREIGN KEY (room_id) REFERENCES hotel_booking_hotelroom(id) ON DELETE CASCADE
);

-- Индексы для оптимизации
CREATE INDEX idx_hotelroom_price ON hotel_booking_hotelroom(price_per_night);
CREATE INDEX idx_hotelroom_created ON hotel_booking_hotelroom(created_at);
CREATE INDEX idx_booking_dates ON hotel_booking_booking(date_start, date_end);