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


def check_circle_collision(x1, y1, r1, x2, y2, r2):
    """
    Returns True if two circles are colliding, False otherwise.
    Optimized to avoid using square root operations.
    """
    dx = x1 - x2
    dy = y1 - y2
    squared_distance = (dx ** 2) + (dy ** 2)

    radii_sum = r1 + r2
    squared_radii_sum = radii_sum ** 2

    return squared_distance <= squared_radii_sum
