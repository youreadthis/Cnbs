from sub import Tower
from sub import base_region
import math
def read_and_validate_two_numbers(vvod:str) -> tuple:
    try:
        # Считываем строку и разбиваем на части
        user_input = input("Введите два числа через пробел: ").strip()
        parts = user_input.split()
        
        # Проверяем, что ровно два значения
        if len(parts) != 2:
            return False
        
        nums = []
        for part in parts:
            try:
                # Пробуем сначала как int, если не получится — как float
                if '.' in part:
                    nums.append(float(part))
                else:
                    nums.append(int(part))
            except ValueError:
                return False
        
        return tuple(nums)
    
    except Exception:
        return False
    

def main():
    b_s:list[Tower] = tower.parsing_base_station()
    R1, R2, R3 = math.sqrt(b_s[0].square/math.pi),math.sqrt(b_s[1].square/math.pi), math.sqrt(b_s[2].square/math.pi)
    coords:list[tuple[float]] = []
    vvod = ""
    print("Введите координаты (x, y) минимум 3 или '-' для выхода")
    while len(coords) < 3 or vvod == '-':
        vvod = input("Введите координаты: ").strip()
        ans = read_and_validate_two_numbers(vvod)
        if ans:
            coords.append(ans)
        print(f"Введено координат {len(coords)}")
    region = base_region.Region(coords, R1, R2, R3)
base_region.visualize_towers(region, R1, R2, R3)