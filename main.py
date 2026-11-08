from models import ToDoList, Task
import sys
import io
import arabic_reshaper
from bidi.algorithm import get_display

def farsi(text: str) -> str:
    """اصلاح حروف فارسی برای نمایش درست و متصل در ترمینال"""
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_menu() -> None:
    """نمایش گزینه‌های در دسترس کاربر"""
    print("\n--- TaskPulse CLI ---")
    print(farsi("1. مشاهده همه تسک‌ها"))
    print(farsi("2. افزودن تسک جدید"))
    print(farsi("3. علامت‌زدن تسک به عنوان انجام‌شده"))
    print(farsi("4. حذف تسک"))
    print(farsi("5. خروج"))

def show_tasks(todo: ToDoList) -> None:
    """نمایش لیست تسک‌ها به همراه شماره و وضعیت"""
    tasks = todo.list_tasks()
    if not tasks:
        print("\nهیچ تسکی ثبت نشده است!")
        return
    
    print("\n--- لیست تسک‌ها ---")
    for idx, task in enumerate(tasks):
        status_text = "تکمیل شده" if task.completed else "در انتظار"
        print(f"{idx}. [{status_text}] {task.title} - اولویت: {task.priority}")
        if task.description:
            print(f"   توضیحات: {task.description}")

def handle_add_task(todo: ToDoList) -> None:
    """دریافت اطلاعات تسک جدید از کاربر و افزودن آن"""
    print(farsi("\n--- افزودن تسک جدید ---"))
    title = input(farsi("  :  عنوان تسک ")).strip()
    if not title:
        print("خطا: عنوان تسک نمی‌تواند خالی باشد!")
        return
    
    description = input("توضیحات (اختیاری): ").strip()
    priority = input("اولویت (کم، متوسط، زیاد): ").strip() or "متوسط"
    
    todo.add_task(title, description, priority)
    print("تسک با موفقیت افزوده و ذخیره شد.")

def handle_complete_task(todo: ToDoList) -> None:
    """دریافت شماره تسک برای تغییر وضعیت به انجام‌شده"""
    show_tasks(todo)
    if not todo.list_tasks():
        return
    
    try:
        index = int(input("\nشماره تسکی که انجام شده را وارد کنید: "))
        if todo.complete_task(index):
            print("وضعیت تسک به 'انجام‌شده' تغییر یافت.")
        else:
            print("خطا: شماره تسک نامعتبر است!")
    except ValueError:
        print("خطا: لطفاً فقط عدد وارد کنید!")

def handle_delete_task(todo: ToDoList) -> None:
    """دریافت شماره تسک برای حذف"""
    show_tasks(todo)
    if not todo.list_tasks():
        return
    
    try:
        index = int(input("\nشماره تسکی که می‌خواهید حذف کنید را وارد کنید: "))
        if todo.delete_task(index):
            print("تسک با موفقیت حذف شد.")
        else:
            print("خطا: شماره تسک نامعتبر است!")
    except ValueError:
        print("خطا: لطفاً فقط عدد وارد کنید!")

def main():
    """حلقه اصلی اجرای برنامه CLI"""
    todo = ToDoList()  # بارگذاری تسک‌ها از فایل هنگام شروع

    while True:
        print_menu()
        choice = input((farsi(" : لطفاً یک گزینه انتخاب کنید (1و5) "))).strip()
    
        if choice == "1":
            show_tasks(todo)
        elif choice == "2":
            handle_add_task(todo)
        elif choice == "3":
            handle_complete_task(todo)
        elif choice == "4":
            handle_delete_task(todo)
        elif choice == "5":
            print(farsi("خروج از برنامه."))
            break
        else:
            print(farsi("گزینه نامعتبر است! لطفاً عددی بین ۱ تا ۵ وارد کنید."))

if __name__ == "__main__":
    main()
