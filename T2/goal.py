import datetime


class Goal:
    def __init__(self, name, target_amount, current_balance, category, deadline,
                 deposit_frequency_days=7,  # определил частоту пополнения
                 status = "Активна"):
        self.name = name                                # Название цели.
        self.target_amount = float(target_amount)       # Итоговая сумма, необходимая для достижения цели
        self.current_balance = float(current_balance)   # Текущий баланс, накопленный на данный момент.
        self.category = category                        # Категория цели (например, "Путешествие", "Автомобиль", "Образование").
        self.status = status                            # Статус цели (например, "Активна", "Достигнута", "Приостановлена").
        try:
            self.deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            print("Некорректный формат даты. Используйте ГГГГ-ММ-ДД. Дата установлена на сегодня.")
            self.deadline = datetime.date.today()
        self.progress_notifications = {}  # Словарь для хранения информации об уведомлениях по прогрессу
        self.deposit_frequency_days = deposit_frequency_days  # Сохраняем частоту пополнений
        self.deposit_history = []  #  Список для хранения истории пополнений (дата, сумма)


    def __str__(self): # Возвращает строковое представление объекта Goal.
        return f"Цель: {self.name}, Категория: {self.category}, Цель: {self.target_amount}, Баланс: {self.current_balance}, Статус: {self.status}, Прогресс: {self.get_progress():.2f}%, Срок: {self.deadline}, Пополнение: каждые {self.deposit_frequency_days} дн."

    def deposit(self, amount): # Добавляет указанную сумму к текущему балансу.
        if amount > 0:
            if self.current_balance + amount <= self.target_amount: # проверка, что  при внесении средств текущий баланс не превысит целевую сумму.
                 self.current_balance += amount
                 print(f"Внесено {amount} в цель '{self.name}'. Новый баланс: {self.current_balance}")
            else:
                deposit_amount = self.target_amount - self.current_balance
                self.current_balance = self.target_amount
                print(f"Внесено {deposit_amount} в цель '{self.name}'. Новый баланс: {self.current_balance}. Больше внести нельзя, т.к. цель достигнута")

            self.update_status()
            self.check_progress_notifications()  # Проверяем уведомления после внесения депозита
            self.deposit_history.append((datetime.date.today(), amount)) # Сохраняем информацию о пополнении
        else:
            print("Сумма взноса должна быть положительной.")

    def withdraw(self, amount: float):                                          #  Сумма для снятия.
        if amount > 0 and amount <= self.current_balance:
            self.current_balance -= amount
            print(f"Снято {amount} из цели '{self.name}'. Новый баланс: {self.current_balance}")
            self.update_status()
            self.check_progress_notifications() # Проверяем уведомления после cнятия средств
        else:
            print("Недостаточно средств или некорректная сумма для снятия.")

    def update_status(self): # Обновляет статус цели в зависимости от текущего баланса и целевой суммы.
        if self.current_balance >= self.target_amount: # После достижения цели (когда текущий баланс >= итоговая сумма) менять статус на "выполнена"
            self.status = "Выполнена"
            print(f"Цель '{self.name}' достигнута!")
        elif self.status == "Достигнута":
            self.status = "В процессе"

    def get_progress(self) -> float: # Процент прогресса (от 0.0 до 100.0).
        if self.target_amount == 0:
            return 100.0  # Избегаем деления на ноль, если целевая сумма равна 0
        return (self.current_balance / self.target_amount) * 100


    def to_dict(self):
        goal_dict = {
            "name": self.name,
            "target_amount": self.target_amount,
            "current_balance": self.current_balance,
            "category": self.category,
            "deadline": str(self.deadline),
            "status": self.status,
            "deposit_frequency_days": self.deposit_frequency_days,
        }
        # Сохраняем информацию об уведомлениях
        for progress, notified in self.progress_notifications.items():
            goal_dict[f"progress_notification_{progress}"] = notified

        return goal_dict

    def is_deadline_approaching(self, check_date, days=7): # Проверяет, приближается ли срок выполнения цели.
        time_difference = self.deadline - check_date
        return 0 <= time_difference.days <= days

    def check_progress_notifications(self):
        progress = int(self.get_progress())  # Получаем прогресс в виде целого числа
        notification_points = [25, 50, 75, 90] # Определяем точки прогресса для уведомлений

        for point in notification_points:
            if progress >= point and point not in self.progress_notifications:
                print(f"Ура! Вы достигли {point}% цели '{self.name}'!")
                self.progress_notifications[point] = True # Отмечаем, что уведомление для этого процента уже было показано

    def has_progress_notification(self, progress):
        return self.progress_notifications.get(progress, False)

    def suggest_deadline(self): # Предлагает дату завершения цели на основе истории пополнений и частоты.
        if not self.deposit_history:
            print("Нет истории пополнений. Невозможно рассчитать предложенную дату.")
            return None

        # Вычисляем среднюю сумму пополнения
        total_deposit = sum(amount for _, amount in self.deposit_history)
        average_deposit = total_deposit / len(self.deposit_history)

        # Вычисляем, сколько еще нужно внести
        remaining_amount = self.target_amount - self.current_balance

        # Вычисляем, сколько пополнений потребуется
        if average_deposit == 0:
            print("Средняя сумма пополнения равна 0. Невозможно рассчитать предложенную дату.")
            return None

        num_deposits_needed = remaining_amount / average_deposit

        # Вычисляем предложенную дату
        estimated_days = num_deposits_needed * self.deposit_frequency_days
        suggested_deadline = datetime.date.today() + datetime.timedelta(days=estimated_days)

        return suggested_deadline
