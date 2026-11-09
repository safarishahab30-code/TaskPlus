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
    print(farsi("5. فیلتر و جستجوی تسک‌ها"))
    print(farsi("6. خروج"))

def show_tasks(task_list: list) -> None:
    """نمایش لیست تسک‌ها به همراه شماره و وضعیت"""
    if not task_list:
        print(farsi("\nهیچ تسکی برای نمایش وجود ندارد!"))
        return
    
    print(farsi("\n--- لیست تسک‌ها ---"))
    for idx, task in enumerate(task_list):
        status_text = "تکمیل شده" if task.completed else "در انتظار"
        date_str = f" | موعد: {task.due_date}" if getattr(task, 'due_date', None) else ""
        line = f"{idx}. [{status_text}] {task.title} - اولویت: {task.priority}{date_str}"
        print(farsi(line))
        if task.description:
            print(farsi(f"   توضیحات: {task.description}"))

def handle_add_task(todo: ToDoList) -> None:
    """دریافت اطلاعات تسک جدید از کاربر و افزودن آن"""
    print(farsi("\n--- افزودن تسک جدید ---"))
    title = input(farsi("عنوان تسک: ")).strip()
    if not title:
        print(farsi("خطا: عنوان تسک نمی‌تواند خالی باشد!"))
        return
    
    description = input(farsi("توضیحات (اختیاری): ")).strip()
    priority = input(farsi("اولویت (کم، متوسط، زیاد): ")).strip() or "متوسط"
    due_date = input(farsi("موعد انجام (مثلاً 1403-08-20 یا خالی): ")).strip()
    
    todo.add_task(title=title, description=description, priority=priority, due_date=due_date)
    print(farsi("تسک با موفقیت افزوده و ذخیره شد."))

def handle_complete_task(todo: ToDoList) -> None:
    """دریافت شماره تسک برای تغییر وضعیت به انجام‌شده"""
    show_tasks(todo.list_tasks())
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
    show_tasks(todo.list_tasks())
    if not todo.list_tasks():
        return
    try:
        index = int(input(farsi("\nشماره تسکی که می‌خواهید حذف کنید را وارد کنید: ")))
        if todo.delete_task(index):
            print(farsi("تسک با موفقیت حذف شد."))
        else:
            print(farsi("خطا: شماره تسک نامعتبر است!"))
    except ValueError:
        print(farsi("خطا: لطفاً فقط عدد وارد کنید!"))

def main():
    """حلقه اصلی اجرای برنامه CLI"""
    todo = ToDoList()  # بارگذاری تسک‌ها از فایل هنگام شروع

    while True:
        print_menu()
        choice = input(farsi(" : لطفاً یک گزینه انتخاب کنید (1 تا 6) ")).strip()
    
        if choice == "1":
            show_tasks(todo.list_tasks())
        elif choice == "2":
            handle_add_task(todo)
        elif choice == "3":
            handle_complete_task(todo)
        elif choice == "4":
            handle_delete_task(todo)
        elif choice == "5":
            handle_filter_tasks(todo)
        elif choice == "6":
            print(farsi("خروج از برنامه."))
            break
        else:
            print(farsi("گزینه نامعتبر است! لطفاً عددی بین ۱ تا ۶ وارد کنید."))


if __name__ == "__main__":
    main()
