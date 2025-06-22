import datetime

from T2.progress_dedline import calculate_overall_progress, check_deadlines
from T2.goal import Goal
from T2.load_goals_from_csv import LoadGoals
from T2.save_goals_to_csv import SaveGoal

filename = "goals.csv"

# Загрузка целей из CSV (если файл существует)
load_goal = LoadGoals()
available_categories = ["Работа", "Здоровье", "Личное", "Развлечения"]
goals = load_goal.load_goals_from_csv(filename, available_categories)

# Если файл не существует или пустой, создаем несколько целей
if not goals:
    goals = [
        Goal("Массаж", 150000, 50000, "Здоровье", '2025-07-01'),
        Goal("Отпуск в Италии", 300000, 100000, "Развлечения", '2025-07-01'),
        Goal("Новый велосипед", 50000, 20000, "Спорт", '2025-07-01')
    ]

# Добавление новой цели вручную
while True:
    add_new = input("Добавить новую цель? (1-да/2-нет): ")
    if add_new == "1":
        while True:
            a = 0
            try:
                name = input("Введите название цели: ")
                target_amount = float(input("Введите итоговую сумму: "))
                current_balance = float(input("Введите текущий баланс: "))
                print("\nДоступные категории:")
                for i, category in enumerate(available_categories):
                    print(f"{i + 1}. {category}")
                category_int = input("Введите номер категории из списка выше: ")
                if category_int == '1':
                    category = 'Работа'
                elif category_int == '2': category = 'Здоровье'
                elif category_int == '3': category = 'Личное'
                elif category_int == '4': category = 'Развлечения'
                else: category = 'не допустимую категорию'
                print(f'выбрали {category}')
                if category not in available_categories:
                    print("\nНекорректная категория. Пожалуйста, выберайте из списка. Давайте начнем с начала")
                    continue
                deadline = input("\nВведите срок выполнения цели в формате ГГГГ-ММ-ДД: ")
                deposit_frequency_days = int(
                input("Как часто планируете пополнять цель (в днях)?: "))
                break  # Выход из цикла ввода, если все данные введены корректно
            except ValueError:
                print("Некорректный ввод суммы. Пожалуйста, введите число.")

        new_goal = Goal(name, target_amount, current_balance, category, deadline, deposit_frequency_days)
        goals.append(new_goal)
        print(f"Цель '{name}' добавлена.")
    else:
        break

# Вывод информации о целях
for i, goal in enumerate(goals):
    print(f"{i + 1}: {goal}")

# Ручной ввод депозита для выбранной цели
if goals:
    while True:
        try:
            goal_number = int(input("Введите номер цели для внесения депозита (или 0 для пропуска): "))
            if goal_number == 0:
                break
            if 1 <= goal_number <= len(goals):
                selected_goal = goals[goal_number - 1]
                deposit_amount = float(input(f"Введите сумму для внесения в цель '{selected_goal.name}': "))
                selected_goal.deposit(deposit_amount)
                break
            else:
                print("Некорректный номер цели.")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число.")

# Предложение даты завершения для выбранной цели
if goals:
    while True:
        try:
            goal_number = int(input("Введите номер цели, для которой хотите предложить дату завершения (или 0 для пропуска): "))
            if goal_number == 0:
                break
            if 1 <= goal_number <= len(goals):
                selected_goal = goals[goal_number - 1]
                suggested_deadline = selected_goal.suggest_deadline()
                if suggested_deadline:
                    print(f"Предлагаемая дата завершения для цели '{selected_goal.name}': {suggested_deadline}")
                break
            else:
                print("Некорректный номер цели.")
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число.")

# Проверка сроков выполнения целей на определенную дату
while True:
    check_date_str = input(
        "Введите дату для проверки сроков выполнения целей в формате ГГГГ-ММ-ДД (или нажмите Enter для использования текущей даты): ")
    if not check_date_str:
        check_date = datetime.date.today()
        break
    try:
        check_date = datetime.datetime.strptime(check_date_str, "%Y-%m-%d").date()
        break
    except ValueError:
        print("Некорректный формат даты. Используйте ГГГГ-ММ-ДД.")
check_deadlines(goals, check_date)  # Вызываем с заданной датой


# Удаление цели
while True:
    try:
        goal_to_delete_index = int(input("Введите номер цели для удаления (или 0 для отмены): ")) - 1
        if goal_to_delete_index == -1:
            print("Удаление отменено.")
            break
        if 0 <= goal_to_delete_index < len(goals):
            deleted_goal = goals.pop(goal_to_delete_index)
            print(f"Цель '{deleted_goal.name}' удалена.")
            break
        else:
            print("Некорректный номер цели.")
    except ValueError:
        print("Пожалуйста, введите число.")

# Вывод информации о целях после удаления
print("\nСписок целей после удаления:")
for goal in goals:
    print(goal)

# Вычисление и вывод общего прогресса
overall_progress = calculate_overall_progress(goals)
print(f"\nОбщий прогресс по всем целям: {overall_progress:.2f}%")


# Сохранение целей в CSV
save_goal = SaveGoal()
save_goal.save_goals_to_csv(filename, goals)
print(f"Цели сохранены в файл '{filename}'")