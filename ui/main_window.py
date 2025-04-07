from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QLineEdit,
    QListWidget,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
)
from PyQt6.QtCore import Qt

from models.car import CAuto
from models.garage import CGarage


class MainWindow(QMainWindow):
    def __init__(self, garage: CGarage):
        super().__init__()

        self.garage = garage

        self.central_widget = QWidget()
        self.setMinimumSize(700, 500)
        self.setWindowTitle("Гараж автомобилей")

        self.main_layout = QVBoxLayout()

        self.info_layout = QHBoxLayout()

        self.draw_car_info_layout()
        self.draw_garage_info_layout()

        self.info_layout.addLayout(self.car_info_layout)
        self.info_layout.addLayout(self.garage_info_layout)

        self.main_layout.addLayout(self.info_layout)
        self.save_button = QPushButton("Сохранить в файл")
        self.save_button.setMaximumWidth(180)
        self.save_button.setMinimumHeight(40)
        self.load_button = QPushButton("Загрузить из файла")
        self.load_button.setMaximumWidth(180)
        self.load_button.setMinimumHeight(40)
        self.bottom_buttons_layout = QHBoxLayout()
        self.bottom_buttons_layout.addWidget(self.save_button)
        self.bottom_buttons_layout.addWidget(self.load_button)

        self.main_layout.addLayout(self.bottom_buttons_layout)

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.add_car_button.clicked.connect(self.add_car)
        self.sort_by_fio_btn.clicked.connect(self.sort_cars)  # Подключаем сортировку
        self.save_button.clicked.connect(self.save_to_file)  # Подключаем сохранение
        self.load_button.clicked.connect(self.load_from_file)  # Подключаем загрузку

    def draw_car_info_layout(self):
        """Функция для отрисовки layout "Ввод данных" """
        self.car_info_layout = QVBoxLayout()
        self.car_info_label = QLabel("Ввод данных")
        self.car_info_layout.addWidget(self.car_info_label)

        self.car_info_v_layout = QVBoxLayout()

        self.license_plate_layout = QHBoxLayout()
        self.license_plate_label = QLabel("Госномер")
        self.license_plate_input = QLineEdit()
        self.license_plate_input.setMaximumWidth(200)
        self.license_plate_layout.addWidget(self.license_plate_label)
        self.license_plate_layout.addWidget(self.license_plate_input)

        self.model_layout = QHBoxLayout()
        self.model_label = QLabel("Модель")
        self.model_input = QLineEdit()
        self.model_input.setMaximumWidth(200)
        self.model_layout.addWidget(self.model_label)
        self.model_layout.addWidget(self.model_input)

        self.color_layout = QHBoxLayout()
        self.color_label = QLabel("Цвет")
        self.color_input = QLineEdit()
        self.color_input.setMaximumWidth(200)
        self.color_layout.addWidget(self.color_label)
        self.color_layout.addWidget(self.color_input)

        self.owner_layout = QHBoxLayout()
        self.owner_label = QLabel("ФИО")
        self.owner_input = QLineEdit()
        self.owner_input.setMaximumWidth(200)
        self.owner_layout.addWidget(self.owner_label)
        self.owner_layout.addWidget(self.owner_input)

        self.car_info_v_layout.addLayout(self.license_plate_layout)
        self.car_info_v_layout.addLayout(self.model_layout)
        self.car_info_v_layout.addLayout(self.color_layout)
        self.car_info_v_layout.addLayout(self.owner_layout)

        spacer_top = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.car_info_layout.addItem(spacer_top)

        self.car_info_layout.addLayout(self.car_info_v_layout)

        spacer_bottom = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        self.car_info_layout.addItem(spacer_bottom)

        self.add_car_button = QPushButton("Добавить авто")
        self.add_car_button.setMinimumWidth(200)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_car_button)
        button_layout.setAlignment(self.add_car_button, Qt.AlignmentFlag.AlignHCenter)
        self.car_info_layout.addLayout(button_layout)

    def draw_garage_info_layout(self):
        """Функция для отрисовки layout "Данные гаража" """
        self.garage_info_layout = QVBoxLayout()
        self.garage_info_layout.addWidget(QLabel("Данные гаража"))

        self.cars_list = QListWidget()
        self.garage_info_layout.addWidget(self.cars_list)

        self.sort_by_fio_btn = QPushButton("Сортировка по ФИО")
        self.garage_info_layout.addWidget(self.sort_by_fio_btn)

    def draw_info_garage_layout(self):
        self.cars_list.clear()
        for car in self.garage.cautos:
            self.cars_list.addItem(str(car))

    def add_car(self):
        """Метод для добавления автомобиля в гараж"""
        license_plate = self.license_plate_input.text()
        model = self.model_input.text()
        color = self.color_input.text()
        owner = self.owner_input.text()

        new_car = CAuto(
            license_plate=license_plate,
            model=model,
            color=color,
            owner=owner,
        )

        if self.garage.add_car(new_car):
            self.draw_info_garage_layout()
            self.clear_inputs()
        else:
            self.show_error_message(
                "Гараж полон! Невозможно добавить новый автомобиль."
            )

    def sort_cars(self):
        """Метод для сортировки автомобилей по ФИО"""
        self.garage.sort_by_owner()
        self.draw_info_garage_layout()

    def save_to_file(self):
        """Метод для сохранения данных в файл"""
        self.garage.save_to_file("car_garage_data.xlsx")
        print("Данные сохранены в файл.")

    def load_from_file(self):
        """Метод для загрузки данных из файла"""
        self.garage.load_from_file("car_garage_data.xlsx")
        self.draw_info_garage_layout()

    def clear_inputs(self):
        """Метод для очист ки полей ввода"""
        self.license_plate_input.clear()
        self.model_input.clear()
        self.color_input.clear()
        self.owner_input.clear()

    from PyQt6.QtWidgets import QMessageBox

    def show_error_message(self, message):
        """Функция для отображения сообщения об ошибке"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText("Ошибка")
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle("Ошибка")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
