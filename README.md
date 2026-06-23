<details>
<summary>📸 Скриншот</summary>

![Screenshot](https://raw.githubusercontent.com/Rrezzak09VPN/remnawave-dashboard-widget/main/screenshot.png)

</details>

<br>

# 🖥 Remnawave Live Dashboard

Визуальный дашборд для мониторинга **Remnawave** панели в реальном времени.
Отображает состояние нод, онлайн пользователей, погоду, время и календарь — всё в одном окне.

## 🚀 Возможности

- **Мониторинг нод Remnawave** — CPU, RAM, Load Average, трафик, количество онлайн пользователей
- **Список онлайн пользователей** — кто подключен и через какую ноду (активность менее 30 секунд)
- **Погода** — поиск города, температура, влажность, ветер (бесплатно, без API-ключа)
- **Часы** — точное время с учётом часового пояса выбранного города
- **Календарь** — с навигацией по месяцам/неделям
- **Автообновление** каждые 10 секунд (ноды и пользователи), каждые 10 минут (погода)
- **FLIP-анимации** — плавное перемещение карточек при сортировке

## ⚙ Быстрый старт

### Windows
1. Скачайте проект в любую папку
2. Запустите **`run_dashboard.bat`** — скрипт сам установит зависимости (fastapi, httpx, uvicorn) и откроет браузер

### Linux / macOS
```
pip install fastapi httpx uvicorn
python start_dashboard.py
```

Дашборд откроется по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 🔧 Настройка (start_dashboard.py)

Откройте файл и укажите данные вашей Remnawave панели:

```python
REMNA_API_URL = "https://panel.example.com"   # Адрес вашей панели
REMNA_TOKEN = "eyJhbGciOiJI..."               # API токен Remnawave
COOKIE_SECRET = ""                             # Cookie (если требуется)
```

### Вариант 1: Прямое подключение (Docker / Bare Metal)
Если панель доступна напрямую — оставьте COOKIE_SECRET пустым ("").

### Вариант 2: Панель за Nginx (с Cookie-авторизацией)
Если ваша Remnawave панель за Nginx — вставьте в COOKIE_SECRET значение Cookie, которое вы получили при установке панели (его обычно сохраняют в текстовый файл).

Если вы не сохранили Cookie — откройте панель в браузере, нажмите F12 → вкладка Network, обновите страницу (F5), найдите любой запрос к API, скопируйте значение заголовка Cookie: и вставьте в COOKIE_SECRET.

## 📦 Структура проекта

- start_dashboard.py — backend на FastAPI (прокси к Remnawave API + погода)
- END.html — frontend с интерфейсом дашборда
- run_dashboard.bat — скрипт запуска для Windows
- screenshot.png — скриншот дашборда

## 📄 Лицензия

MIT

## ❤️ Community

Сделано для сикретнова чатика камунити Remnawave
