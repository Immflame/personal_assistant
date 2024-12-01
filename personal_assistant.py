import csv
import os
from datetime import datetime
import re
from classes import *


def manage_notes():
    notes = load_data('notes.json')
    next_id = len(notes) + 1 if notes else 1
    while True:
        print("\nУправление заметками:")
        print("1. Создать новую заметку")
        print("2. Просмотреть список заметок")
        print("3. Просмотреть подробности заметки")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Импорт заметок из CSV")
        print("7. Экспорт заметок в CSV")
        print("8. Назад")
        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите заголовок заметки: ")
            content = input("Введите содержимое заметки: ")
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            note = Note(next_id, title, content, timestamp)
            notes.append(note.__dict__)
            next_id += 1
            print("Заметка успешно добавлена!")

        elif choice == '2':
            if notes:
                for note in notes:
                    print(f"ID: {note['id']}, Заголовок: {note['title']}, Дата: {note['timestamp']}")
            else:
                print("Список заметок пуст.")

        elif choice == '3':
            note_id = int(input("Введите ID заметки для просмотра: "))
            note = next((note for note in notes if note['id'] == note_id), None)
            if note:
                print(f"Заголовок: {note['title']}\nСодержимое: {note['content']}\nДата: {note['timestamp']}")
            else:
                print("Заметка не найдена.")

        elif choice == '4':
            note_id = int(input("Введите ID заметки для редактирования: "))
            note = next((note for note in notes if note['id'] == note_id), None)
            if note:
                note['title'] = input(f"Введите новый заголовок (текущий: {note['title']}): ") or note['title']
                note['content'] = input(f"Введите новое содержимое (текущий: {note['content']}): ") or note['content']
                note['timestamp'] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                print("Заметка успешно отредактирована!")
            else:
                print("Заметка не найдена.")

        elif choice == '5':
            note_id = int(input("Введите ID заметки для удаления: "))
            notes[:] = [note for note in notes if note['id'] != note_id]
            print("Заметка успешно удалена!")

        elif choice == '6':  # Импорт из CSV
            filename = input("Введите имя CSV-файла для импорта: ")
            try:
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            note = Note(next_id, row['title'], row['content'], row['timestamp'])
                            notes.append(note.__dict__)
                            next_id += 1
                        except KeyError as e:
                            print(f"Ошибка при импорте: Отсутствует поле {e} в CSV файле.")
                print("Заметки успешно импортированы из CSV-файла.")
            except FileNotFoundError:
                print(f"Ошибка: Файл {filename} не найден.")
            except Exception as e:
                print(f"Произошла ошибка при импорте CSV: {e}")

        elif choice == '7':  # Экспорт в CSV
            filename = input("Введите имя CSV-файла для экспорта: ")
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['id', 'title', 'content', 'timestamp']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(notes)
                print("Заметки успешно экспортированы в CSV-файл.")
            except Exception as e:
                print(f"Произошла ошибка при экспорте в CSV: {e}")

        elif choice == '8':
            break
        else:
            print("Неверный выбор.")

    save_data(notes, 'notes.json')


