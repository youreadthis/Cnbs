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
        self.centers_of_towers = {}
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
    def get_centers_of_towers(self):
        return self.centers_of_towers
    def get_number_of_towers(self):
        return {k: len(v) for k, v in self.centers_of_towers.items()}
    def get_total_number_of_towers(self):
        return sum(len(v) for v in self.centers_of_towers.values())
    def __str__(self):
        # 1. Получаем данные
        total_towers = self.get_total_number_of_towers()
        towers_breakdown = self.get_number_of_towers()
        
        details_list = []
        # Сортируем ключи, чтобы R1 всегда был перед R2
        for key in sorted(towers_breakdown.keys()):
            count = towers_breakdown[key]
            clean_name = key.replace('_centers', '').upper()
            details_list.append(f"  • {clean_name}: {count} шт.")
        
        details_str = "\n".join(details_list) if details_list else "  (нет данных)"

        # 3. Форматируем площадь (2 знака после запятой)
        area_str = f"{self.area:,.2f}".replace(",", " ")

        return (
            f"========================================\n"
            f"📍 ОТЧЕТ О РЕГИОНЕ\n"
            f"========================================\n"
            f"Геометрия:\n"
            f"  • Вершин:  {len(self.coordinates)}\n"
            f"  • Площадь: {area_str} кв. ед.\n"
            f"----------------------------------------\n"
            f"Инфраструктура:\n"
            f"  • Всего вышек: {total_towers}\n"
            f"  • Детализация:\n"
            f"{details_str}\n"
            f"========================================"
        )
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
        """
        (min_x, min_y), (max_x, max_y) = self.rectangle
        circles = []
        
        if 2 * r > (max_x - min_x) or 2 * r > (max_y - min_y):
            return circles

        dx = 2 * r
        dy_offset = math.sqrt(3) * r
        
        # Исправление 1: Добавляем epsilon для корректной обработки границ
        epsilon = 1e-9

        y = min_y + r
        row_index = 0

        while y <= max_y - r + epsilon:
            if row_index % 2 == 0:
                x_start = min_x + r
            else:
                x_start = min_x + r + r

            x = x_start
            while x <= max_x - r + epsilon:
                if self._check_circle_overlap((x, y), r, percent, accuracy):
                    circles.append((x, y))
                x += dx
            
            y += dy_offset
            row_index += 1

        return circles

    def _calculate_intersection_area(self, r1: float, r2: float, d: float) -> float:
        """
        Вычисляет площадь пересечения двух окружностей.
        r1, r2: радиусы окружностей.
        d: расстояние между центрами.
        """
        # 1. Если окружности не пересекаются
        if d >= r1 + r2:
            return 0.0
        
        # 2. Если одна окружность полностью внутри другой
        if d <= abs(r1 - r2):
            return math.pi * min(r1, r2) ** 2
        
        # 3. Частичное пересечение (формула через радиусы и расстояние)
        r1_sq = r1 ** 2
        r2_sq = r2 ** 2
        
        # Угол сектора первой окружности
        alpha = math.acos((r1_sq + d**2 - r2_sq) / (2 * r1 * d))
        # Угол сектора второй окружности
        beta = math.acos((r2_sq + d**2 - r1_sq) / (2 * r2 * d))
        
        # Площадь пересечения = сумма площадей двух сегментов
        # S_segment = 0.5 * r^2 * (angle - sin(angle)) - формула сегмента,
        # но здесь используется оптимизированная общая формула пересечения:
        area = r1_sq * alpha + r2_sq * beta - \
               0.5 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))
               
        return area

    def pack_secondary_circles(self, 
                               r_new: int, 
                               percent: int, 
                               existing_circles: list[tuple], 
                               r_existing: int, 
                               existing_circles_2: list[tuple] = None, 
                               r_existing_2: int = None,
                               accuracy: int = 20):
        """
        Размещает новые окружности (r_new).
        Условие коллизии: 'Чистая площадь' новой окружности должна быть >= percent.
        То есть площадь пересечений не должна превышать (100 - percent).
        """
        new_circles = []
        
        obstacle_groups = []
        if existing_circles:
            obstacle_groups.append((existing_circles, r_existing))
        if existing_circles_2 and r_existing_2 is not None:
            obstacle_groups.append((existing_circles_2, r_existing_2))

        # 1. Считаем максимально допустимую площадь перекрытия
        # Если percent=80 (хотим 80% чистого), то overlap может быть до 20%
        circle_area = math.pi * (r_new ** 2)
        max_allowed_overlap = circle_area * ((100 - percent) / 100.0)

        # Предварительный расчет квадратов для быстрого отсева
        group_min_dists_sq = []
        for _, r_group in obstacle_groups:
            # Дистанция, при которой круги хотя бы касаются
            dist = (r_group + r_new) ** 2 * 0.999
            group_min_dists_sq.append(dist)

        (min_x, min_y), (max_x, max_y) = self.rectangle
        dx = 2 * r_new
        dy_offset = math.sqrt(3) * r_new
        epsilon = 1e-9

        y = min_y + r_new
        row_index = 0
        
        while y <= max_y - r_new + epsilon:
            if row_index % 2 == 0:
                x_start = min_x + r_new
            else:
                x_start = min_x + r_new + r_new
                
            x = x_start
            while x <= max_x - r_new + epsilon:
                candidate = (x, y)
                
                # Накопитель перекрытия для текущего кандидата
                current_overlap = 0.0
                is_valid = True
                
                for i, (group_coords, r_group) in enumerate(obstacle_groups):
                    min_dist_sq = group_min_dists_sq[i]
                    safe_dist = r_group + r_new # Дистанция полного касания
                    
                    for ex, ey in group_coords:
                        # --- ОПТИМИЗАЦИИ ---
                        # 1. Если препятствие слишком высоко по Y (список отсортирован), выходим
                        if ey > y + safe_dist:
                             break 
                        # 2. Быстрые проверки по осям
                        if abs(ey - y) > safe_dist:
                            continue
                        if abs(ex - x) > safe_dist:
                            continue
                        
                        d_sq = (ex - x)**2 + (ey - y)**2
                        
                        # --- ПРОВЕРКА КОЛЛИЗИИ ---
                        # Если расстояние меньше суммы радиусов -> есть пересечение
                        if d_sq < min_dist_sq:
                            # Считаем точную площадь пересечения
                            dist = math.sqrt(d_sq)
                            overlap_area = self._calculate_intersection_area(r_new, r_group, dist)
                            current_overlap += overlap_area
                            
                            # Если накопленное пересечение уже больше допустимого -> окружность не подходит
                            if current_overlap > max_allowed_overlap:
                                is_valid = False
                                break 
                    
                    if not is_valid:
                        break # Выход из цикла по группам

                # Если по коллизиям с соседями прошли, проверяем границы региона
                if is_valid:
                    # accuracy здесь отвечает за проверку "внутри многоугольника"
                    if self._check_circle_overlap(candidate, r_new, percent, accuracy):
                        new_circles.append(candidate)
                
                x += dx
            
            y += dy_offset
            row_index += 1
            
        return new_circles

    def find_all_centers_of_towers(self, r1: int, r2: int, r3: int, 
                                   percent1: int = 70, percent2: int = 70, percent3: int = 70) -> dict:
        """
        Находит центры башен.
        r1 - самый большой радиус, r2 - средний, r3 - самый маленький.
        """
        # Валидация входных данных
        if r1 <= 0 or r2 <= 0 or r3 <= 0:
            raise ValueError("Radii must be positive values.")
        if r1 < r2 or r2 < r3:
            raise ValueError("R1 must be greater than R2, and R2 must be greater than R3.")
        
        # 1. Упаковка самых БОЛЬШИХ (r1). Результат в circles_r1
        circles_r1 = self.pack_circles_hexagonal(r1, percent1, accuracy=50)
        
        # 2. Упаковка СРЕДНИХ (r2). Избегаем circles_r1. Результат в circles_r2
        circles_r2 = self.pack_secondary_circles(
            r_new=r2, 
            percent=percent2, 
            existing_circles=circles_r1, 
            r_existing=r1, 
            accuracy=30
        )
        
        # 3. Упаковка МАЛЕНЬКИХ (r3). Избегаем r1 и r2. Результат в circles_r3
        circles_r3 = self.pack_secondary_circles(
            r_new=r3, 
            percent=percent3, 
            existing_circles=circles_r1, 
            r_existing=r1, 
            existing_circles_2=circles_r2, 
            r_existing_2=r2, 
            accuracy=20
        )
        self.centers_of_towers = {
            'r1_centers': circles_r1,
            'r2_centers': circles_r2,
            'r3_centers': circles_r3
        }
        return {
            'r1_centers': circles_r1,
            'r2_centers': circles_r2,
            'r3_centers': circles_r3
        }
    

