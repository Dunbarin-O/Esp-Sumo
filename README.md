# Esp-Sumo
## Design Story

I started this project because I wanted to build a mini-sumo robot. I quickly found myself relying on a mess of separate motor drivers, sensors, regulators, and breakout boards, so I decided to design a single, integrated PCB built specifically around the robot's hardware requirements.

One of my first major challenges was the power architecture. I initially planned to use two buck converters in series to drop the 7.4 V battery supply to 5 V, and then down to 3.3 V. As I developed the PCB layout, I realized the second converter added significant component count, trace routing complexity, cost, and board space for a relatively small efficiency benefit. I revised the design to use a single 5 V buck converter followed by a 3.3 V LDO linear regulator.
After completing the V1 layout, I had the board reviewed by another hardware designer. That review exposed critical real-world edge cases I had overlooked, including battery reverse-polarity protection, transient motor current demands, USB-C ESD protection, and rail isolation. I incorporated this feedback directly into the design to overhaul the power architecture and significantly improve board protection and reliability.

The most valuable part of this project wasn't just getting the first design to pass DRC. It was learning that a circuit can look completely correct in a schematic capture tool while real-world implementation challenges lie just beneath the surface.

V1 is not the final answer—it is a functional iteration shaped by design decisions, mistakes, peer feedback, and continuous improvement.

---

### Read Further

For detailed technical implementation, schematics, component calculations, PCB layout files, and manufacturing outputs, explore the rest of the repository:

* **`PCB/`** – Native KiCad design files:
  * `Mini_sumo.kicad_sch` – Schematic capture files.
  * `Mini_sumo.kicad_pcb` – PCB trace routing and board layout.
* **`Hardware/`** – Assembly and manufacturing outputs:
  * `Mini_sumo.zip` – Production Gerber & drill files for board fabrication.
  * `combined_bom.csv` – Bill of Materials listing all active and passive components.
  * `positions.csv` – Pick-and-Place (CPL / Centroid) file for automated SMT assembly.
Project is in
 its early stages 

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


 ## ESP32-S3 GPIO Pin Mapping

| GPIO Pin | Label / Connection | Subsystem | Function / Description |
| :--- | :--- | :--- | :--- |
| **GPIO1** | `D1` | User UI | Pushbutton SW4 (Input w/ Pull-up) |
| **GPIO2** | `D2` | User UI | Pushbutton SW5 (Input w/ Pull-up) |
| **GPIO3** | `D3` | User UI | Pushbutton SW6 (Input w/ Pull-up) |
| **GPIO4** | `D4` | IR Sensors | Front Left IR Sensor Signal (`J6`) |
| **GPIO5** | `D5` | IR Sensors | Front Right IR Sensor Signal (`J8`) |
| **GPIO6** | `D6` | IR Sensors | Edge Left IR Floor Sensor Signal (`J9`) |
| **GPIO7** | `D7` | IR Sensors | Edge Right IR Floor Sensor Signal (`J10`) |
| **GPIO8** | `D8` | User UI | Pushbutton SW7 (Input w/ Pull-up) |
| **GPIO9** | `D9` | Motor Driver 1 | `IN1` Control Pin (U7 DRV8870 - Left Motor PWM) |
| **GPIO10** | `D10` | Motor Driver 1 | `IN2` Control Pin (U7 DRV8870 - Left Motor Dir) |
| **GPIO11** | `D11` | Servo | PWM Output Signal Header (`J11`) |
| **GPIO12** | `D12` | Status LED | User Indicator LED D6 |
| **GPIO13** | `D13` | Motor Driver 2 | `IN1` Control Pin (U8 DRV8870 - Right Motor PWM) |
| **GPIO14** | `D14` | Motor Driver 2 | `IN2` Control Pin (U8 DRV8870 - Right Motor Dir) |
| **GPIO15** | `D15` | I2C Bus | `SCL` Serial Clock (Shared: MPU-6050 & SSD1306 OLED) |
| **GPIO16** | `D16` | I2C Bus | `SDA` Serial Data (Shared: MPU-6050 & SSD1306 OLED) |
| **GPIO17** | `D17` | Power Protection | UV LO Alert Signal (TPS3702 Battery Supervisor) |
| **GPIO19** | `USB_D-` | USB Interface | Native USB D- (Type-C Flashing / Serial) |
| **GPIO20** | `USB_D+` | USB Interface | Native USB D+ (Type-C Flashing / Serial) |
| **EN** | `EN` | System | Reset Button (SW2) / Chip Enable |
| **IO0** | `IO0` | System | Boot Mode Selection Button (SW3) |

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
### Front-End Power Protection Circuit

