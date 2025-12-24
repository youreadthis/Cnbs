import math
import random


class Region:
    """Класс, представляющий географический регион."""
    def __init__(self, coordinates:list[tuple]):
        """Инициализирует регион с заданными координатами вершин."""
        if not coordinates or len(coordinates) < 3:
            raise ValueError("less than 3 coordinates provided")
        self.coordinates = coordinates
        self.area = self.calculate_area()
        self.rectangle = self.calculate_rectangle()
    def calculate_area(self):
        """Вычисляет площадь многоугольника по формуле Гаусса."""
        coords = self.coordinates
        n = len(self.coordinates) 
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += coords[i][0] * coords[j][1]
            area -= coords[j][0] * coords[i][1]
        return abs(area) / 2.0
    def calculate_rectangle(self):
        """Вычисляет ограничивающий прямоугольник региона."""
        cords=self.coordinates
        min_x = cords[0][0]
        max_x = cords[0][0]
        min_y = cords[0][1]
        max_y = cords[0][1]
        for (x, y) in cords:
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
        return ((min_x, min_y), (max_x, max_y))
    def get_area(self):
        return self.area
    def get_bounding_rectangle(self):
        return self.rectangle
    def get_coordinates(self):
        return self.coordinates
    def contains(self, point:tuple):
        """Проверяет, находится ли точка внутри региона."""
        x, y = point
        (min_x, min_y), (max_x, max_y) = self.rectangle
        if not (min_x <= x <= max_x and min_y <= y <= max_y):
            return False
        inside = False
        n = len(self.coordinates)
        j = n - 1
        for i in range(n):
            xi, yi = self.coordinates[i]
            xj, yj = self.coordinates[j]
            
            intersect = ((yi > y) != (yj > y)) and \
                        (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
            if intersect:
                inside = not inside
            j = i
            
        return inside
    def _check_circle_overlap(self, center: tuple, r: float, threshold_percent: int, samples: int = 25) -> bool:
        """
        Проверяет, находится ли заданный процент площади окружности внутри региона.
        Использует метод Монте-Карло.
        """
        cx, cy = center
        
        # ОПТИМИЗАЦИЯ 1: Если центр внутри, и процент нужен небольшой (<40%) 
        center_inside = self.contains(center)
        if center_inside and threshold_percent < 40:
             return True
        
        # ОПТИМИЗАЦИЯ 2: Если центр снаружи, а нужен высокий процент (>60%)
        if not center_inside and threshold_percent > 60:
            return False

        inside_count = 0
        
        # Генерируем точки и проверяем их
        for _ in range(samples):
            # Генерация случайной точки внутри круга (равномерное распределение)
            angle = random.random() * 2 * math.pi
            dist = r * math.sqrt(random.random())
            
            px = cx + dist * math.cos(angle)
            py = cy + dist * math.sin(angle)
            
            if self.contains((px, py)):
                inside_count += 1
        
        calculated_percent = (inside_count / samples) * 100
        return calculated_percent >= threshold_percent

    def pack_circles_hexagonal(self, r: int, percent: int, accuracy: int = 30):
        """
        percent: Минимальный процент площади окружности, который должен быть внутри региона (0-100).
        accuracy: Количество случайных точек для проверки площади (больше = точнее, но медленнее).
        """
        (min_x, min_y), (max_x, max_y) = self.rectangle
        circles = []
        
        if 2 * r > (max_x - min_x) or 2 * r > (max_y - min_y):
            return circles

        dx = 2 * r
        dy_offset = math.sqrt(3) * r

        y = min_y + r
        row_index = 0

        while y <= max_y - r:
            if row_index % 2 == 0:
                x_start = min_x + r
            else:
                x_start = min_x + r + r

            x = x_start
            while x <= max_x - r:
                # Используем проверку площади
                if self._check_circle_overlap((x, y), r, percent, accuracy):
                    circles.append((x, y))
                
                x += dx
            
            y += dy_offset
            row_index += 1

        return circles
    
    
        
        