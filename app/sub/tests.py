import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
import base_region

def visualize_towers(region, results, r1, r2, r3):
    """
    Визуализирует регион и размещенные башни.
    
    Args:
        region: Экземпляр класса Region
        results: Словарь с центрами, который вернул find_all_centers_of_towers
        r1, r2, r3: Радиусы (должны совпадать с теми, что передавали в расчет)
    """
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 1. Отрисовка границ региона
    # Создаем полигон для matplotlib
    poly_patch = Polygon(region.coordinates, 
                         closed=True, 
                         fill=False, 
                         edgecolor='black', 
                         linewidth=2, 
                         label='Граница региона')
    ax.add_patch(poly_patch)
    
    # Чтобы график автоматически подстроился под размер региона
    (min_x, min_y), (max_x, max_y) = region.rectangle
    ax.set_xlim(min_x - r1, max_x + r1)
    ax.set_ylim(min_y - r1, max_y + r1)
    
    # 2. Функция для отрисовки слоя окружностей
    def plot_layer(centers, radius, color, label_prefix):
        if not centers:
            return
        
        # Рисуем окружности
        # Используем alpha (прозрачность), чтобы видеть наложения
        for i, (cx, cy) in enumerate(centers):
            # Метка только для первого элемента, чтобы легенда не дублировалась
            label = f"{label_prefix} (r={radius})" if i == 0 else None
            
            circle = Circle((cx, cy), radius, color=color, alpha=0.4, label=label)
            ax.add_patch(circle)
            
            # (Опционально) Рисуем точку в центре
            ax.plot(cx, cy, '.', color=color, markersize=1)

    # 3. Рисуем слои (от больших к маленьким, чтобы маленькие были поверх)
    # Предполагаем, что r1 > r2 > r3. Если нет, поменяйте порядок вызовов.
    
    # Слой R1 (Самые большие) - Синий
    if 'r1_centers' in results:
        plot_layer(results['r1_centers'], r1, 'blue', 'Layer 1')
        
    # Слой R2 (Средние) - Зеленый
    if 'r2_centers' in results:
        plot_layer(results['r2_centers'], r2, 'green', 'Layer 2')
        
    # Слой R3 (Маленькие) - Красный
    if 'r3_centers' in results:
        plot_layer(results['r3_centers'], r3, 'red', 'Layer 3')

    # 4. Настройки отображения
    ax.set_aspect('equal') # Важно! Чтобы круги были круглыми, а не овальными
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.title(f"Размещение башен: Всего {sum(len(v) for v in results.values())} шт.")
    plt.legend(loc='upper right')
    
    plt.show()

# --- ПРИМЕР ИСПОЛЬЗОВАНИЯ ---
if True:
    # 1. Создаем регион (например, сложный пятиугольник)
    coords = [(0, 0), (3000, 0), (3000, 2000), (1500, 3000), (0, 2000), (200, 1000), (1500,50)]
    region = base_region.Region(coords)

    # 2. Задаем параметры
    R1, R2, R3 = 40, 20, 4
    
    # 3. Считаем
    print("Вычисляем...")
    towers = region.find_all_centers_of_towers(R1, R2, R3, percent1=80, percent2=65, percent3=90)
    
    print(f"R1: {len(towers['r1_centers'])}, R2: {len(towers['r2_centers'])}, R3: {len(towers['r3_centers'])}")

    # 4. Рисуем
    visualize_towers(region, towers, R1, R2, R3)