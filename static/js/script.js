// script.js
// Цей файл відповідає за динамічну взаємодію з користувачем на фронтенді,
// включаючи обробку подій та асинхронні запити до API-сервісу на бекенді.

// Основний обробник подій для форми додавання нового завдання
document.getElementById('add-task-form').addEventListener('submit', async (e) => {
    // Відміняємо стандартну поведінку форми, щоб запобігти перезавантаженню сторінки
    e.preventDefault();

    const taskNameInput = document.getElementById('task-name');
    const taskPrioritySelect = document.getElementById('task-priority');

    const taskName = taskNameInput.value.trim();
    const priority = taskPrioritySelect.value;

    // Валідація: якщо назва порожня після видалення пробілів, зупиняємо виконання
    if (!taskName) {
        alert('Назва завдання не може бути порожньою.');
        return;
    }

    // Перетворення українських значень пріоритетів на англійські для бекенду
    let priorityToSend;
    if (priority === 'Високий') {
        priorityToSend = 'high';
    } else if (priority === 'Середній') {
        priorityToSend = 'medium';
    } else {
        priorityToSend = 'low';
    }

    try {
        const response = await fetch('/api/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task_name: taskName, priority: priorityToSend })
        });

        if (response.ok) {
            const newTask = await response.json();
            const taskList = document.getElementById('task-list');

            const li = document.createElement('li');
            li.id = `task-${newTask.id}`;
            li.className = `task-item`; // Додаємо універсальний клас для стилізації
            li.innerHTML = `
                <div class="task-name">
                    <span>${newTask.name}</span>
                </div>
                <div class="task-priority">
                    <small class="priority-${newTask.priority}">(${priority})</small>
                </div>
                <div class="actions">
                    <button type="button" class="complete-btn" data-task-id="${newTask.id}"><i class="fa-solid fa-check"></i></button>
                    <button type="button" class="edit-btn" data-task-id="${newTask.id}"><i class="fa-solid fa-pencil"></i></button>
                    <button type="button" class="delete-btn" data-task-id="${newTask.id}"><i class="fa-solid fa-trash"></i></button>
                </div>
            `;
            taskList.appendChild(li);

            // Очищаємо поле введення після успішного додавання
            taskNameInput.value = '';
        } else {
            const errorData = await response.json();
            alert(`Помилка: ${errorData.error}`);
        }
    } catch (error) {
        console.error('Помилка при додаванні завдання:', error);
        alert('Сталася помилка. Спробуйте ще раз.');
    }
});

// Делегування подій для кнопок "виконано", "редагувати" та "видалити"
document.getElementById('task-list').addEventListener('click', async (e) => {
    // Обробка кліку на кнопці "виконано"
    if (e.target.closest('.complete-btn')) {
        const taskId = e.target.closest('.complete-btn').dataset.taskId;
        const taskItem = document.getElementById(`task-${taskId}`);
        try {
            const response = await fetch(`/api/complete/${taskId}`, { method: 'PATCH' });
            if (response.ok) {
                taskItem.classList.toggle('completed');
            } else {
                alert('Помилка при зміні статусу.');
            }
        } catch (error) {
            console.error('Помилка при зміні статусу:', error);
            alert('Сталася помилка. Спробуйте ще раз.');
        }
    }

    // Обробка кліку на кнопці "видалити"
    if (e.target.closest('.delete-btn')) {
        const taskId = e.target.closest('.delete-btn').dataset.taskId;
        if (confirm('Ви впевнені, що хочете видалити це завдання?')) {
            try {
                const response = await fetch(`/api/delete/${taskId}`, { method: 'DELETE' });
                if (response.ok) {
                    document.getElementById(`task-${taskId}`).remove();
                } else {
                    alert('Помилка при видаленні.');
                }
            } catch (error) {
                console.error('Помилка при видаленні:', error);
                alert('Сталася помилка. Спробуйте ще раз.');
            }
        }
    }

    // Обробка кліку на кнопці "редагувати"
    if (e.target.closest('.edit-btn')) {
        const taskId = e.target.closest('.edit-btn').dataset.taskId;
        const taskItem = document.getElementById(`task-${taskId}`);
        const currentNameSpan = taskItem.querySelector('.task-name span');
        const currentName = currentNameSpan.textContent;

        const newName = prompt('Введіть нову назву для завдання:', currentName);
        if (newName && newName.trim() !== currentName) {
            try {
                const response = await fetch(`/api/update/${taskId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ new_name: newName.trim() })
                });

                if (response.ok) {
                    const data = await response.json();
                    currentNameSpan.textContent = data.name;
                } else {
                    const errorData = await response.json();
                    alert(`Помилка: ${errorData.error}`);
                }
            } catch (error) {
                console.error('Помилка при оновленні назви:', error);
                alert('Сталася помилка. Спробуйте ще раз.');
            }
        }
    }
});
