from sub import Tower
from sub import parsing_base_station
from sub import base_region
import math
def read_and_validate_two_numbers(vvod:str) -> tuple:
    try:
        # Считываем строку и разбиваем на части
        user_input = vvod
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
    
def chose_rad():
    b_s:list[Tower] = parsing_base_station()
    for i in range(len(b_s)):
        print(f"N: {i}  Название вышки: {b_s[i].name}  Площадь: {b_s[i].square}")
    n1, n2, n3 = sorted(list(map(int, input("Введите номера вышек(через пробел): ").split())))
    R1, R2, R3 = math.sqrt(b_s[n1].square/math.pi),math.sqrt(b_s[n2].square/math.pi), math.sqrt(b_s[n3].square/math.pi)
    return R1, R2, R3


def main():
    b_s:list[Tower] = parsing_base_station()
    R1, R2, R3 = chose_rad()
    coords:list[tuple[float]] = []
    vvod = ""
    print("Введите координаты (x, y) минимум 3 или '-' для выхода")
    while len(coords) < 3 or vvod != '-':
        vvod = input("Введите координаты: ").strip()
        ans = read_and_validate_two_numbers(vvod)
        if ans:
            coords.append(ans)
        print(f"Введено координат {len(coords)}")
    region = base_region.Region(coords, R1, R2, R3)
    base_region.visualize_towers(region, R1, R2, R3)


main()