import tkinter as tk
from tkinter import ttk, messagebox


class Task:
    def __init__(self, task_id, description, due_date):
        self.task_id = task_id
        self.description = description
        self.due_date = due_date
        self.completed = False

    def mark_as_completed(self):
        self.completed = True

    def update_description(self, new_description):
        self.description = new_description

    def update_due_date(self, new_due_date):
        self.due_date = new_due_date


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, description, due_date):
        new_task = Task(self.next_id, description, due_date)
        self.tasks.append(new_task)
        self.next_id += 1

    def delete_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                return True
        return False

    def edit_task(self, task_id, new_description, new_due_date):
        for task in self.tasks:
            if task.task_id == task_id:
                task.update_description(new_description)
                task.update_due_date(new_due_date)
                return True
        return False

    def mark_task_completed(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                task.mark_as_completed()
                return True
        return False


class TaskManagerApp:
    def __init__(self, master):
        self.master = master
        self.manager = TaskManager()

        master.title("Менеджер задач")
        master.geometry("800x400")

        # Создаем Treeview для отображения задач
        self.tree = ttk.Treeview(master, columns=('ID', 'Описание', 'Срок', 'Статус'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Описание', text='Описание')
        self.tree.heading('Срок', text='Срок')
        self.tree.heading('Статус', text='Статус')
        self.tree.column('ID', width=50)
        self.tree.column('Описание', width=300)
        self.tree.column('Срок', width=100)
        self.tree.column('Статус', width=100)
        self.tree.pack(pady=20)

        # Панель кнопок
        button_frame = tk.Frame(master)
        button_frame.pack(pady=10)

        self.add_btn = tk.Button(button_frame, text="Добавить", command=self.add_task)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.edit_btn = tk.Button(button_frame, text="Редактировать", command=self.edit_task)
        self.edit_btn.pack(side=tk.LEFT, padx=5)

        self.delete_btn = tk.Button(button_frame, text="Удалить", command=self.delete_task)
        self.delete_btn.pack(side=tk.LEFT, padx=5)

        self.complete_btn = tk.Button(button_frame, text="Выполнено", command=self.mark_completed)
        self.complete_btn.pack(side=tk.LEFT, padx=5)

        self.refresh_tasks()

    def refresh_tasks(self):
        # Очищаем текущий список
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Добавляем актуальные задачи
        for task in self.manager.tasks:
            status = "✅ Выполнено" if task.completed else "🕒 В работе"
            self.tree.insert('', 'end',
                             values=(task.task_id, task.description, task.due_date, status),
                             tags=('completed' if task.completed else 'active'))

        # Настраиваем цвета для статусов
        self.tree.tag_configure('completed', foreground='gray')
        self.tree.tag_configure('active', foreground='green')

    def add_task(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Новая задача")

        tk.Label(dialog, text="Описание:").grid(row=0, column=0, padx=5, pady=5)
        description_entry = tk.Entry(dialog, width=30)
        description_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Срок выполнения:").grid(row=1, column=0, padx=5, pady=5)
        due_date_entry = tk.Entry(dialog, width=30)
        due_date_entry.grid(row=1, column=1, padx=5, pady=5)

        def save():
            desc = description_entry.get()
            date = due_date_entry.get()
            if desc and date:
                self.manager.add_task(desc, date)
                self.refresh_tasks()
                dialog.destroy()
            else:
                messagebox.showwarning("Ошибка", "Заполните все поля")

        tk.Button(dialog, text="Сохранить", command=save).grid(row=2, columnspan=2, pady=10)

    def edit_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите задачу для редактирования")
            return

        # Исправленная строка с закрывающей скобкой
        task_id = int(self.tree.item(selected[0])['values'][0])

        for task in self.manager.tasks:
            if task.task_id == task_id:
                dialog = tk.Toplevel(self.master)
                dialog.title("Редактирование задачи")

                tk.Label(dialog, text="Описание:").grid(row=0, column=0, padx=5, pady=5)
                description_entry = tk.Entry(dialog, width=30)
                description_entry.insert(0, task.description)
                description_entry.grid(row=0, column=1, padx=5, pady=5)

                tk.Label(dialog, text="Срок выполнения:").grid(row=1, column=0, padx=5, pady=5)
                due_date_entry = tk.Entry(dialog, width=30)
                due_date_entry.insert(0, task.due_date)
                due_date_entry.grid(row=1, column=1, padx=5, pady=5)

                def save():
                    new_desc = description_entry.get()
                    new_date = due_date_entry.get()
                    if new_desc and new_date:
                        self.manager.edit_task(task_id, new_desc, new_date)
                        self.refresh_tasks()
                        dialog.destroy()
                    else:
                        messagebox.showwarning("Ошибка", "Заполните все поля")

                tk.Button(dialog, text="Сохранить", command=save).grid(row=2, columnspan=2, pady=10)
                break

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите задачу для удаления")
            return

        task_id = int(self.tree.item(selected[0])['values'][0])
        if self.manager.delete_task(task_id):
            self.refresh_tasks()
        else:
            messagebox.showerror("Ошибка", "Задача не найдена")

    def mark_completed(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите задачу")
            return

        task_id = int(self.tree.item(selected[0])['values'][0])
        if self.manager.mark_task_completed(task_id):
            self.refresh_tasks()
        else:
            messagebox.showerror("Ошибка", "Задача не найдена")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()