* **P-Channel Reverse Polarity Protection (AO3401A):** Uses a low-$R_{DS(on)}$ P-FET (Q1) to block reverse voltage if the battery is plugged in backward, with a 10V Zener diode (D1) protecting $V_{GS}$ against voltage transients.
* **Overcurrent Safety (F1):** In-line fuse provides hard fault protection against high-current shorts.
* **Active Under-Voltage Monitoring (TPS3702):** Samples battery rail via resistor divider (R21/R22) and outputs a low-battery alert signal (D17) to the ESP32 to prevent over-discharging 2S LiPo cells.
* <img width="1071" height="441" alt="image" src="https://github.com/user-attachments/assets/e562dbd5-3411-494c-a677-0f14db7d65c9" />
## Picking a driver IC : DRV8220 vs. DRV8870

When designing the motor stage, I needed driver chips capable of handling high startup currents and heavy mechanical loads without overheating or shutting down mid-operation.

### First Attempt: Dual DRV8220 (Compact, but Limited)

<img width="1029" height="385" alt="image" src="https://github.com/user-attachments/assets/ad9ed73f-566d-4e69-b2ab-d1ca69d7d7fc" />

My initial plan was to use two compact DRV8220 drivers in the DRL package, but bench analysis revealed major bottlenecks:
* **Thermal Overheating:** High internal resistance ($R_{DS(on)} \approx 1\,\Omega$) and the lack of a thermal pad ($152\,^{\circ}\text{C/W}$ thermal resistance) caused severe heat buildup, limiting continuous current to $< 0.9\text{A}$.
* **Hard Shutdowns:** The $1.76\text{A}$ overcurrent protection (OCP) cuts power entirely during high loads or stalls, stopping the robot mid-operation instead of sustaining torque.
* **Difficult Hand-Soldering:** The tiny leadless DRL package has contacts tucked under the chip, making it extremely difficult to solder, inspect, or rework with a standard soldering iron without bridging.
* **No Built-in Current Sensing:** Lacks a dedicated `ISEN` pin, preventing the use of external sense resistors to measure or actively control motor current.
* **Startup Voltage Glitches & Efficiency Loss:** Logic inputs easily float during microcontroller boot, causing motor twitches. High internal resistance also wastes battery voltage as heat before it reaches the motors.

---

### Final Solution: Dual DRV8870 (High Power & Current Chopping)

<img width="1298" height="437" alt="image" src="https://github.com/user-attachments/assets/195faf15-e0a2-4435-b9f5-aba8458ab8ba" />

I upgraded to two DRV8870 drivers featuring an exposed PowerPAD package and external sense resistors:
* **Hand-Soldering Friendly:** The larger HSOP-8 package with exposed leads **very** important for reliable hand soldering(ended up having it assembled by jcl).
* **Superior Thermals:** Lower internal resistance ($450\,\text{m}\Omega$) paired with a copper thermal pad handles up to $3.6\text{A}$ peak current safely.
* <img width="413" height="630" alt="image" src="https://github.com/user-attachments/assets/e5b2cec0-4098-48ca-ac25-e980a780fd31" />

* **Smart Current Chopping ($I_{\text{TRIP}}$):** Instead of shutting down completely during a stall, the driver uses parallel sense resistors ($R17 - R20$) totaling $0.2\,\Omega$ to limit current automatically:
  $$I_{\text{TRIP}} = \frac{V_{\text{REF}}}{10 \times R_{\text{ISEN}}} = \frac{3.3\text{V}}{10 \times 0.2\,\Omega} = 1.65\text{A}$$
  When pushing heavy loads, the chip acts like an automatic safety valve—"chopping" current to maintain maximum pushing force without tripping power failures or browning out the battery rail.
* **Brush Noise Suppression:** Added $0.1\,\mu\text{F}$ ceramic capacitors ($C2, C5$) directly across the motor terminals to absorb high-frequency electrical noise before it can interfere with the I2C gyroscope or IR floor sensors.

---
