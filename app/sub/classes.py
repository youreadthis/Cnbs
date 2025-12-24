class region:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.area = self.calculate_area()
        self.rectangle = self.calculate_rectangle()