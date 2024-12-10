import sys
import serial
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMainWindow, QPushButton, QProgressBar, \
    QHBoxLayout
from PyQt5.QtCore import QTimer


class CarDataApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.arduino = serial.Serial('COM3', 9600)  # Adjust COM port as needed
        self.conn = sqlite3.connect('engine_data.db')
        self.create_table()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every 1 second

    def initUI(self):
        self.setWindowTitle('Engine Data Visualization')

        # Labels for sensor data
        self.rpm_label = QLabel('RPM: N/A', self)
        self.speed_label = QLabel('Speed: N/A', self)
        self.temp_label = QLabel('Coolant Temp: N/A', self)
        self.fuel_label = QLabel('Fuel Level: N/A', self)

        # Progress bars for gauge animation
        self.speed_gauge = QProgressBar(self)
        self.speed_gauge.setMaximum(200)  # Assuming max speed is 200 km/h
        self.torque_gauge = QProgressBar(self)
        self.torque_gauge.setMaximum(400)  # Assuming max torque is 400 Nm

        # Plot
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.rpm_label)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.temp_label)
        layout.addWidget(self.fuel_label)

        gauge_layout = QHBoxLayout()
        gauge_layout.addWidget(QLabel('Speed:'))
        gauge_layout.addWidget(self.speed_gauge)
        gauge_layout.addWidget(QLabel('Torque:'))
        gauge_layout.addWidget(self.torque_gauge)

        layout.addLayout(gauge_layout)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.show()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS engine_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            rpm FLOAT,
                            speed FLOAT,
                            coolant_temp FLOAT,
                            fuel_level FLOAT,
                            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def update_data(self):
        if self.arduino.in_waiting:
            data = self.arduino.readline().decode('utf-8').strip()
            print(f"Arduino Data: {data}")
            try:
                rpm, speed, coolant_temp, fuel_level = map(float, data.split(','))
                self.rpm_label.setText(f'RPM: {rpm}')
                self.speed_label.setText(f'Speed: {speed} km/h')
                self.temp_label.setText(f'Coolant Temp: {coolant_temp} °C')
                self.fuel_label.setText(f'Fuel Level: {fuel_level}%')
                self.speed_gauge.setValue(int(speed))
                self.torque_gauge.setValue(int(rpm / 2))  # Simplified torque calculation

                self.store_data(rpm, speed, coolant_temp, fuel_level)
                self.update_plot()
            except ValueError:
                print("Error parsing data")

    def store_data(self, rpm, speed, coolant_temp, fuel_level):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO engine_data (rpm, speed, coolant_temp, fuel_level) VALUES (?, ?, ?, ?)',
                       (rpm, speed, coolant_temp, fuel_level))
        self.conn.commit()

    def update_plot(self):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT timestamp, rpm, speed, coolant_temp, fuel_level FROM engine_data ORDER BY id DESC LIMIT 20')
        rows = cursor.fetchall()

        self.timestamps = [row[0] for row in rows]
        self.rpm_values = [row[1] for row in rows]
        self.speed_values = [row[2] for row in rows]
        self.temp_values = [row[3] for row in rows]
        self.fuel_values = [row[4] for row in rows]

        self.ax.clear()
        self.ax.plot(self.timestamps, self.rpm_values, label='RPM')
        self.ax.plot(self.timestamps, self.speed_values, label='Speed')
        self.ax.plot(self.timestamps, self.temp_values, label='Coolant Temp')
        self.ax.plot(self.timestamps, self.fuel_values, label='Fuel Level')
        self.ax.set_xlabel('Timestamp')
        self.ax.set_ylabel('Value')
        self.ax.set_title('Engine Data History')
        self.ax.legend()
        self.ax.tick_params(axis='x', rotation=45)
        self.ax.invert_xaxis()  # Invert the x-axis direction
        self.canvas.draw()

    def closeEvent(self, event):
        self.arduino.close()
        self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CarDataApp()
    sys.exit(app.exec())
