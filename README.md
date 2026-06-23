<details>
<summary>📸 Скриншот</summary>

![Screenshot](https://raw.githubusercontent.com/Rrezzak09VPN/remnawave-dashboard-widget/main/screenshot.png)

</details>

<br>

## 🖥 Remnawave Live Dashboard

Визуальный дашборд для мониторинга **Remnawave** панели в реальном времени.
Отображает состояние нод, онлайн пользователей, погоду, время и календарь — всё в одном окне.

## 🚀 Возможности

- **Мониторинг нод Remnawave** — CPU, RAM, Load Average, трафик, количество онлайн пользователей
- **Список онлайн пользователей** — кто подключен и через какую ноду (фильтр: активность < 30 секунд)
- **Погода** — поиск города, отображение температуры, влажности, ветра (бесплатно, без API-ключа)
- **Часы** — точное время с поддержкой часового пояса выбранного города
- **Календарь** — с навигацией по месяцам/неделям
- **Автообновление** каждые 10 секунд для нод и пользователей, каждые 10 минут для погоды
- **Анимации FLIP** — плавное перемещение карточек нод при сортировке

## ⚙ Быстрый старт

### Windows
1. Скачайте проект в любую папку (например, C:\Dashboard)
2. Запустите **un_dashboard.bat** — скрипт сам установит зависимости (astapi, httpx, uvicorn) и откроет браузер

### Linux / macOS
`ash
pip install fastapi httpx uvicorn
python start_dashboard.py
`

Дашборд откроется по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 🔧 Настройка (start_dashboard.py)

Откройте файл и укажите данные вашей Remnawave панели:

`python
REMNA_API_URL = "https://panel.example.com"   # Адрес вашей панели
REMNA_TOKEN = "eyJhbGciOiJI..."               # API токен Remnawave
COOKIE_SECRET = ""                             # Cookie-секрет (если требуется)
`

### Вариант 1: Прямое подключение (Docker / Bare Metal)
Если панель доступна напрямую — оставьте COOKIE_SECRET пустым ("").

### Вариант 2: Через Nginx с Cookie
Если панель защищена Nginx и требует Cookie для доступа:
1. Откройте панель в браузере, нажмите F12 → вкладка **Network**
2. Обновите страницу (F5), найдите любой запрос к API
3. В **Request Headers** скопируйте значение Cookie: и вставьте в COOKIE_SECRET

## 📦 Структура проекта

- start_dashboard.py — backend на FastAPI (прокси к Remnawave API + погода)
- END.html — frontend с интерфейсом дашборда
- un_dashboard.bat — скрипт запуска для Windows
- screenshot.png — скриншот дашборда

## 📄 Лицензия

MIT