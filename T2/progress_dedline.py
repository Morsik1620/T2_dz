import datetime


def calculate_overall_progress(goals):# Вычисляет общий прогресс по всем целям
    total_current_balance = sum(goal.current_balance for goal in goals)
    total_target_amount = sum(goal.target_amount for goal in goals)

    if total_target_amount == 0:
        return 100.0  # Избегаем деления на ноль, если общая целевая сумма равна 0
    return (total_current_balance / total_target_amount) * 100

def check_deadlines(goals, check_date=None): # Проверяет приближение сроков выполнения целей и выводит уведомления.
    if check_date is None:
        check_date = datetime.date.today()

    for goal in goals:
        if goal.is_deadline_approaching(check_date):
            days_left = (goal.deadline - check_date).days
            print(f"Внимание: Срок выполнения цели '{goal.name}' ({goal.category}) истекает через {days_left} дней! (Проверено на {check_date})")

