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
        Упаковывает окружности внутри региона в гексагональной сетке.
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
    def pack_secondary_circles(self, 
                               r_new: int, 
                               percent: int, 
                               # Первая группа (обязательная)
                               existing_circles: list[tuple], 
                               r_existing: int, 
                               # Вторая группа (опциональная)
                               existing_circles_2: list[tuple] = None, 
                               r_existing_2: int = None,
                               accuracy: int = 20):
        """
        Размещает новые окружности (r_new), избегая коллизий с одной или двумя группами существующих.
        """
        new_circles = []
        
        # 1. Подготовка групп препятствий
        # Собираем все препятствия в единый список формата: [(список_точек, радиус), ...]
        obstacle_groups = []
        
        # Добавляем первую группу
        if existing_circles:
            obstacle_groups.append((existing_circles, r_existing))
        else:
            raise ValueError("First of existing circles must be provided.")
            
        # Добавляем вторую группу, если она передана
        if existing_circles_2 and r_existing_2 is not None:
            obstacle_groups.append((existing_circles_2, r_existing_2))

        # min_dists_sq будет списком: [дистанция_для_группы_1, дистанция_для_группы_2]
        group_min_dists_sq = []
        for _, r_group in obstacle_groups:
            # (радиус_группы + радиус_новый)^2 * 0.999 (для устранения ошибки float)
            dist = (r_group + r_new) ** 2 * 0.999
            group_min_dists_sq.append(dist)

        # 2. Параметры сетки (на основе размера НОВЫХ окружностей)
        (min_x, min_y), (max_x, max_y) = self.rectangle
        dx = 2 * r_new
        dy_offset = math.sqrt(3) * r_new

        y = min_y + r_new
        row_index = 0
        
        # 3. Основной цикл генерации
        while y <= max_y - r_new:
            if row_index % 2 == 0:
                x_start = min_x + r_new
            else:
                x_start = min_x + r_new + r_new
                
            x = x_start
            while x <= max_x - r_new:
                candidate = (x, y)
                collision = False
                
                # --- ПРОВЕРКА КОЛЛИЗИЙ ---
                # Проходимся по всем группам препятствий
                for i, (group_coords, _) in enumerate(obstacle_groups):
                    min_dist_sq = group_min_dists_sq[i]
                    safe_dist_linear = math.sqrt(min_dist_sq) # Для быстрой проверки abs
                    
                    for ex, ey in group_coords:
                        # Оптимизация: быстрая проверка по осям (Manhattan-like)
                        if abs(ex - x) > safe_dist_linear or abs(ey - y) > safe_dist_linear:
                            continue
                        
                        # Точная проверка (Евклидова)
                        if (ex - x)**2 + (ey - y)**2 < min_dist_sq:
                            collision = True
                            break # Выход из цикла по окружностям группы
                    
                    if collision:
                        break # Выход из цикла по группам

                # --- ЕСЛИ НЕТ КОЛЛИЗИЙ ---
                if not collision:
                    # Проверяем, внутри ли региона
                    if self._check_circle_overlap(candidate, r_new, percent, accuracy):
                        new_circles.append(candidate)
                
                x += dx
            
            y += dy_offset
            row_index += 1
            
        return new_circles
    def find_all_centers_of_towers(self, r1:int, r2:int, r3:int, percent1:int=70, percent2:int=70, percent3:int=70) -> dict:
        """Находит центры башен внутри региона
        r1 <= r2 <= r3 - радиусы покрытия башен"""
        if r1 <= 0 or r2 <= 0 or r3 <= 0:
            raise ValueError("Radii must be positive values.")
        if r1<r2 or r2<r3:
            raise ValueError("R1 must be greater than R2, and R2 must be greater than R3.")
        if percent1<0 or percent1>100 or percent2<0 or percent2>100 or percent3<0 or percent3>100:
            raise ValueError("Percent values must be between 0 and 100.")
        # 1. Упаковка самых больших окружностей (r3)
        circles_r3 = self.pack_circles_hexagonal(r3, percent3, accuracy=50)
        # 2. Упаковка средних окружностей (r2)
        circles_r2 = self.pack_secondary_circles(r2, percent2, circles_r3, r3, accuracy=30)
        # 3. Упаковка самых маленьких окружностей (r1)
        circles_r1 = self.pack_secondary_circles(r1, percent1, circles_r3, r3, circles_r2, r2, accuracy=20)
        return {
            'r1_centers': circles_r1,
            'r2_centers': circles_r2,
            'r3_centers': circles_r3
        }
        
        