import math


def get_diagonal_velocity(dx, dy, speed):
    """
    Рассчитывает скорость по осям X и Y для движения по диагонали.
    dx, dy — направление (-1, 0, 1)
    """
    # Находим длину вектора (расстояние)
    distance = math.hypot(dx, dy)

    if distance == 0:
        return 0, 0

    # Нормализуем вектор и умножаем на общую скорость
    vx = (dx / distance) * speed
    vy = (dy / distance) * speed

    return vx, vy
