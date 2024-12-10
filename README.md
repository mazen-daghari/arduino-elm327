# arduino-elm327
describe this project This project is focused on real-time data acquisition and visualization of various car engine parameters using an ELM327 OBD-II adapter, an Arduino Uno, and a PyQt5 application with Matplotlib.

Components:
--
ELM327 OBD-II Adapter: This device interfaces with the car's OBD-II port to retrieve engine data such as RPM, speed, coolant temperature, and fuel level.

Arduino Uno: Acts as an intermediary to read data from the ELM327 adapter and send it to a computer via serial communication.

Python Script: A PyQt5 application that reads data from the Arduino, stores it in an SQLite database, and visualizes the data using Matplotlib.

Arduino Code:
--

Setup: Initializes serial communication with both the computer and the ELM327 adapter.

Loop: Continuously reads data from the ELM327 adapter and sends it to the computer if the data is valid. The data includes RPM, speed, coolant temperature, and fuel level.

Python Script:
--
Initialization:

Sets up the PyQt5 application window with labels for displaying the engine parameters and progress bars for gauge animations.

Initializes serial communication with the Arduino.

Creates an SQLite database to store the retrieved engine data.

Data Acquisition:
--

Reads data from the Arduino every second.

Updates the labels and progress bars with the new data.

Stores the data in the SQLite database.

Data Visualization:
--

Retrieves the latest engine data from the SQLite database.

Plots the historical data using Matplotlib within the PyQt5 application.

The x-axis is inverted to show the most recent data on the right.

Features:
--
Real-Time Data Display: Continuously updates and displays engine parameters such as RPM, speed, coolant temperature, and fuel level.

Gauge Animation: Uses progress bars to visually represent speed and torque.

Historical Data Plot: Visualizes the historical data of engine parameters using Matplotlib plots embedded within the PyQt5 application.

SQLite Database: Stores engine data for historical analysis and visualization.

Summary:
--
This project provides a comprehensive real-time monitoring system for car engine parameters using OBD-II data. The combination of Arduino for data acquisition and PyQt5 with Matplotlib for data visualization ensures an interactive and informative user interface. This setup can be used for diagnostic purposes, performance monitoring, or educational demonstrations.
Licence (MIT)
--

Contact : dagmazen@gmail.com
--
