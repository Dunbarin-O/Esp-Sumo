# Esp-Sumo

ESP32 General-Purpose Robotics Development Kit in its early stages 

A low-cost, open-source motion control board for ESP32-based robots.

High-performance motor driver boards are often tailored to a single use case or carry a steep price tag. This project provides a low-cost, all-in-one hardware foundation designed to drive small-scale, high-precision mobile robots without requiring extra breakout boards or expensive driver shields.

Supported Kinematics & Applications:

Mini Sumo Robots: Integrated motor control and gyro feedback for rapid opponent tracking and high-torque maneuvers.

Inverted Pendulum / Self-Balancing: Direct IMU integration for low-latency loop control and pitch stabilization.

Heading-Corrected Rovers: Closed-loop yaw monitoring for straight-line differential driving and precise turn angles.

### V1 Key Features

* **Dual High-Current Motor Drivers:** Two TI DRV8870 ICs providing independent PWM speed and direction control, supporting up to 3.6 A peak output per channel.
* **Onboard Motion Sensing:** MPU-6050 6-axis gyroscope and accelerometer connected via I2C for pitch, roll, and yaw feedback.
* **Integrated Diagnostic Display Header:** Dedicated 4-pin I2C header positioned for direct SSD1306 OLED screens (128x64 or 128x32).
* **User Input Controls:** 3 onboard tactical pushbuttons mapped to ESP32 GPIOs for mode selection, calibration, and menu navigation.
* **Built-in Servo Mount & Header:** Dedicated 3-pin PWM servo header (VCC, GND, Signal) with mounting holes integrated directly into the PCB outline (ideal for mini sumo flippers or sensor sweepers).
* **Optimized Power Architecture:** Designed for 2S (7.4V) LiPo input with onboard voltage regulation to safely power the ESP32, OLED, and logic components.
* **Expansion I/O:** Exposed GPIO headers for IR edge sensors, line detectors, or custom sensors.
* **100% Open-Source Hardware:** Full KiCad project files, schematics, PCB layouts, BOM, and manufacturing outputs (Gerbers/CPL) included.
  
  
 <img width="1763" height="766" alt="Top+null+SMT026081362981" src="https://github.com/user-attachments/assets/32ad1a9a-bd80-4e35-ad53-a593bfcab190" />

 ## Engineering Design Process & Iterations
## Power Design Choice: Dual Buck Converters vs. Buck + LDO

### First Attempt: Two-Stage Buck Regulation
My initial plan was to use two buck converters in series to drop the 7.4V (2S LiPo) battery voltage down to 5V, and then down to 3.3V for the system ICs to maximize energy efficiency.
<img width="1337" height="504" alt="Screenshot 2026-07-03 165300" src="https://github.com/user-attachments/assets/1924f090-6275-4f11-8a7b-51b6312f975c" />
* **Buck Stage 1 (7.4V → 5V):** Powers 5V peripherals (servos/sensors) and feeds the second regulator stage.
  * *Space for Stage 1 Schematic / Layout Image:*
  * 

* **Buck Stage 2 (5V → 3.3V):** Steps down 5V to power the ESP32, MPU-6050, and SSD1306 OLED screen.
  * *Space for Stage 2 Schematic / Layout Image:*
  * 

**The Problem:** Each buck converter requires its own dedicated supporting passives (inductors, filter capacitors, and feedback resistors). Running two switching stages took up too much PCB footprint, added significant routing complexity, and increased the overall Bill of Materials (BOM) cost.

---

### Final Solution: Single Buck + 3.3V LDO Regulator
I simplified the power tree by keeping a single buck converter for the 5V rail and replacing the second buck stage with a straightforward 3.3V Low-Dropout (LDO) linear regulator.
