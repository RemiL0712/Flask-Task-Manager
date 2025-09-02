import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Визначаємо базовий шлях до папки проєкту
basedir = os.path.abspath(os.path.dirname(__file__))

# Ініціалізуємо Flask-додаток
app = Flask(__name__)

# Налаштовуємо базу даних SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Створюємо екземпляр SQLAlchemy
db = SQLAlchemy(app)

# ============================================================================
# Визначаємо модель даних для наших завдань
# Це клас, який відповідає за структуру таблиці в базі даних
# ============================================================================
class Task(db.Model):
    # Унікальний ідентифікатор завдання, автоматично інкрементується
    id = db.Column(db.Integer, primary_key=True)
    # Назва завдання, унікальна і не може бути порожньою
    name = db.Column(db.String(80), unique=True, nullable=False)
    # Статус виконання (True - виконано, False - не виконано)
    status = db.Column(db.Boolean, default=False, nullable=False)
    # Пріоритет завдання
    priority = db.Column(db.String(20), nullable=False)

    # Метод __repr__ допомагає при налагодженні
    def __repr__(self):
        return f'<Task {self.name}>'

# ============================================================================
# Створюємо базу даних та таблицю
# Цей блок виконується лише один раз, при першому запуску додатку
# ============================================================================
with app.app_context():
    db.create_all()

# ============================================================================
# МАРШРУТИ ДОДАТКУ (ROUTES)
# ============================================================================

# Головна сторінка
# Відображає список усіх завдань
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

# API для додавання завдання (метод POST)
@app.route('/api/add', methods=['POST'])
def api_add_task():
    # Отримуємо дані з JSON-запиту
    data = request.get_json()
    task_name = data.get('task_name')
    task_priority = data.get('priority')

    # Перевіряємо, чи завдання з такою назвою вже існує
    if Task.query.filter_by(name=task_name).first():
        return jsonify({'error': 'Завдання з такою назвою вже існує'}), 409

    # Створюємо нове завдання
    new_task = Task(name=task_name, priority=task_priority)
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'name': new_task.name, 'priority': new_task.priority}), 201

# API для видалення завдання (метод DELETE)
@app.route('/api/delete/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    # Знаходимо завдання за ID
    task = Task.query.get_or_404(task_id)
    # Видаляємо завдання з бази даних
    db.session.delete(task)
    db.session.commit()
    # Повертаємо повідомлення про успішне видалення
    return jsonify({'message': 'Завдання видалено'}), 200

# API для позначення завдання як виконаного (метод POST)
@app.route('/api/complete/<int:task_id>', methods=['POST'])
def api_complete_task(task_id):
    # Знаходимо завдання за ID
    task = Task.query.get_or_404(task_id)
    # Змінюємо статус на протилежний
    task.status = not task.status
    db.session.commit()
    return jsonify({'status': task.status}), 200

# API для редагування завдання (метод POST)
@app.route('/api/update/<int:task_id>', methods=['POST'])
def api_update_task(task_id):
    # Знаходимо завдання за ID
    task = Task.query.get_or_404(task_id)
    # Отримуємо нові дані з JSON
    data = request.get_json()
    new_name = data.get('new_name')

    # Перевіряємо, чи нова назва вже існує
    if Task.query.filter(Task.name == new_name, Task.id != task_id).first():
        return jsonify({'error': 'Завдання з такою назвою вже існує'}), 409

    # Оновлюємо назву завдання
    task.name = new_name
    db.session.commit()
    return jsonify({'name': task.name}), 200

# Запускаємо додаток
if __name__ == '__main__':
    app.run(debug=True)
    