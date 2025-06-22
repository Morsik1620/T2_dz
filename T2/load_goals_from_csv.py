import csv
from T2.goal import Goal


class LoadGoals:
    def __init__(self):
        pass

    def load_goals_from_csv(self, filename, available_categories): # Загружает список объектов Goal из CSV файла.
        goals = []
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    category = row["category"]
                    deadline = row["deadline"]
                    deposit_frequency_days = int(row.get("deposit_frequency_days", 7))  # Загружаем, по умолчанию 7

                    if category not in available_categories:
                        print(
                            f"Предупреждение: Категория '{category}' не входит в список допустимых категорий.  Цель пропущена.")
                        continue  # Пропускаем эту цель, если категория недопустима

                    goal = Goal(
                        row["name"],
                        float(row["target_amount"]),
                        float(row["current_balance"]),
                        category,
                        deadline,
                        deposit_frequency_days,  # Передаем частоту
                        row["status"]
                    )

                    # Загружаем информацию об уведомлениях из файла
                    for key, value in row.items():
                        if key.startswith("progress_notification_"):
                            progress = int(key.split("_")[-1])
                            goal.progress_notifications[progress] = value.lower() == "true"

                    goals.append(goal)
        except FileNotFoundError:
            print(f"Файл '{filename}' не найден.  Будет создан новый файл при сохранении.")
        return goals