# Brand Click Tracker

Тестовое задание: адаптивный лендинг Dell с учётом кликов и переходом на официальный сайт.

Стек: React, JavaScript, CSS, Vite, Python, FastAPI, SQLAlchemy, PostgreSQL, Docker Compose. При разработке использовал ChatGPT.

Лендинг после публикации GitHub Pages: https://Ilia-Savch.github.io/brand-click-tracker/

Репозиторий: https://github.com/Ilia-Savch/brand-click-tracker

## Запуск backend

Нужны Git и запущенный Docker Desktop с Linux-контейнерами. Python и PostgreSQL отдельно устанавливать не нужно.

```powershell
git clone https://github.com/Ilia-Savch/brand-click-tracker.git
cd brand-click-tracker
Copy-Item .env.example .env
docker compose up --build -d --wait
```

Для Linux/macOS вместо Copy-Item: `cp .env.example .env`.

Если `.env` уже существует, повторно копировать его не нужно. Порт 8000 должен быть свободен: ранее запущенный локальный Uvicorn нужно остановить.

После запуска откройте лендинг в браузере на этом же компьютере. CTA обращаются к http://127.0.0.1:8000. На другом устройстве, в том числе телефоне, localhost указывает на это устройство. Если браузер запрашивает доступ к локальной сети, разрешите его для тестирования.

API: http://127.0.0.1:8000/docs

Клики: http://127.0.0.1:8000/clicks

```powershell
docker compose logs -f backend
docker compose down
```

Первая команда показывает логи, вторая останавливает проект. Данные PostgreSQL сохраняются в volume после остановки. Не используйте `down -v`, если хотите сохранить клики.

## Логика

`GET /click?offer=Dell&sub1=hero` создаёт уникальный UUID, сохраняет click_id, offer, sub1, время UTC, IP и User-Agent в БД, затем возвращает 302 на https://www.dell.com/. Параметры сохраняются без изменения. Если запись не удалась, редирект не выполняется.

`GET /clicks` возвращает все клики в JSON. Кнопки передают sub1: `hero`, `categories`, `footer`. За Docker Desktop адрес клиента может отображаться как адрес шлюза Docker.

Проверить редирект без перехода на Dell:

```powershell
curl.exe -i "http://127.0.0.1:8000/click?offer=Dell&sub1=test123"
```

Ожидается статус 302, Location с адресом Dell и новая запись в `/clicks`. В Linux/macOS используйте `curl` вместо `curl.exe`.

## Frontend и аналитика

GTM: `GTM-T5SSF4VV`. GA4: `G-MNMZS3XY6J`, подключён через GTM. Нажатия отправляют `cta_click` с параметрами `offer` и `cta_id`. Получение события и `cta_id=hero` проверено в DebugView, настройки GTM опубликованы.

Для локальной разработки нужен Node.js 22.12+:

```powershell
cd frontend
Copy-Item .env.example .env
npm ci
npm run dev
```

Проверки: `npm run lint` и `npm run build` из папки frontend.

Блокировщики и VPN могут мешать аналитике или открытию Dell. Backend сохраняет клики независимо от Google Analytics. Лендинг — учебный проект, не официальный сайт Dell.
