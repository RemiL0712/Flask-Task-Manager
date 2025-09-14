// script.js
// Цей файл містить логіку взаємодії з користувачем та асинхронні запити до сервера (API).

// Обробник подій для форми додавання завдання
document.getElementById('add-task-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const taskNameInput = document.getElementById('task-name');
    const taskPrioritySelect = document.getElementById('task-priority');

    const taskName = taskNameInput.value;
    const priority = taskPrioritySelect.value;

    let priorityToSend = '';

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

            taskNameInput.value = '';
        } else {
            const errorData = await response.json();
            alert(`Помилка: ${errorData.error}`);
        }
    } catch (error) {
        console.error('Помилка:', error);
        alert('Сталася помилка. Спробуйте ще раз.');
    }
});

// Обробник подій для кнопок "виконано", "редагувати" та "видалити"
document.getElementById('task-list').addEventListener('click', async (e) => {
    // Перевіряємо, чи був клік на кнопці "виконано"
    if (e.target.closest('.complete-btn')) {
        const taskId = e.target.closest('.complete-btn').dataset.taskId;
        const taskItem = document.getElementById(`task-${taskId}`);

        try {
            // Використовуємо PATCH для часткового оновлення статусу
            const response = await fetch(`/api/complete/${taskId}`, { method: 'PATCH' });
            if (response.ok) {
                taskItem.classList.toggle('completed');
            } else {
                alert('Помилка при зміні статусу.');
            }
        } catch (error) {
            console.error('Помилка:', error);
            alert('Сталася помилка. Спробуйте ще раз.');
        }
    }

    // Перевіряємо, чи був клік на кнопці "видалити"
    if (e.target.closest('.delete-btn')) {
        const taskId = e.target.closest('.delete-btn').dataset.taskId;
        const taskItem = document.getElementById(`task-${taskId}`);

        if (confirm('Ви впевнені, що хочете видалити це завдання?')) {
            try {
                // Використовуємо DELETE для видалення завдання
                const response = await fetch(`/api/delete/${taskId}`, { method: 'DELETE' });
                if (response.ok) {
                    taskItem.remove();
                } else {
                    alert('Помилка при видаленні.');
                }
            } catch (error) {
                console.error('Помилка:', error);
                alert('Сталася помилка. Спробуйте ще раз.');
            }
        }
    }

    // Перевіряємо, чи був клік на кнопці "редагувати"
    if (e.target.closest('.edit-btn')) {
        const taskId = e.target.closest('.edit-btn').dataset.taskId;
        const taskItem = document.getElementById(`task-${taskId}`);
        const currentNameSpan = taskItem.querySelector('span');
        const currentName = currentNameSpan.textContent;

        const newName = prompt('Введіть нову назву для завдання:', currentName);
        if (newName && newName !== currentName) {
            try {
                // Використовуємо PUT для оновлення назви
                const response = await fetch(`/api/update/${taskId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ new_name: newName })
                });

                if (response.ok) {
                    const data = await response.json();
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
