// script.js
// Цей файл містить логіку взаємодії з користувачем та асинхронні запити до сервера (API).

// Обробник подій для форми додавання завдання
document.getElementById('add-task-form').addEventListener('submit', async (e) => {
    // Відміняємо стандартну поведінку форми, щоб сторінка не перезавантажувалася
    e.preventDefault();

    // Отримуємо значення з полів введення
    const taskNameInput = document.getElementById('task-name');
    const taskPrioritySelect = document.getElementById('task-priority');

    const taskName = taskNameInput.value;
    const priority = taskPrioritySelect.value;

    try {
        // Відправляємо POST-запит до API для додавання завдання
        const response = await fetch('/api/add', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ task_name: taskName, priority: priority })
        });

        // Перевіряємо, чи успішним був запит
        if (response.ok) {
            // Отримуємо дані нового завдання у форматі JSON
            const newTask = await response.json();
            const taskList = document.getElementById('task-list');

            // Створюємо новий елемент списку (<li>)
            const li = document.createElement('li');
            li.id = `task-${newTask.id}`; // Додаємо унікальний ID
            li.innerHTML = `
                <span>${newTask.name}</span>
                <small class="priority-${newTask.priority.toLowerCase()}">(${newTask.priority})</small>
                <div class="actions">
                    <button type="button" class="complete-btn" data-task-id="${newTask.id}"><i class="fa-solid fa-check"></i></button>
                    <button type="button" class="edit-btn" data-task-id="${newTask.id}"><i class="fa-solid fa-pencil"></i></button>
                    <button type="button" class="delete-btn" data-task-id="${newTask.id}"><i class="fa-solid fa-trash"></i></button>
                </div>
            `;
            // Додаємо новий елемент у список
            taskList.appendChild(li);

            // Очищуємо поле вводу
            taskNameInput.value = '';
        } else {
            // Якщо запит був неуспішним, показуємо повідомлення про помилку
            const errorData = await response.json();
            alert(`Помилка: ${errorData.error}`);
        }
    } catch (error) {
        console.error('Помилка:', error);
        alert('Сталася помилка. Спробуйте ще раз.');
    }
});

// Використовуємо делегування подій для обробки кліків на кнопках
// Це дозволяє обробляти кліки на елементах, які ще не існують на сторінці
document.getElementById('task-list').addEventListener('click', async (e) => {
    // Перевіряємо, чи був клік на кнопці видалення
    if (e.target.closest('.delete-btn')) {
        const taskId = e.target.closest('.delete-btn').dataset.taskId;
        try {
            // Відправляємо DELETE-запит до API
            const response = await fetch(`/api/delete/${taskId}`, { method: 'DELETE' });
            if (response.ok) {
                // Видаляємо елемент зі сторінки, якщо запит успішний
                document.getElementById(`task-${taskId}`).remove();
            } else {
                const errorData = await response.json();
                alert(`Помилка: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Помилка:', error);
            alert('Сталася помилка. Спробуйте ще раз.');
        }
    }

    // Перевіряємо, чи був клік на кнопці "Виконано"
    if (e.target.closest('.complete-btn')) {
        const taskId = e.target.closest('.complete-btn').dataset.taskId;
        try {
            // Відправляємо POST-запит до API
            const response = await fetch(`/api/complete/${taskId}`, { method: 'POST' });
            if (response.ok) {
                // Змінюємо клас елемента, щоб застосувати стилі виконаного завдання
                const taskItem = document.getElementById(`task-${taskId}`);
                taskItem.classList.toggle('completed');
            } else {
                const errorData = await response.json();
                alert(`Помилка: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Помилка:', error);
            alert('Сталася помилка. Спробуйте ще раз.');
        }
    }

    // Перевіряємо, чи був клік на кнопці редагування
    if (e.target.closest('.edit-btn')) {
        const taskId = e.target.closest('.edit-btn').dataset.taskId;
        const taskItem = document.getElementById(`task-${taskId}`);
        const currentNameSpan = taskItem.querySelector('span');
        const currentName = currentNameSpan.textContent;

        // Викликаємо вікно-підказку для введення нової назви
        const newName = prompt('Введіть нову назву для завдання:', currentName);
        if (newName && newName !== currentName) {
            try {
                // Відправляємо POST-запит для оновлення назви
                const response = await fetch(`/api/update/${taskId}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ new_name: newName })
                });
                if (response.ok) {
                    const data = await response.json();
                    // Оновлюємо назву на сторінці
                    currentNameSpan.textContent = data.name;
                } else {
                    const errorData = await response.json();
                    alert(`Помилка: ${errorData.error}`);
                }
            } catch (error) {
                console.error('Помилка:', error);
                alert('Сталася помилка. Спробуйте ще раз.');
            }
        }
    }
});
