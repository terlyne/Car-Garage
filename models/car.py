class CAuto:
    def __init__(self, license_plate, model, color, owner):
        self.license_plate = license_plate
        self.model = model
        self.color = color
        self.owner = owner

    def __str__(self):
        return f"{self.model}; {self.license_plate}; {self.color}; {self.owner}"
