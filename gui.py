from datetime import datetime
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import arabic_reshaper
from bidi.algorithm import get_display
import jdatetime
from models import ToDoList

def fix_farsi(text: str) -> str:
    return text

class TaskPulseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(fix_farsi("TaskPulse GUI - مدیریت تسک‌ها"))
        self.root.geometry("550x730")

        self.todo = ToDoList()

        # ۱. بخش فیلتر و جستجوی تسک‌ها
        self.frame_search = tk.LabelFrame(self.root, text=fix_farsi("جستجو و فیلتر"), font=("Arial", 9))
        self.frame_search.pack(fill="x", padx=20, pady=5, ipadx=5, ipady=5)

        tk.Label(self.frame_search, text=fix_farsi("جستجو:")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_search = tk.Entry(self.frame_search, width=25)
        self.entry_search.grid(row=0, column=1, padx=5, pady=2)
        self.entry_search.bind("<KeyRelease>", self.filter_tasks)

        tk.Label(self.frame_search, text=fix_farsi("دسته‌بندی:")).grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.combo_filter_cat = ttk.Combobox(
            self.frame_search,
            values=["همه", "کاری", "شخصی", "درسی", "متفرقه"],
            width=12,
            state="readonly",
        )
        self.combo_filter_cat.grid(row=0, column=3, padx=5, pady=2)
        self.combo_filter_cat.set("همه")
        self.combo_filter_cat.bind("<<ComboboxSelected>>", self.filter_tasks)

        # ۲. بخش نمایش لیست تسک‌ها
        self.lbl_list = tk.Label(self.root, text=fix_farsi("لیست تسک‌ها"), font=("Arial", 11, "bold"))
        self.lbl_list.pack(pady=5)

        self.listbox = tk.Listbox(self.root, width=70, height=10, font=("Courier New", 10))
        self.listbox.pack(pady=5)

        # ۳. فرم افزودن تسک جدید (با دسته‌بندی پویا و قابل تایپ)
        self.frame_add = tk.LabelFrame(self.root, text=fix_farsi("افزودن تسک جدید"), font=("Arial", 10))
        self.frame_add.pack(fill="both", padx=20, pady=5, ipadx=5, ipady=5)

        tk.Label(self.frame_add, text=fix_farsi("عنوان تسک:")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_title = tk.Entry(self.frame_add, width=35)
        self.entry_title.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.frame_add, text=fix_farsi("توضیحات:")).grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_desc = tk.Entry(self.frame_add, width=35)
        self.entry_desc.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.frame_add, text=fix_farsi("دسته‌بندی:")).grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.combo_add_cat = ttk.Combobox(
            self.frame_add,
            values=["کاری", "شخصی", "درسی", "متفرقه"],
            width=33,
        )
        self.combo_add_cat.grid(row=2, column=1, padx=5, pady=2)
        self.combo_add_cat.set("کاری")

        tk.Label(self.frame_add, text=fix_farsi("اولویت (کم، متوسط، زیاد):")).grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.entry_priority = tk.Entry(self.frame_add, width=35)
        self.entry_priority.insert(0, "متوسط")
        self.entry_priority.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(self.frame_add, text=fix_farsi("موعد انجام (1405/08/18):")).grid(row=4, column=0, sticky="w", padx=5, pady=2)
        self.entry_due = tk.Entry(self.frame_add, width=35)
        today_jalali = jdatetime.date.today().strftime("%Y/%m/%d")
        self.entry_due.insert(0, today_jalali)
        self.entry_due.grid(row=4, column=1, padx=5, pady=2)

        self.btn_add = tk.Button(
            self.frame_add,
            text=fix_farsi("ثبت تسک"),
            width=15,
            bg="#4CAF50",
            fg="white",
            command=self.add_task,
        )
        self.btn_add.grid(row=5, column=0, columnspan=2, pady=8)

        # ۴. دکمه‌های عملیاتی روی تسک انتخاب‌شده و گزارش‌ها
        self.frame_actions = tk.Frame(self.root)
        self.frame_actions.pack(pady=5)

        self.btn_complete = tk.Button(
            self.frame_actions,
            text=fix_farsi("انجام‌شدن"),
            width=13,
            bg="#2196F3",
            fg="white",
            command=self.complete_task,
        )
        self.btn_complete.grid(row=0, column=0, padx=2, pady=2)

        self.btn_delete = tk.Button(
            self.frame_actions,
            text=fix_farsi("حذف تسک"),
            width=13,
            bg="#f44336",
            fg="white",
            command=self.delete_task,
        )
        self.btn_delete.grid(row=0, column=1, padx=2, pady=2)

        self.btn_refresh = tk.Button(
            self.frame_actions,
            text=fix_farsi("بارگذاری مجدد"),
            width=13,
            command=self.refresh_tasks,
        )
        self.btn_refresh.grid(row=0, column=2, padx=2, pady=2)

        self.btn_export = tk.Button(
            self.frame_actions,
            text=fix_farsi("خروجی CSV"),
            width=13,
            bg="#9C27B0",
            fg="white",
            command=self.export_csv,
        )
        self.btn_export.grid(row=0, column=3, padx=2, pady=2)

        # دکمه‌های Backup & Restore
        self.frame_backup = tk.Frame(self.root)
        self.frame_backup.pack(pady=5)

        self.btn_backup = tk.Button(
            self.frame_backup,
            text=fix_farsi("پشتیبان‌گیری (Backup)"),
            width=25,
            bg="#607D8B",
            fg="white",
            command=self.backup_database,
        )
        self.btn_backup.grid(row=0, column=0, padx=5, pady=2)

        self.btn_restore = tk.Button(
            self.frame_backup,
            text=fix_farsi("بازیابی (Restore)"),
            width=25,
            bg="#FF9800",
            fg="white",
            command=self.restore_database,
        )
        self.btn_restore.grid(row=0, column=1, padx=5, pady=2)

        # بارگذاری اولیه داده‌ها
        self.refresh_tasks()

    def refresh_tasks(self):
        """بارگذاری و نمایش مجدد تسک‌ها در لیست‌باکس"""
        self.listbox.delete(0, tk.END)
        tasks = self.todo.list_tasks()

        if not tasks:
            self.listbox.insert(tk.END, fix_farsi("هیچ تسکی ثبت نشده است."))
            return

        for idx, task in enumerate(tasks):
            status = "✓" if task.completed else "✗"
            cat = getattr(task, "category", "متفرقه")
            due_str = f" | موعد: {task.due_date}" if task.due_date else ""
            line = f"{idx}. [{status}] [{cat}] {task.title} - اولویت: {task.priority}{due_str}"
            self.listbox.insert(tk.END, line)

    def filter_tasks(self, event=None):
        """فیلتر کردن تسک‌ها بر اساس جستجوی متن و دسته‌بندی"""
        query = self.entry_search.get().strip().lower()
        selected_cat = self.combo_filter_cat.get()

        self.listbox.delete(0, tk.END)
        tasks = self.todo.list_tasks()

        filtered = []
        for task in tasks:
            cat = getattr(task, "category", "متفرقه")
            match_query = query in task.title.lower() or query in task.description.lower()
            match_cat = (selected_cat == "همه") or (cat == selected_cat)

            if match_query and match_cat:
                filtered.append(task)

        if not filtered:
            self.listbox.insert(tk.END, fix_farsi("هیچ تسکی با این مشخصات یافت نشد."))
            return

        for idx, task in enumerate(filtered):
            status = "✓" if task.completed else "✗"
            cat = getattr(task, "category", "متفرقه")
            due_str = f" | موعد: {task.due_date}" if task.due_date else ""
            line = f"{idx}. [{status}] [{cat}] {task.title} - اولویت: {task.priority}{due_str}"
            self.listbox.insert(tk.END, line)

    def add_task(self):
        """دریافت اطلاعات و افزودن تسک جدید"""
        title = self.entry_title.get().strip()
        description = self.entry_desc.get().strip()
        category = self.combo_add_cat.get().strip() or "متفرقه"
        priority = self.entry_priority.get().strip() or "متوسط"
        due_date = self.entry_due.get().strip()

        if not title:
            messagebox.showerror(fix_farsi("خطا"), fix_farsi("عنوان تسک نمی‌تواند خالی باشد!"))
            return

        try:
            self.todo.add_task(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
                category=category,
            )
        except TypeError:
            self.todo.add_task(
                title=title,
                description=description,
                priority=priority,
                due_date=due_date,
            )

        # به‌روزرسانی لیست دسته‌بندی‌های فیلتر
        current_values = list(self.combo_filter_cat["values"])
        if category not in current_values:
            current_values.append(category)
            self.combo_filter_cat["values"] = current_values
            self.combo_add_cat["values"] = [v for v in current_values if v != "همه"]

        # پاک‌سازی فیلدها
        self.entry_title.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_priority.delete(0, tk.END)
        self.entry_priority.insert(0, "متوسط")
        self.entry_due.delete(0, tk.END)
        self.entry_due.insert(0, jdatetime.date.today().strftime("%Y/%m/%d"))

        self.refresh_tasks()
        messagebox.showinfo(fix_farsi("موفقیت"), fix_farsi("تسک با موفقیت اضافه شد."))

    def complete_task(self):
        """تغییر وضعیت تسک انتخاب‌شده به انجام‌شده"""
        try:
            selected_indices = self.listbox.curselection()
            if not selected_indices:
                messagebox.showwarning(fix_farsi("هشدار"), fix_farsi("لطفاً یک تسک را از لیست انتخاب کنید!"))
                return

            index = selected_indices[0]
            if self.todo.complete_task(index):
                self.refresh_tasks()
                messagebox.showinfo(fix_farsi("موفقیت"), fix_farsi("وضعیت تسک به انجام‌شده تغییر یافت."))
            else:
                messagebox.showerror(fix_farsi("خطا"), fix_farsi("شماره تسک نامعتبر است!"))
        except Exception as e:
            messagebox.showerror(fix_farsi("خطا"), fix_farsi(str(e)))

    def delete_task(self):
        """حذف تسک انتخاب‌شده"""
        try:
            selected_indices = self.listbox.curselection()
            if not selected_indices:
                messagebox.showwarning(fix_farsi("هشدار"), fix_farsi("لطفاً یک تسک را از لیست انتخاب کنید!"))
                return

            index = selected_indices[0]
            if self.todo.delete_task(index):
                self.refresh_tasks()
                messagebox.showinfo(fix_farsi("موفقیت"), fix_farsi("تسک با موفقیت حذف شد."))
            else:
                messagebox.showerror(fix_farsi("خطا"), fix_farsi("شماره تسک نامعتبر است!"))
        except Exception as e:
            messagebox.showerror(fix_farsi("خطا"), fix_farsi(str(e)))

    def export_csv(self):
        """خروجی گزارش تسک‌ها به فرمت CSV با انکودینگ استاندارد فارسی"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title=fix_farsi("ذخیره گزارش تسک‌ها")
        )
        if file_path:
            try:
                tasks = self.todo.list_tasks()
                with open(file_path, mode="w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)
                    writer.writerow(["عنوان", "توضیحات", "دسته‌بندی", "اولویت", "موعد انجام", "وضعیت"])
                    for task in tasks:
                        status = "انجام‌شده" if task.completed else "در جریان"
                        cat = getattr(task, "category", "متفرقه")
                        desc = getattr(task, "description", "")
                        due = getattr(task, "due_date", "")
                        writer.writerow([task.title, desc, cat, task.priority, due, status])
                messagebox.showinfo(fix_farsi("موفقیت"), fix_farsi("گزارش CSV با موفقیت ذخیره شد."))
            except Exception as e:
                messagebox.showerror(fix_farsi("خطا"), fix_farsi(f"خطا در ذخیره فایل: {e}"))

    def backup_database(self):
        """تهیه نسخه پشتیبان از فایل داده‌ها"""
        try:
            backup_name = f"tasks_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy("tasks.db", backup_name)
            messagebox.showinfo(fix_farsi("موفقیت"), fix_farsi(f"پشتیبان با موفقیت در فایل {backup_name} ذخیره شد."))
        except Exception as e:
            try:
                backup_name = f"tasks_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                shutil.copy("tasks.csv", backup_name)
                messagebox.showinfo(fix_farsi("موفقیت"), fix_farsi(f"پشتیبان با موفقیت در فایل {backup_name} ذخیره شد."))
            except Exception as ex:
                messagebox.showerror(fix_farsi("خطا"), fix_farsi(f"خطا در پشتیبان‌گیری: {ex}"))

    def restore_database(self):
        """بازیابی پایگاه داده از روی فایل پشتیبان"""
        file_path = filedialog.askopenfilename(
            title=fix_farsi("انتخاب فایل پشتیبان"),
            filetypes=[("Database/CSV Files", "*.db;*.csv"), ("All Files", "*.*")],
        )
        if file_path:
            try:
                target = "tasks.db" if file_path.endswith(".db") else "tasks.csv"
                shutil.copy(file_path, target)
                messagebox.showinfo(fix_farsi("موفقیت"), fix_farsi("دیتابیس با موفقیت بازیابی شد. لیست به‌روزرسانی شد."))
                self.refresh_tasks()
            except Exception as e:
                messagebox.showerror(fix_farsi("خطا"), fix_farsi(f"خطا در بازیابی: {e}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskPulseGUI(root)
    root.mainloop()