def manage_tasks():
    tasks = load_data('tasks.json')
    next_id = len(tasks) + 1 if tasks else 1
    while True:
        print("\nУправление задачами:")
        print("1. Добавить новую задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Экспорт задач в CSV")
        print("7. Импорт задач из CSV")
        print("8. Назад")
        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Введите название задачи: ")
            description = input("Введите описание задачи: ")
            priority = input("Выберите приоритет (Высокий/Средний/Низкий): ")
            while True:
                due_date_str = input("Введите срок выполнения (ДД-ММ-ГГГГ): ")
                if re.match(r"^\d{2}-\d{2}-\d{4}$", due_date_str):
                    due_date = due_date_str
                    break
                else:
                    print("Неверный формат даты. Используйте формат ДД-ММ-ГГГГ.")

            task = Task(next_id, title, description, priority=priority, due_date=due_date)
            tasks.append(task.__dict__)
            next_id += 1
            print("Задача успешно добавлена!")

        elif choice == '2':
            if tasks:
                for task in tasks:
                    status = "Выполнено" if task['done'] else "Не выполнено"
                    print(
                        f"ID: {task['id']}, Название: {task['title']}, Статус: {status}, Приоритет: {task['priority']}, Срок: {task['due_date']}")
            else:
                print("Список задач пуст.")

        elif choice == '3':
            task_id = int(input("Введите ID задачи для отметки как выполненной: "))
            task = next((task for task in tasks if task['id'] == task_id), None)
            if task:
                task['done'] = True
                print("Задача отмечена как выполненная!")
            else:
                print("Задача не найдена.")

        elif choice == '4':
            task_id = int(input("Введите ID задачи для редактирования: "))
            task = next((task for task in tasks if task['id'] == task_id), None)
            if task:
                task['title'] = input(f"Введите новое название (текущее: {task['title']}): ") or task['title']
                task['description'] = input(f"Введите новое описание (текущее: {task['description']}): ") or task[
                    'description']
                task['priority'] = input(f"Введите новый приоритет (текущий: {task['priority']}): ") or task['priority']
                while True:
                    due_date_str = input(f"Введите новый срок выполнения (ДД-ММ-ГГГГ, текущий: {task['due_date']}): ")
                    if due_date_str == "":
                        break
                    if re.match(r"^\d{2}-\d{2}-\d{4}$", due_date_str):
                        task['due_date'] = due_date_str
                        break
                    else:
                        print("Неверный формат даты. Используйте формат ДД-ММ-ГГГГ.")
                print("Задача успешно отредактирована!")
            else:
                print("Задача не найдена.")


        elif choice == '5':
            task_id = int(input("Введите ID задачи для удаления: "))
            tasks[:] = [task for task in tasks if task['id'] != task_id]
            print("Задача успешно удалена!")

        elif choice == '6':  # Экспорт в CSV
            filename = input("Введите имя CSV-файла для экспорта: ")
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['id', 'title', 'description', 'done', 'priority', 'due_date']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(tasks)
                print("Задачи успешно экспортированы в CSV-файл.")
            except Exception as e:
                print(f"Произошла ошибка при экспорте в CSV: {e}")

        elif choice == '7':  # Импорт из CSV
            filename = input("Введите имя CSV-файла для импорта: ")
            try:
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            task = Task(next_id, row['title'], row['description'], row['done'] == 'True',
                                        row['priority'], row['due_date'])
                            tasks.append(task.__dict__)
                            next_id += 1
                        except KeyError as e:
                            print(f"Ошибка при импорте: Отсутствует поле {e} в CSV файле.")
                    print("Задачи успешно импортированы из CSV-файла.")
            except FileNotFoundError:
                print(f"Ошибка: Файл {filename} не найден.")
            except Exception as e:
                print(f"Произошла ошибка при импорте CSV: {e}")

        elif choice == '8':
            break
        else:
            print("Неверный выбор.")

    save_data(tasks, 'tasks.json')


