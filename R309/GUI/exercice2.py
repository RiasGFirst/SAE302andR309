import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt

class TemperatureConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversion de Température")
        self.setMinimumSize(400, 200)
        self.setMaximumSize(500, 300)

        self.temp_label = QLabel("Température")
        self.temp_input = QLineEdit()
        self.unit_label = QLabel("°C")
        self.convert_button = QPushButton("Convertir")
        self.conversion_box = QComboBox()
        self.conversion_box.addItems(["°C -> K", "K -> °C"])
        self.result_label = QLabel("Conversion")
        self.result_output = QLineEdit()
        self.result_output.setEnabled(False)
        self.result_unit_label = QLabel("K")
        self.help_button = QPushButton("?")

        layout = QGridLayout()
        layout.addWidget(self.temp_label, 0, 0)
        layout.addWidget(self.temp_input, 0, 1)
        layout.addWidget(self.unit_label, 0, 2)
        layout.addWidget(self.convert_button, 1, 1, 1, 1)
        layout.addWidget(self.conversion_box, 1, 2)
        layout.addWidget(self.result_label, 2, 0)
        layout.addWidget(self.result_output, 2, 1)
        layout.addWidget(self.result_unit_label, 2, 2)
        layout.addWidget(self.help_button, 3, 2, alignment=Qt.AlignmentFlag.AlignRight)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.convert_button.clicked.connect(self.convert_temperature)
        self.conversion_box.currentIndexChanged.connect(self.update_units)
        self.help_button.clicked.connect(self.show_help)

    def update_units(self):
        if self.conversion_box.currentText() == "°C -> K":
            self.unit_label.setText("°C")
            self.result_unit_label.setText("K")
        else:
            self.unit_label.setText("K")
            self.result_unit_label.setText("°C")

    def convert_temperature(self):
        try:
            temp = float(self.temp_input.text())
            if self.conversion_box.currentText() == "°C -> K":
                if temp < -273.15:
                    raise ValueError("La température ne peut pas être inférieure à -273.15 °C.")
                result = temp + 273.15
            else:
                if temp < 0:
                    raise ValueError("La température ne peut pas être inférieure à 0 K.")
                result = temp - 273.15
            self.result_output.setText(f"{result:.2f}")
        except ValueError as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def show_help(self):
        QMessageBox.information(self, "Aide", "Permet de convertir un nombre soit de Kelvin vers Celsius, soit de Celsius vers Kelvin.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TemperatureConverter()
    window.show()
    sys.exit(app.exec())
