import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtCore import QCoreApplication


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Une première fenêtre")

        self.setMinimumSize(300, 200)
        self.setMaximumSize(400, 300)

        self.label = QLabel("Saisir votre nom")
        self.text_input = QLineEdit()
        self.message_label = QLabel("")

        self.ok_button = QPushButton("Ok")
        self.quit_button = QPushButton("Quitter")

        self.ok_button.clicked.connect(self.display_message)
        self.quit_button.clicked.connect(self.quit_application)

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0, 1, 2)
        layout.addWidget(self.text_input, 1, 0, 1, 2)
        layout.addWidget(self.ok_button, 2, 0, 1, 2)
        layout.addWidget(self.quit_button, 4, 0, 1, 2)
        layout.addWidget(self.message_label, 3, 0, 1, 2)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def display_message(self):
        name = self.text_input.text()
        self.message_label.setText(f"Bonjour {name}")

    def quit_application(self):
        QCoreApplication.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
