import csv


#class Tower(self, id_bs:int, name:str, square:float, frequency:int, type_antenna:str, range_of_handrover, standart):

def read_csv(filename:str):
    with open(filename, encoding = "UTF-8") as file:
        reader = csv.reader(file)
        next(reader)                                    #пропускаем заголовки
        #for row in reader:

read_csv("Базовые_станции.csv")