def manage_contacts():
    contacts = load_data('contacts.json')
    next_id = len(contacts) + 1 if contacts else 1
    while True:
        print("\nУправление контактами:")
        print("1. Добавить новый контакт")
        print("2. Поиск контакта")
        print("3. Редактировать контакт")
        print("4. Удалить контакт")
        print("5. Экспорт контактов в CSV")
        print("6. Импорт контактов из CSV")
        print("7. Назад")
        choice = input("Выберите действие: ")

        if choice == '1':
            name = input("Введите имя контакта: ")
            phone = input("Введите номер телефона (необязательно): ")
            email = input("Введите email (необязательно): ")
            contact = Contact(next_id, name, phone, email)
            contacts.append(contact.__dict__)
            next_id += 1
            print("Контакт успешно добавлен!")

        elif choice == '2':
            search_term = input("Введите имя или номер телефона для поиска: ")
            results = [contact for contact in contacts if search_term.lower() in contact['name'].lower() or (
                        contact['phone'] and search_term.lower() in contact['phone'].lower())]
            if results:
                for contact in results:
                    print(
                        f"ID: {contact['id']}, Имя: {contact['name']}, Телефон: {contact['phone']}, Email: {contact['email']}")
            else:
                print("Контакт не найден.")

        elif choice == '3':
            contact_id = int(input("Введите ID контакта для редактирования: "))
            contact = next((contact for contact in contacts if contact['id'] == contact_id), None)
            if contact:
                contact['name'] = input(f"Введите новое имя (текущее: {contact['name']}): ") or contact['name']
                contact['phone'] = input(f"Введите новый номер телефона (текущий: {contact['phone']}): ") or contact[
                    'phone']
                contact['email'] = input(f"Введите новый email (текущий: {contact['email']}): ") or contact['email']
                print("Контакт успешно отредактирован!")
            else:
                print("Контакт не найден.")

        elif choice == '4':
            contact_id = int(input("Введите ID контакта для удаления: "))
            contacts[:] = [contact for contact in contacts if contact['id'] != contact_id]
            print("Контакт успешно удален!")

        elif choice == '5':  # Экспорт в CSV
            filename = input("Введите имя CSV-файла для экспорта: ")
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['id', 'name', 'phone', 'email']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(contacts)
                print("Контакты успешно экспортированы в CSV-файл.")
            except Exception as e:
                print(f"Произошла ошибка при экспорте в CSV: {e}")

        elif choice == '6':  # Импорт из CSV
            filename = input("Введите имя CSV-файла для импорта: ")
            try:
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            contact = Contact(next_id, row['name'], row['phone'], row['email'])
                            contacts.append(contact.__dict__)
                            next_id += 1
                        except KeyError as e:
                            print(f"Ошибка при импорте: Отсутствует поле {e} в CSV файле.")
                    print("Контакты успешно импортированы из CSV-файла.")
            except FileNotFoundError:
                print(f"Ошибка: Файл {filename} не найден.")
            except Exception as e:
                print(f"Произошла ошибка при импорте CSV: {e}")

        elif choice == '7':
            break
        else:
            print("Неверный выбор.")

    save_data(contacts, 'contacts.json')


