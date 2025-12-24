import csv
import os
import sys
import pandas as pd


class Tower():
    def __init__(self, id_bs:int, name:str, square:float, frequency:int, type_antenna:str, range_of_handrover, standart):
        self.id_bs = int(id_bs)
        self.name = name
        self.square = float(square)
        self.frequency = int(frequency)
        self.type_antenna = type_antenna
        self.range_of_handrover = range_of_handrover
        self.standart = standart


def parsing_base_station(filename:str="Базовыестанции.xlsx"):
    script_dir = os.path.dirname(sys.argv[0])
    df = pd.read_excel(os.path.join(script_dir, filename), index_col=0)
    towers = []
    for row in df.itertuples(index=True, name='Row'):
        towers.append(Tower(row[0], row[1], str(row[2]).replace(",", "."), row[3], row[4], row[5], row[6]))
    return sorted(towers, key=lambda x: x.square, reverse=True) 

print(parsing_base_station()[2])

"""
def parsing_base_station(filename:str="Базовыестанции.csv"):
    script_dir = os.path.dirname(sys.argv[0])

    with open(os.path.join(script_dir, filename), encoding = "UTF-8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)                                                                                        #пропускаем заголовок
        towers = []
        for row in reader:
            towers.append(Tower(row[0], row[1], row[2].replace(",", "."), row[3], row[4], row[5], row[6]))  #заносим всё в массив для работы
        return sorted(towers, key=lambda x: x.square, reverse=True)                                                       #возращаем отсортированный по площаде покрытия
"""