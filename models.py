from typing import Any, Dict, List
import csv
import os


class Task:
  """مدل داده‌ای برای یک وظیفه تکی"""

  def __init__(
      self,
      title,
      description="",
      priority="متوسط",
      due_date=None,
      completed=False,
      category="متفرقه",
  ):
    self.title = title
    self.description = description
    self.priority = priority
    self.due_date = due_date
    self.completed = completed
    self.category = category

  def mark_completed(self) -> None:
    """تغییر وضعیت به انجام‌شده"""
    self.completed = True

  def to_dict(self) -> Dict[str, Any]:
    """تبدیل تسک به دیکشنری جهت ذخیره در فایل CSV"""
    return {
        "title": self.title,
        "description": self.description,
        "due_date": self.due_date,
        "priority": self.priority,
        "completed": str(self.completed),
        "category": self.category,
    }

  def __str__(self) -> str:
    status = "✓" if self.completed else "✗"
    date_str = f" | موعد: {self.due_date}" if self.due_date else ""
    return f"[{status}] {self.title} (دسته‌بندی: {self.category} - اولویت: {self.priority}{date_str})"

class ToDoList:
  """مدیریت مجموعه تسک‌ها و اتصال به فایل CSV"""

  def __init__(self, filename: str = "tasks.csv"):
    self.filename = filename
    self.tasks: List[Task] = []
    self.load_from_file()

  def load_from_file(self) -> None:
    """بارگذاری تسک‌ها از فایل CSV به حافظه رم"""
    if not os.path.exists(self.filename):
      return

    with open(self.filename, mode="r", encoding="utf-8") as file:
      reader = csv.DictReader(file)
      for row in reader:
        completed_bool = row.get("completed", "False").lower() == "true"
        task = Task(
            title=row.get("title", ""),
            description=row.get("description", ""),
            priority=row.get("priority", "متوسط"),
            due_date=row.get("due_date", ""),
            completed=completed_bool,
            category=row.get("category", "متفرقه"),
        )
        self.tasks.append(task)

  def save_to_file(self) -> None:
    """ذخیره تمام تسک‌های رم درون فایل CSV"""
    fieldnames = [
        "title",
        "description",
        "priority",
        "due_date",
        "completed",
        "category",
    ]
    with open(self.filename, mode="w", encoding="utf-8", newline="") as file:
      writer = csv.DictWriter(file, fieldnames=fieldnames)
      writer.writeheader()
      for task in self.tasks:
        writer.writerow(task.to_dict())

  def add_task(
      self,
      title: str,
      description: str = "",
      priority: str = "متوسط",
      due_date: str = "",
      category: str = "متفرقه",
  ) -> None:
    """ایجاد تسک جدید، ذخیره در لیست و فایل"""
    new_task = Task(title, description, priority, due_date, False, category)
    self.tasks.append(new_task)
    self.save_to_file()

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
