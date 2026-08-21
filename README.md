# Esp-Sumo
## Design Story

Building a custom mini-sumo robot sounded straightforward until i tried try wiring one together. Early in the process, I realized that relying on a disconnected stack of off-the-shelf motor drivers, sensor breakout boards, and external voltage regulators created a fragile spiderweb of jumper wires that easily disconnected during testing also pretty ugly, very ugly. To build something that stayed together, I decided to design a single, custom printed circuit board (PCB) to integrate every subsystem onto one reliable platform.

My first major challenge was in designing the power architecture. I initially planned to use two high-efficiency switching buck converters in series one to drop the 7.4V battery down to 5V, and a second to drop it further to 3.3V. While it looked ideal in block diagrams, routing the PCB layout showed that the second converter added significant cost, component count, and board space for a negligible boost in efficiency. I pivoted to a hybrid design: a single switching converter for high-draw 5V motor and servo demands, paired with a lightweight linear regulator for sensitive 3.3V logic. This trade-off taught me balancing performance, cost, and simplicity

Seeking external feedback proved equally transformative. After completing my first schematic draft, I had another hardware designer review my work. That peer review exposed critical real-world edge cases I had completely overlooked. To prevent catastrophic shorts during rapid battery swaps, I incorporated a low-resistance P-channel MOSFET switch for instant reverse-polarity protection. I also completely re-evaluated my motor drivers. My initial plan used tiny DRV8220 drivers to keep the board compact, but testing showed their high internal resistance caused severe overheating, and their strict overcurrent protection completely shut off power during motor stalls. I upgraded to dual DRV8870 drivers featuring active "current chopping." Instead of shutting down when pushing against an obstacle, the new drivers automatically throttle current to deliver maximum safe pushing force without crashing the battery rail.

When the fabricated boards arrived, the ESP32-S3 microcontroller powered on and flashed code over USB smoothly on the first try. However, physical hardware quickly revealed real-world oversights that software DRC checks could not predict. I had selected incorrect physical footprints for my pin headers in KiCad, meaning the OLED display could not plug directly into the board and required manual jumper wire reworks. Furthermore, placing every component on a single side made the overall PCB footprint far too large for a compact mini-sumo chassis.

This project proved that a circuit can look entirely correct in a schematic editor while real-world physics, ergonomics, and physical dimensions tell a different story. Version 1 was not perfect, but it served as a functional masterclass in circuit protection, component selection, and practical board layout. For Version 2, I am transitioning to a double-sided component layout to cut the board size in half while correcting all header footprints for a clean, plug-and-play assembly.
---

### Read Further

For detailed technical implementation, schematics, component calculations, PCB layout files, and manufacturing outputs, explore the rest of the repository which is still a wip :

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


| ESP32-S3 GPIO | Schematic net | Actually connected to             |
| ------------: | ------------- | --------------------------------- |
|     **GPIO0** | I00           | Boot button **SW3** + 10k pull-up |
|     **GPIO1** | D1            | **Right IR sensor** J5            |
|     **GPIO2** | D2            | **Left IR sensor** J6             |
|     **GPIO3** | D3            | **SW4 button**                    |
|     **GPIO4** | D4            | **Left edge sensor** J8           |
|     **GPIO5** | D5            | **Right edge sensor** J10         |
|     **GPIO6** | D6            | **SW5 button**                    |
|     **GPIO7** | D7            | **SW6 button**                    |
|     **GPIO8** | D8            | **Left motor driver IN2**         |
|     **GPIO9** | D9            | **Left motor driver IN1**         |
|    **GPIO10** | D10           | **J17 breakout pin 1**            |
|    **GPIO11** | D11           | **Gyro SCL**                      |
|    **GPIO12** | D12           | **Gyro SDA**                      |
|    **GPIO13** | D14           | **Right motor driver IN2**        |
|    **GPIO14** | D13           | **Right motor driver IN1**        |
|    **GPIO15** | D15           | **J15 / right motor?**            |
|    **GPIO16** | D16           | **J11 servo?**                    |
|    **GPIO17** | D17           | **J17 software uvlo**             |
|    **GPIO18** | D18           | **Servo signal**                  |
|    **GPIO19** | USB_D−        | **USB D−**                        |
|    **GPIO20** | USB_D+        | **USB D+**                        |
|    **GPIO21** | —             | **Unused**                        |

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
  When pushing heavy loads, the chip acts like an automatic safety valve "chopping" current to maintain pushing force without tripping power failures or browning out the battery rail.
* **Brush Noise Suppression:** Added $0.1\,\mu\text{F}$ ceramic capacitors ($C2, C5$) directly across the motor terminals to absorb high-frequency electrical noise before it can interfere with the I2C gyroscope or IR floor sensors.

---
## ESP32-S3 Core
i chose the s3 because of its native usb to uart and it simplicity to set up and get working keeping parts cost low
<img width="1291" height="595" alt="image" src="https://github.com/user-attachments/assets/fe2f7381-8d12-4647-804b-77c66de9765d" />


This section covers the core ESP32-S3 microcontroller, its power filtering, boot/reset logic, user UI, and external expansion headers.

### Core Microcontroller (ESP32-S3-WROOM-1)
* **Brain of the Robot:** Handles sensor polling, motor control loops, and peripheral interfaces.
* **Power Decoupling ($C14, C15$):** Placed $0.1\,\mu\text{F}$ and $22\,\mu\text{F}$ capacitors close to the $+3.3\text{V}$ power pin (`Pin 2`) to filter out high-frequency noise and prevent voltage dips when the chip spikes in power draw during wireless tasks or bootup.

