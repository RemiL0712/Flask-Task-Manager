# app.py
# Головний файл веб-додатку "Менеджер Завдань" на Flask.
# Він відповідає за налаштування сервера, взаємодію з базою даних
# та обробку всіх HTTP-запитів.

import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

# =====================================================================
# 1. НАЛАШТУВАННЯ ДОДАТКУ
# =====================================================================

# Визначаємо базовий шлях для коректного знаходження файлів
basedir = os.path.abspath(os.path.dirname(__file__))

# Ініціалізація Flask-додатку
app = Flask(__name__)

# Додавання підтримки CORS для дозволу запитів з інших доменів
CORS(app)

# Конфігурація бази даних SQLite
# База даних буде створена у файлі tasks.db в корені проєкту
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Створення екземплярів SQLAlchemy та Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# =====================================================================
# 2. МОДЕЛЬ ДАНИХ
# =====================================================================

# Визначення моделі "Task" для таблиці в базі даних
class Task(db.Model):
    # Унікальний числовий ідентифікатор (primary key)
    id = db.Column(db.Integer, primary_key=True)
    # Назва завдання, має бути унікальною та не може бути порожньою
    name = db.Column(db.String(80), unique=True, nullable=False)
    # Статус завдання: False (не виконано) або True (виконано)
    status = db.Column(db.Boolean, default=False, nullable=False)
    # Пріоритет, зберігається як рядок ('high', 'medium', 'low')
    priority = db.Column(db.String(20), nullable=False)
    # Час створення завдання, автоматично встановлюється
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Метод для зручного представлення об'єкта при налагодженні
    def __repr__(self):
        return f'<Task id={self.id} name="{self.name}" status={self.status}>'

# =====================================================================
# 3. МАРШРУТИЗАЦІЯ (РОУТИНГ)
# =====================================================================

# Головний маршрут, що відображає основну сторінку додатка
@app.route('/')
def index():
    # Запит до бази даних для отримання всіх завдань, відсортованих за ID
    tasks = Task.query.order_by(Task.id).all()
    # Відображення HTML-шаблону, передаючи дані завдань
    return render_template('index.html', tasks=tasks)

# =====================================================================
# 4. API ENDPOINTS (ДЛЯ JAVASCRIPT)
# =====================================================================

# API-маршрут для створення нового завдання
@app.route('/api/add', methods=['POST'])
def api_add_task():
    # Отримання даних у форматі JSON з тіла запиту
    data = request.get_json()
    task_name = data.get('task_name')
    priority = data.get('priority')

    # Валідація вхідних даних
    if not task_name or not priority:
        # Повернення помилки 400 (Bad Request), якщо дані неповні
        return jsonify({'error': 'Назва та пріоритет є обов\'язковими'}), 400

    new_task = Task(name=task_name, priority=priority)
    try:
        db.session.add(new_task)
        db.session.commit()
        # Повернення успішної відповіді 201 (Created) з даними нового завдання
        return jsonify({
            'id': new_task.id,
            'name': new_task.name,
            'status': new_task.status,
            'priority': new_task.priority,
            'created_at': new_task.created_at.isoformat()
        }), 201
    except IntegrityError:
        # Обробка випадку, коли завдання з такою назвою вже існує
        db.session.rollback()
        return jsonify({'error': 'Завдання з такою назвою вже існує.'}), 409
    except Exception as e:
        # Загальна обробка інших невідомих помилок
        db.session.rollback()
        return jsonify({'error': f'Невідома помилка: {str(e)}'}), 500

# API-маршрут для видалення завдання
@app.route('/api/delete/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    # Пошук завдання за ID, автоматично повертає 404, якщо не знайдено
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Завдання видалено'}), 200

# API-маршрут для зміни статусу завдання
@app.route('/api/complete/<int:task_id>', methods=['PATCH'])
def api_complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    # Інвертування статусу (True -> False, False -> True)
    task.status = not task.status
    db.session.commit()
    return jsonify({'status': task.status}), 200

# API-маршрут для оновлення назви завдання
@app.route('/api/update/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    new_name = data.get('new_name')

    if not new_name:
        return jsonify({'error': 'Назва не може бути порожньою'}), 400

    task.name = new_name
    db.session.commit()
    return jsonify({
        'id': task.id,
        'name': task.name,
        'status': task.status,
        'priority': task.priority
    }), 200

# =====================================================================
# 5. ЗАПУСК ДОДАТКУ
# =====================================================================

# Стандартна конструкція для запуску сервера, якщо файл запускається безпосередньо
if __name__ == '__main__':
    app.run(debug=True)
    