# Esp-Sumo

ESP32 General-Purpose Robotics Development Kit in its early stages 

A low-cost, open-source motion control board for ESP32-based robots.
High-performance motor boards are usually expensive or made for just one job. This project is a low-cost, all-in-one board that lets you build precise small robots without needing extra shields or breakout boards.

Applications:

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

**The Problem:** Each buck converter requires its own dedicated supporting passives (inductors, filter capacitors, and feedback resistors). Running two switching stages took up too much PCB footprint, added significant routing complexity, and increased the overall Bill of Materials (BOM) cost.

---

### Final Solution: Single Buck + 3.3V LDO Regulator
I simplified the power tree by keeping a single buck converter for the 5V rail and replacing the second buck stage with a straightforward 3.3V Low-Dropout (LDO) linear regulator.
<img width="662" height="161" alt="image" src="https://github.com/user-attachments/assets/78cd9888-940a-4b8b-9529-73642ea8acf9" /> <img width="493" height="248" alt="image" src="https://github.com/user-attachments/assets/36244862-ba0c-40d4-b81a-cdb78638a8ed" />

## Peer Design Review: Power & Protection Enhancements

Following the V1 layout release, a community hardware review identified several critical power delivery and protection improvements to increase reliability:

### 1. Battery Input & System Protection
* **Circuit Protection:** The design was solid, but it lacked input safety. Adding an in-line fuse and a reverse-polarity protection circuit (e.g., a P-channel MOSFET or ideal diode) on the 2S LiPo rail is essential to prevent permanent board failure from accidental battery misplugs during quick pit stops.
* **Input Bulk Decoupling:** The 10 µF input capacitor ($C_{\text{IN}1}$) on the buck regulator followed basic bench-supply reference designs. However, long battery wire harnesses introduce parasitic inductance. Upgrading $C_{\text{IN}1}$ to a **47 µF ceramic + 10 µF ceramic paired with a 100 µF electrolytic** lowers High-Frequency ESR and prevents sudden motor current draw from sagging the shared battery rail and browning out the ESP32.

### 2. Switching Regulator Duty Cycle & Stability
* At 7.4 V nominal input, the 5 V buck converter operates near a **0.67 duty cycle** (higher as the LiPo drains). Because the regulator uses peak current mode with fixed internal compensation, switch-node signal integrity must be verified under full load with an oscilloscope to ensure stable loop performance across the entire discharge curve.

### 3. ESD & Port Safety
* Added dedicated **ESD protection IC (USBLC6-2SC6)** on the USB-C $V_{\text{BUS}}$ and $D+/D-$ lines to guard the ESP32 against static discharge during  flashing
* <img width="1271" height="834" alt="image" src="https://github.com/user-attachments/assets/a236f976-6519-4381-b47c-92eb4bb5672a" />



### Power Isolation: OR-ing Diode Selection

To prevent backfeeding power between the USB-C 5V supply and the onboard 5V buck converter when both are plugged in simultaneously, I implemented a simple diode OR-ing power path
combining the 2 into 5V Safe and feeding it into ldo.

* **Why Schottky over Silicon Diodes:** Standard silicon rectifiers cause a ~0.7V drop, which would reduce the 5.0V USB rail down to 4.3V—dangerously close to the ESP32's minimum operating threshold and brownout limit.
* **Low Forward Voltage ($V_F$):** Using Schottky diodes keeps the voltage drop under ~0.3V, maintaining a stable supply rail (~4.7V+) for logic components and sensors while safely preventing reverse current flow into your computer's USB port or the buck regulator since a lipo battery is used trying to charge over usb withour any charging circuits could be dangerous.
  <img width="651" height="521" alt="image" src="https://github.com/user-attachments/assets/5f31de6a-ffd7-4cc3-ada9-85864d5ca93f" />