def manage_finances():
    finances = load_data('finance.json')
    next_id = len(finances) + 1 if finances else 1
    while True:
        print("\nУправление финансовыми записями:")
        print("1. Добавить новую запись")
        print("2. Просмотреть все записи")
        print("3. Генерация отчёта")
        print("4. Удалить запись")
        print("5. Экспорт финансовых записей в CSV")
        print("6. Импорт финансовых записей из CSV")
        print("7. Назад")
        choice = input("Выберите действие: ")

        if choice == '1':
            while True:
                try:
                    amount = float(input("Введите сумму (положительное число для дохода, отрицательное для расхода): "))
                    break
                except ValueError:
                    print("Неверный формат суммы. Пожалуйста, введите число.")
            category = input("Введите категорию операции: ")
            while True:
                date_str = input("Введите дату операции (ДД-ММ-ГГГГ): ")
                if re.match(r"^\d{2}-\d{2}-\d{4}$", date_str):
                    date = date_str
                    break
                else:
                    print("Неверный формат даты. Используйте формат ДД-ММ-ГГГГ.")
            description = input("Введите описание операции (необязательно): ")
            record = FinanceRecord(next_id, amount, category, date, description)
            finances.append(record.__dict__)
            next_id += 1
            print("Финансовая запись успешно добавлена!")

        elif choice == '2':
            if finances:
                for record in finances:
                    type_op = "Доход" if record['amount'] > 0 else "Расход"
                    print(
                        f"ID: {record['id']}, Тип: {type_op}, Сумма: {record['amount']}, Категория: {record['category']}, Дата: {record['date']}, Описание: {record['description']}")
            else:
                print("Список финансовых записей пуст.")

        elif choice == '3':
            while True:
                start_date_str = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
                end_date_str = input("Введите конечную дату (ДД-ММ-ГГГГ): ")
                if re.match(r"^\d{2}-\d{2}-\d{4}$", start_date_str) and re.match(r"^\d{2}-\d{2}-\d{4}$", end_date_str):
                    start_date = start_date_str
                    end_date = end_date_str
                    break
                else:
                    print("Неверный формат даты. Используйте формат ДД-ММ-ГГГГ.")

            report_filename = f"report_{start_date}_{end_date}.csv"
            try:
                with open(report_filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['id', 'amount', 'category', 'date', 'description']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows([rec for rec in finances if start_date <= rec['date'] <= end_date])

                total_income = sum(
                    rec['amount'] for rec in finances if rec['amount'] > 0 and start_date <= rec['date'] <= end_date)
                total_expense = sum(
                    rec['amount'] for rec in finances if rec['amount'] < 0 and start_date <= rec['date'] <= end_date)
                balance = total_income + total_expense

                print(f"\nФинансовый отчёт за период с {start_date} по {end_date}:")
                print(f"- Общий доход: {total_income:.2f} руб.")
                print(f"- Общие расходы: {abs(total_expense):.2f} руб.")
                print(f"- Баланс: {balance:.2f} руб.")
                print(f"Подробная информация сохранена в файле {report_filename}")
            except Exception as e:
                print(f"Произошла ошибка при генерации отчета: {e}")


        elif choice == '4':
            record_id = int(input("Введите ID записи для удаления: "))
            finances[:] = [record for record in finances if record['id'] != record_id]
            print("Запись успешно удалена!")

        elif choice == '5':
            filename = input("Введите имя CSV-файла для экспорта: ")
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['id', 'amount', 'category', 'date', 'description']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(finances)
                print("Финансовые записи успешно экспортированы в CSV-файл.")
            except Exception as e:
                print(f"Произошла ошибка при экспорте в CSV: {e}")

        elif choice == '6':  # Импорт из CSV
            filename = input("Введите имя CSV-файла для импорта: ")
            try:
                with open(filename, 'r', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        try:
                            record = FinanceRecord(next_id, float(row['amount']), row['category'], row['date'],
                                                   row['description'])
                            finances.append(record.__dict__)
                            next_id += 1
                        except (KeyError, ValueError) as e:
                            print(f"Ошибка при импорте: {e}")
                    print("Финансовые записи успешно импортированы из CSV-файла.")
            except FileNotFoundError:
                print(f"Ошибка: Файл {filename} не найден.")
            except Exception as e:
                print(f"Произошла ошибка при импорте CSV: {e}")

        elif choice == '7':
            break
        else:
            print("Неверный выбор.")

    save_data(finances, 'finance.json')


def calculator():
    while True:
        try:
            expression = input("Введите выражение (или 'q' для выхода): ")
            if expression.lower() == 'q':
                break
            result = eval(expression)  # Используем eval с осторожностью в реальных приложениях!
            print("Результат:", result)
        except (SyntaxError, NameError, ZeroDivisionError):
            print("Ошибка! Неверный формат выражения.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


def main():
    if not os.path.exists('notes.json'):
        save_data([], 'notes.json')
    if not os.path.exists('tasks.json'):
        save_data([], 'tasks.json')
    if not os.path.exists('contacts.json'):
        save_data([], 'contacts.json')
    if not os.path.exists('finance.json'):
        save_data([], 'finance.json')

    while True:
        print("\nДобро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            manage_notes()
        elif choice == '2':
            manage_tasks()
        elif choice == '3':
            manage_contacts()
        elif choice == '4':
            manage_finances()
        elif choice == '5':
            calculator()
        elif choice == '6':
            break
        else:
            print("Неверный выбор.")


if __name__ == "__main__":
    main()

