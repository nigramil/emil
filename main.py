import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = 'expenses.json'

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.data = []

        # Поля для ввода
        frame_input = tk.Frame(root)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Сумма:").grid(row=0, column=0, padx=5)
        self.entry_sum = tk.Entry(frame_input)
        self.entry_sum.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="Категория:").grid(row=0, column=2, padx=5)
        self.entry_category = tk.Entry(frame_input)
        self.entry_category.grid(row=0, column=3, padx=5)

        tk.Label(frame_input, text="Дата (YYYY-MM-DD):").grid(row=0, column=4, padx=5)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.grid(row=0, column=5, padx=5)

        btn_add = tk.Button(root, text="Добавить расход", command=self.add_expense)
        btn_add.pack(pady=5)

        # Таблица расходов
        columns = ('sum', 'category', 'date')
        self.tree = ttk.Treeview(root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Фильтры
        frame_filters = tk.Frame(root)
        frame_filters.pack(pady=10)

        tk.Label(frame_filters, text="Фильтр по категории:").grid(row=0, column=0, padx=5)
        self.filter_category = tk.Entry(frame_filters)
        self.filter_category.grid(row=0, column=1, padx=5)

        tk.Label(frame_filters, text="Фильтр по дате:").grid(row=0, column=2, padx=5)
        self.filter_date = tk.Entry(frame_filters)
        self.filter_date.grid(row=0, column=3, padx=5)

        btn_filter = tk.Button(frame_filters, text="Фильтровать", command=self.apply_filter)
        btn_filter.grid(row=0, column=4, padx=5)

        btn_show_all = tk.Button(frame_filters, text="Показать все", command=self.load_data)
        btn_show_all.grid(row=0, column=5, padx=5)

        # Подсчет суммы
        btn_sum = tk.Button(root, text="Подсчитать сумму за текущий фильтр", command=self.calculate_total)
        btn_sum.pack(pady=5)

        # Загрузка данных
        self.load_data()

    def load_data(self):
        self.data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = []
        self.refresh_table()

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump(self.data, f, indent=4)

    def refresh_table(self, filtered_data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        data_to_show = filtered_data if filtered_data is not None else self.data
        for item in data_to_show:
            self.tree.insert('', tk.END, values=(item['sum'], item['category'], item['date']))

    def add_expense(self):
        sum_str = self.entry_sum.get()
        category = self.entry_category.get()
        date_str = self.entry_date.get()

        # Проверка суммы
        try:
            sum_value = float(sum_str)
            if sum_value <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите положительное число для суммы.")
            return

        # Проверка даты
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД.")
            return

        # Добавление записи
        expense = {
            'sum': sum_value,
            'category': category,
            'date': date_str
        }
        self.data.append(expense)
        self.save_data()
        self.load_data()

        # Очистка полей
        self.entry_sum.delete(0, tk.END)
        self.entry_category.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)

    def apply_filter(self):
        category_filter = self.filter_category.get().strip().lower()
        date_filter = self.filter_date.get().strip()

        filtered = self.data
        if category_filter:
            filtered = [item for item in filtered if item['category'].lower() == category_filter]
        if date_filter:
            filtered = [item for item in filtered if item['date'] == date_filter]

        self.refresh_table(filtered)

    def calculate_total(self):
        total = 0
        for item in self.tree.get_children():
            val = self.tree.item(item)['values'][0]
            total += float(val)
        messagebox.showinfo("Итоговая сумма", f"Общая сумма: {total:.2f}")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