---

### Boot Logic & System Buttons
* **Reset Circuit (`SW2`, `EN`):** Pressing `SW2` pulls the `EN` pin to ground to manually restart the microcontroller. 
  * **Debouncing & RC Delay ($R9, C9, C13, R13$):** An RC circuit ($10\,\text{k}\Omega$ pull-up + $1\,\mu\text{F}$ cap) keeps `EN` stable at $+3.3\text{V}$ and prevents electrical noise from causing random micro-resets.
* **Boot Button (`SW3`, `IO0`):** Pressing `SW3` grounds `IO0` on startup to force the ESP32 into USB flashing/bootloader mode. A $10\,\text{k}\Omega$ pull-up resistor ($R14$) ensures `IO0` stays pulled HIGH during normal operation so the chip boots standard code.

---

### User UI & Peripherals
* **User Pushbuttons (`SW4`, `SW5`, `SW6`):** Standard tactile buttons tied to `D3`, `D6`, and `D7`. When pressed, they ground the input line, giving the user programmable controls (e.g., selecting robot fight modes or starting a match).
* **Status LED (`D6`, $R15$):** A debug LED connected to $+3.3\text{V}$ via a $1\,\text{k}\Omega$ current-limiting resistor ($R15$) for visual feedback.

---

### Breakout & Expansion Headers
* **Power Breakouts (`J7`, `J9`):** 4-pin headers giving easy access to GND and $+3.3\text{V}$ rails for external modules, logic analyzers, or multimeters during bench testing.
* **OLED / Sensor Connector (`J17`):** 4-pin connector routing $+3.3\text{V}$, GND, `D10`, and `D17` for plugging in external displays or additional sensor modules.
* **Servo Connector (`J11`):** Dedicated 3-pin header routing $+5\text{V}$, GND, and signal line `D18` to drive a servo motor directly.
## Final Schematic
<img width="3264" height="2112" alt="Mini_sumo (7)" src="https://github.com/user-attachments/assets/956de7ec-9b69-4fdd-9dd3-53660b42b521" />

## Board in Hand: Lessons & Physical Hardware Issues

Testing the physical V1 board revealed several layout footprint mismatches and routing constraints that required manual rework:

* **Header Pin Size Mismatches:** The physical pin header footprints for GND, 3.3V, breakout points, and the OLED screen connector were sized incorrectly compared to the actual component pitch/pin sizes.
* **OLED Screen Rework:** Because of the pin size mismatch at header `J17`, the display could not be mounted directly to the PCB. As a temporary workaround, jumper wires had to be manually soldered to interface the screen with the board.
* **Large Board Footprint:** Things **HUGE!**
* **Next Version Improvements:** V2 will utilize double-sided SMT component placement to shrink the board footprint significantly, alongside corrected pin header footprints to eliminate wire jumpers.
##Testing & Peripheral Hardware Validation

 For the buttons 
 i use micropython and thonny the arduiono ide would work just fine
 Thonny.

### Interactive Reflex Game
An interactive MicroPython script that measures reaction times in milliseconds using `time.ticks_ms()` to stress-test button responsiveness under dynamic polling loop conditions.

```python
import time
import random
from machine import Pin

# Initialize switches with internal pull-ups (Active LOW)
switches = {
    "SW4 (IO3)": Pin(3, Pin.IN, Pin.PULL_UP),
    "SW5 (IO6)": Pin(6, Pin.IN, Pin.PULL_UP),
    "SW6 (IO7)": Pin(7, Pin.IN, Pin.PULL_UP),
}

print("=" * 40)
print("   MINI-SUMO BUTTON REFLEX CHALLENGE")
print("=" * 40)
print("Instructions: Press the requested button as fast as possible when prompted!\n")

time.sleep(2)

score = 0
total_rounds = 5

for r in range(1, total_rounds + 1):
    print(f"\n--- ROUND {r} of {total_rounds} ---")
    print("Get ready...")
    
    # Wait a random delay (1.5 to 4 seconds) to prevent guessing
    time.sleep(random.uniform(1.5, 4.0))
    
    # Select a target button randomly
    target_name, target_pin = random.choice(list(switches.items()))
    
    print("\n" + "#" * 30)
    print(f"   ---> PRESS {target_name}! <---")
    print("#" * 30)
    
    start_time = time.ticks_ms()
    pressed = False
    
    while not pressed:
        # Check all switches
        for name, pin in switches.items():
            if pin.value() == 0:  # Button pressed (LOW)
                reaction_time = time.ticks_diff(time.ticks_ms(), start_time)
                
                if name == target_name:
                    print(f"SUCCESS! Reaction Time: {reaction_time} ms")
                    score += 1
                else:
                    print(f"WRONG BUTTON! You pressed {name} instead of {target_name}. (+0 pts)")
                
                pressed = True
                
                # Debounce / wait until button is released before moving on
                while pin.value() == 0:
                    time.sleep_ms(10)
                break
                
        time.sleep_ms(5)  # Polling delay

    time.sleep(1)

print("\n" + "=" * 40)
print(f"GAME OVER! Final Score: {score} / {total_rounds}")
if score == total_rounds:
    print("Rating: SUMO GRAND CHAMPION (Lightning fast!)")
elif score >= 3:
    print("Rating: SOLID REFLEXES")
else:
    print("Rating: NEEDS PRACTICE")
print("=" * 40)

