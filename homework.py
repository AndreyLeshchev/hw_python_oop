from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message = (
        'Тип тренировки: {}; '
        'Длительность: {:.3f} ч.; '
        'Дистанция: {:.3f} км; '
        'Ср. скорость: {:.3f} км/ч; '
        'Потрачено ккал: {:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает строку информационного сообщения."""
        return self.message.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MI_IN_H: int = 60

    def __init__(
            self, action: int,
            duration: float, weight: float) -> None:
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
        raise NotImplementedError(f'Метод {self.get_spent_calories.__name__} '
                                  f'должен быть реализован в подклассе '
                                  f'{self.__class__.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        time_in_minutes: float = self.duration * self.MI_IN_H
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / self.M_IN_KM * time_in_minutes)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    FIRST_CAL_MEAN_WEIGHT: float = 0.035
    SECOND_CAL_MEAN_WEIGHT: float = 0.029
    M_SEC_COEF: float = 0.278
    SM_IN_M: int = 100

    def __init__(
            self, action: int,
            duration: float, weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        meters_second: float = self.get_mean_speed() * self.M_SEC_COEF
        height_meter: float = self.height / self.SM_IN_M
        time_in_minutes: float = self.duration * self.MI_IN_H
        return ((self.FIRST_CAL_MEAN_WEIGHT * self.weight
                 + (meters_second**2 / height_meter)
                 * self.SECOND_CAL_MEAN_WEIGHT * self.weight)
                * time_in_minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    CALORIES_WEIGHT: int = 2

    def __init__(
            self, action: int,
            duration: float, weight: float,
            length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_of_training: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in types_of_training:
        raise KeyError('Ошибка - операция не найдена')
    return types_of_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
