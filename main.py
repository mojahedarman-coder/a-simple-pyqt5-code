import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QComboBox
)
class AvgCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Calculator")
        self.resize(400, 250)
        lblName = QLabel("Name:")
        self.txtName = QLineEdit()
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(lblName)
        nameLayout.addWidget(self.txtName)
        lblWeight = QLabel("Weight:")
        self.txtWeight = QLineEdit()
        self.cmbWeight = QComboBox()
        self.cmbWeight.addItems(["kg", "g"])
        weightLayout = QHBoxLayout()
        weightLayout.addWidget(lblWeight)
        weightLayout.addWidget(self.txtWeight)
        weightLayout.addWidget(self.cmbWeight)
        lblHeight = QLabel("Height:")
        self.txtHeight = QLineEdit()
        self.cmbHeight = QComboBox()
        self.cmbHeight.addItems(["cm", "m"])
        heightLayout = QHBoxLayout()
        heightLayout.addWidget(lblHeight)
        heightLayout.addWidget(self.txtHeight)
        heightLayout.addWidget(self.cmbHeight)
        self.lblResult = QLabel("Average: -")
        btnCalc = QPushButton("Calculate & Save")
        btnCalc.clicked.connect(self.calculate_and_save)
        layout = QVBoxLayout()
        layout.addLayout(nameLayout)
        layout.addLayout(weightLayout)
        layout.addLayout(heightLayout)
        layout.addWidget(btnCalc)
        layout.addWidget(self.lblResult)
        self.setLayout(layout)
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL
            )
        """)
        self.conn.commit()
    def calculate_and_save(self):
        try:
            name = self.txtName.text().strip()
            weight = float(self.txtWeight.text())
            height = float(self.txtHeight.text())
            if self.cmbWeight.currentText() == "g":
                weight = weight / 1000.0
            if self.cmbHeight.currentText() == "m":
                height = height * 100.0
            avg = (weight + height) / 2
            self.lblResult.setText(f"Average (kg & cm): {avg:.2f}")
            if name:
                self.cursor.execute(
                    "INSERT INTO users (name, weight, height) VALUES (?, ?, ?)",
                    (name, weight, height)
                )
                self.conn.commit()
                print("Saved:", name, weight, height)  
            else:
                self.lblResult.setText(" Please enter a name!")
        except ValueError:
            self.lblResult.setText(" Please enter vaid numbers!")
    def closeEvent(self, event):
        self.conn.close()
        event.accept()
if __name__ == "__main__":
    app = QApplication([])
    win = AvgCalculator()
    win.show()
    app.exec_()


#do no copy right''''''''''''''''''''''''''''''''''''''''''''''''''