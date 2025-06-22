import csv

class SaveGoal():
    def __init__(self):
        pass

    def save_goals_to_csv(self, filename, goals): # Сохраняет список объектов Goal в CSV файл.
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["name", "target_amount", "current_balance", "category", "deadline", "status",
                          "deposit_frequency_days"]

            # Добавляем динамически поля для прогресс уведомлений
            all_notification_points = set()
            for goal in goals:
                all_notification_points.update(goal.progress_notifications.keys())

            for point in sorted(all_notification_points):
                fieldnames.append(f"progress_notification_{point}")

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for goal in goals:
                writer.writerow(goal.to_dict())