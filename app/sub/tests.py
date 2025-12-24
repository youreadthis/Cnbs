import visualization
import base_region



# 1. Создаем регион (например, сложный пятиугольник)
coords = [(0, 0), (300, 0), (300, 200), (150, 300), (0, 200)]
region = base_region.Region(coords)

# 2. Задаем параметры
R1, R2, R3 = 40, 20, 4.5

# 3. Считаем
print("Вычисляем...")
towers = region.find_all_centers_of_towers(R1, R2, R3, percent1=80, percent2=65, percent3=90)

print(region)

# 4. Рисуем
visualization.visualize_towers(region, towers, R1, R2, R3)