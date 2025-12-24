class Region:
    def __init__(self, coordinates):
        if not coordinates or len(coordinates) < 3:
            raise ValueError("less than 3 coordinates provided")
        self.coordinates = coordinates
        self.area = self.calculate_area()
        self.rectangle = self.calculate_rectangle()
    def calculate_area(self):
        coords = self.coordinates
        n = len(self.coordinates) 
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += coords[i][0] * coords[j][1]
            area -= coords[j][0] * coords[i][1]
        return abs(area) / 2.0
    def calculate_rectangle(self):
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