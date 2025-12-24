import csv


class Tower():
    def __init__(self, id_bs:int, name:str, square:float, frequency:int, type_antenna:str, range_of_handrover, standart):
        self.id_bs = int(id_bs)
        self.name = name
        self.square = float(square)
        self.frequency = int(frequency)
        self.type_antenna = type_antenna
        self.range_of_handrover = range_of_handrover
        self.standart = standart
        

def read_csv(filename:str):
    with open(filename, encoding = "UTF-8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)                                     #пропускаем заголовки
        towers = []
        for row in reader:
            towers.append(Tower(row[0], row[1], row[2].replace(",", "."), row[3], row[4], row[5], row[6]))
        return sorted(towers, key=lambda x: x.square)

towers = read_csv("C:/Users/Владислав/Desktop/Проект/Cnbs/app/sub/Базовыестанции.csv")
