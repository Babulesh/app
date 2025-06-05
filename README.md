# Hotel Booking API

API для управления номерами отеля и бронированиями

## Установка

### Вариант 1: С Docker (рекомендуется)
1. Убедитесь, что у вас установлены Docker и Docker Compose
2. Клонируйте репозиторий
3. Выполните:
   ```bash
   docker-compose up --build
   ```
4. Примените миграции:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

### Вариант 2: Без Docker
1. Установите Python 3.8+
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Настройте базу данных в `hotel/settings.py`
4. Выполните:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Примеры запросов

### Работа с номерами
- Создание номера:
  ```bash
  curl -X POST http://localhost:8000/rooms/create/ \
  -H "Content-Type: application/json" \
  -d '{"description":"Люкс с видом на море", "price_per_night": 15000}'
  ```

- Список номеров (сортировка по цене):
  ```bash
  curl -X GET "http://localhost:8000/rooms/list/?sort_by=price_asc"
  ```

### Работа с бронированиями
- Создание брони:
  ```bash
  curl -X POST http://localhost:8000/bookings/create/ \
  -H "Content-Type: application/json" \
  -d '{"room_id":1, "date_start":"2023-12-25", "date_end":"2023-12-30"}'
  ```

- Список бронирований номера:
  ```bash
  curl -X GET "http://localhost:8000/bookings/list/?room_id=1"
  ```

## Описание API

### Номера отеля
- `POST /rooms/create/` - Создание номера
- `DELETE /rooms/delete/` - Удаление номера
- `GET /rooms/list/` - Список номеров с сортировкой

### Бронирования
- `POST /bookings/create/` - Создание брони
- `DELETE /bookings/delete/` - Удаление брони
- `GET /bookings/list/` - Список бронирований

## Запуск в production
Для production используйте:
```bash
docker-compose -f docker-compose.prod.yml up --build -d
