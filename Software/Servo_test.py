import time
from machine import PWM, Pin

# Servo setup on GPIO 18 (D18)
servo_pin = Pin(18, Pin.OUT)
servo_pwm = PWM(servo_pin)
servo_pwm.freq(50)

# Switches configured with internal pull-ups (Active LOW)
sw4 = Pin(3, Pin.IN, Pin.PULL_UP)  # SW4 -> 0 deg
sw5 = Pin(6, Pin.IN, Pin.PULL_UP)  # SW5 -> 90 deg
sw6 = Pin(7, Pin.IN, Pin.PULL_UP)  # SW6 -> 180 deg


def set_angle(angle):
    angle = max(0, min(180, angle))
    # Map 0-180 deg to 16-bit PWM duty (1638 = 0.5ms, 8192 = 2.5ms at 50Hz)
    duty = int(1638 + (angle / 180.0) * (8192 - 1638))
    servo_pwm.duty_u16(duty)


# Move to center position on boot
set_angle(90)

print("Servo Button Test Active on GPIO 18")
print("Press SW4 (GPIO 3) -> 0° | SW5 (GPIO 6) -> 90° | SW6 (GPIO 7) -> 180°")

while True:
    if sw4.value() == 0:
        set_angle(0)
        print("SW4 Pressed -> Servo set to 0°")
        while sw4.value() == 0:  # Debounce hold
            time.sleep_ms(10)

    elif sw5.value() == 0:
        set_angle(90)
        print("SW5 Pressed -> Servo set to 90°")
        while sw5.value() == 0:
            time.sleep_ms(10)

    elif sw6.value() == 0:
        set_angle(180)
        print("SW6 Pressed -> Servo set to 180°")
        while sw6.value() == 0:
            time.sleep_ms(10)

    time.sleep_ms(20)
