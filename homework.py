class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    
    
    def get_message(self) -> str:
        """Возвращает строку информационного сообщения."""
        return (f'Тип тренировки: {self.training_type};'
               f'Длительность: {self.duration:.3f} ч.;'
               f'Дистанция: {self.distance:.3f} км;'
               f'Ср. скорость: {self.speed:.3f} км/ч;'
               f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    T_IN_MI: int = 60


    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM 

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79


    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                ):
        super().__init__(action, duration, weight)
    
    
    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
 * self.weight / self.M_IN_KM * self.duration * self.T_IN_MI)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1: float = 0.035  # Коэффициент для подсчета калорий.
    K_2: float = 0.029  # Коэффициент для подсчета калорий.
    LEN_STEP: float = 0.65
    SM_IN_M: int = 100
    K_IN_M: float = 3.6
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ):
        super().__init__(action,
                         duration,
                         weight)
        self.height = height
    

    def get_spent_calories(self) -> float:
        return ((self.K_1 * self.weight + ((self.get_mean_speed() / self.K_IN_M)**2 / (self.height / self.SM_IN_M))
 * self.K_2 * self.weight) * self.duration * self.T_IN_MI)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int,
                ):
        super().__init__(action,
                         duration,
                         weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    
    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration
    

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT) * self.CALORIES_WEIGHT * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type == 'SWM':
        return Swimming(*data)
    elif workout_type == 'RUN':
        return Running(*data)
    elif workout_type == 'WLK':
        return SportsWalking(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

