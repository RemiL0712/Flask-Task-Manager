import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Визначаємо базовий шлях до папки проєкту
basedir = os.path.abspath(os.path.dirname(__file__))

# Ініціалізуємо Flask-додаток
app = Flask(__name__)
CORS(app)  # Додаємо підтримку CORS для фронтенду

# Налаштовуємо базу даних SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Створюємо екземпляр SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Підключаємо Flask-Migrate

# =====================================================================
# МОДЕЛЬ ТАБЛИЦІ "Task"
# =====================================================================
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)                # Унікальний ID
    name = db.Column(db.String(80), unique=True, nullable=False) # Назва завдання
    status = db.Column(db.Boolean, default=False, nullable=False) # Виконано / не виконано
    priority = db.Column(db.String(20), nullable=False)           # Пріоритет
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата створення

    def __repr__(self):
        return f'<Task {self.name}>'

# =====================================================================
# ROUTES (МАРШРУТИ)
# =====================================================================

# Головна сторінка
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

# API: Додати завдання (POST)
@app.route('/api/add', methods=['POST'])
def api_add_task():
    data = request.get_json()
    task_name = data.get('task_name')
    task_priority = data.get('priority')

    # Валідація
    if not task_name or not task_priority:
        return jsonify({'error': 'Всі поля повинні бути заповнені'}), 400
    if task_priority not in ['low', 'medium', 'high']:
        return jsonify({'error': 'Невірний пріоритет'}), 400
    if Task.query.filter_by(name=task_name).first():
        return jsonify({'error': 'Завдання з такою назвою вже існує'}), 409

    new_task = Task(name=task_name, priority=task_priority)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        'id': new_task.id,
        'name': new_task.name,
        'priority': new_task.priority,
        'status': new_task.status,
        'created_at': new_task.created_at.isoformat()
    }), 201

# API: Видалити завдання (DELETE)
@app.route('/api/delete/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Завдання видалено'}), 200

# API: Змінити статус завдання (PATCH)
@app.route('/api/complete/<int:task_id>', methods=['PATCH'])
def api_complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = not task.status
    db.session.commit()
    return jsonify({'status': task.status}), 200

# API: Оновити назву (PUT)
@app.route('/api/update/<int:task_id>', methods=['PUT'])
def api_update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    new_name = data.get('new_name')

    if not new_name:
        return jsonify({'error': 'Назва не може бути порожньою'}), 400
    if Task.query.filter(Task.name == new_name, Task.id != task_id).first():
        return jsonify({'error': 'Завдання з такою назвою вже існує'}), 409

    task.name = new_name
    db.session.commit()
    return jsonify({'name': task.name}), 200

# =====================================================================
# Запуск
# =====================================================================
if __name__ == '__main__':
    app.run(debug=True)
