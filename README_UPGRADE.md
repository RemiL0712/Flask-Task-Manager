# Flask Task Manager — Upgraded

## Що додано
- ✅ Структура проєкту з **Blueprints** і чітким розділенням (api/models/routes/services)
- ✅ **REST API** з інтерактивною документацією (**Flask-RESTX**) на `/api/`
- ✅ **JWT**-автентифікація: `/api/auth/register`, `/api/auth/login`
- ✅ CRUD для задач: `/api/tasks`
- ✅ **SQLAlchemy** + **Flask-Migrate** (migrations)
- ✅ **.env** конфігурація, `Dockerfile`, `docker-compose.yml`
- ✅ Базова HTML-сторінка (`/`)

## Запуск локально
```bash
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask db init && flask db migrate -m "init" && flask db upgrade
python wsgi.py
# відкрий: http://127.0.0.1:5000/api/  (Swagger)
```

## Запуск у Docker
```bash
cp .env.example .env
docker compose up --build
# відкрий: http://localhost:5000/api/
```

## Міграція з твого оригінального коду
1. Перенеси свої моделі у `task_manager/models/` (або доповни існуючі).
2. Додай свої HTML/Jinja у `task_manager/templates/` і статику у `task_manager/static/`.
3. Якщо були старі Flask-роути — перемісти у `task_manager/routes/`.
4. Якщо був API — перенеси логіку у `task_manager/api/` (як ресурси RESTX).
5. Онови `requirements.txt` при потребі (наприклад, якщо використовував сторонні пакети).

## Де документація API
Переходь на `/api/` — там Swagger UI та схеми запитів/відповідей.
