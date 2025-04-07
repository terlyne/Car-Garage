import openpyxl
from models.car import CAuto
import sys


class CGarage:
    def __init__(self, max_auto):
        self.cautos = []
        self.next_id = 1
        self.max_auto = max_auto

    def add_car(self, car):
        if len(self.cautos) < self.max_auto:
            car.id = self.next_id
            self.cautos.append(car)
            self.next_id += 1
            return True
        return False

    def save_to_file(self, filename):
        try:
            try:
                wb = openpyxl.load_workbook(filename)
                ws = wb.active
            except FileNotFoundError:
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = "Car Garage Data"
                headers = [
                    "ID",
                    "License Plate",
                    "Model",
                    "Color",
                    "Owner",
                    "Description",
                ]
                ws.append(headers)

            for car in self.cautos:
                ws.append(
                    [
                        car.id,
                        car.license_plate,
                        car.model,
                        car.color,
                        car.owner,
                        car.description,
                    ]
                )

            wb.save(filename)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")
            return False

    def load_from_file(self, filename):
        try:
            wb = openpyxl.load_workbook(filename)
            ws = wb.active

            for row in ws.iter_rows(min_row=2, values_only=True):
                license_plate, model, color, owner = row[1:5]
                car = CAuto(license_plate, model, color, owner)
                self.add_car(car)
        except FileNotFoundError:
            print(f"Файла {filename} не существует!")
            sys.exit()

    def sort_by_owner(self):
        self.cautos.sort(key=lambda car: car.owner)
