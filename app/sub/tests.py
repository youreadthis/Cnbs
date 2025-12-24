
import base_region



coords = [(0, 0), (300, 0), (300, 200), (150, 300), (0, 200)]

# Радиусы
R1, R2, R3 = 20, 12, 4

print("Инициализация и расчет...")

# ТЕПЕРЬ МОЖНО ТАК: Создаем и сразу считаем
my_region = base_region.Region(coords, r1=R1, r2=R2, r3=R3, percent1=80)

print(my_region)

# Визуализация: теперь можно не передавать results, они возьмутся из my_region
base_region.visualize_towers(my_region, R1, R2, R3)