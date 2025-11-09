# Flask Task Manager

Production‑ready Flask застосунок з JWT‑автентифікацією, REST API (Swagger UI), SQLAlchemy + Migrations, `.env` конфігурацією та Docker.

## ✨ Ключові можливості
- **JWT**: реєстрація/логін та захист API
- **Tasks CRUD**: створення, читання, оновлення, видалення
- **Фільтри**: `?q=` (пошук за назвою), `?status=`
- **Swagger UI**: інтерактивна документація на `/api/`
- **ORM + Migrations**: Flask‑SQLAlchemy + Flask‑Migrate
- **.env**: безпечні секрети та налаштування
- **Docker**: `Dockerfile` + `docker-compose.yml`
- Структура з **Blueprints/Namespaces** (api/models/routes/extensions)

## 🧭 Структура
```
task_manager/
  api/         # REST API (Flask-RESTX namespaces)
  extensions/  # db, migrate, jwt, api
  models/      # User, Task
  routes/      # server-rendered routes
  static/      # CSS/JS
  templates/   # Jinja templates
wsgi.py        # entry point
```

## 🚀 Швидкий старт (локально)
```bash
python -m venv .venv && . .venv/bin/activate    # Win: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask db init && flask db migrate -m "init" && flask db upgrade
python wsgi.py
# відкрий http://127.0.0.1:5000/api/
```

## 🐳 Docker
```bash
cp .env.example .env
docker compose up --build
# відкрий http://localhost:5000/api/
```

## 🔐 Ендпоїнти (коротко)
```
POST   /api/auth/register       {email, password}
POST   /api/auth/login          → {access_token}

GET    /api/tasks               (JWT)
POST   /api/tasks               (JWT)  {title, description?, status?}
GET    /api/tasks/<id>          (JWT)
PUT    /api/tasks/<id>          (JWT)
DELETE /api/tasks/<id>          (JWT)
```

## 📦 Оточення
Див. `.env.example`:
```
DATABASE_URL=sqlite:///task_manager.db
SECRET_KEY=please-change-me
JWT_SECRET_KEY=please-change-me-too
```

## 📝 Ліцензія
MIT
