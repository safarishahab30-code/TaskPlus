from typing import Dict, Any
import csv
import os
from typing import List, Dict, Any

class Task:
    """مدل داده‌ای برای یک وظیفه تکی"""

    def __init__(self, title: str, description: str = "", priority: str = "Low", completed: bool = False):
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed

    def mark_completed(self) -> None:
        """تغییر وضعیت به انجام‌شده"""
        self.completed = True

    def to_dict(self) -> Dict[str, Any]:
        """تبدیل تسک به دیکشنری جهت ذخیره در فایل CSV"""
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": str(self.completed)
        }

    def __str__(self) -> str:
        status = "✓" if self.completed else "✗"
        return f"[{status}] {self.title} (اولویت: {self.priority})"
class ToDoList:
    """مدیریت مجموعه تسک‌ها و اتصال به فایل CSV"""

    def __init__(self, filename: str = "tasks.csv"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_from_file()
    def load_from_file(self) -> None:
        """بارگذاری تسک‌ها از فایل CSV به حافظه رم"""
        if not os.path.exists(self.filename):
            return  # اگر فایل هنوز وجود نداشت، کاری انجام نده

        with open(self.filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # تبدیل مقدار 'True'/'False' متنی به نوع boolean
                completed_bool = row["completed"].lower() == "true"
                
                task = Task(
                    title=row["title"],
                    description=row["description"],
                    priority=row["priority"],
                    completed=completed_bool
                )
                self.tasks.append(task)
    def list_tasks(self) -> List[Task]:
        """بازگرداندن لیست تمام تسک‌های موجود در حافظه"""
        return self.tasks
    def complete_task(self, index: int) -> bool:
        """تغییر وضعیت تسک با ایندکس مشخص و به‌روزرسانی فایل"""
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            self.save_to_file()
            return True
        return False
    def delete_task(self, index: int) -> bool:
        """حذف تسک بر اساس شماره ایندکس و به‌روزرسانی فایل"""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_to_file()
            return True
        return False
