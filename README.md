# Esp-Sumo

ESP32 General-Purpose Robotics Development Kit in its early stages 

A low-cost, open-source motion control board for ESP32-based robots.

High-performance motor driver boards are often tailored to a single use case or carry a steep price tag. This project provides a low-cost, all-in-one hardware foundation designed to drive small-scale, high-precision mobile robots without requiring extra breakout boards or expensive driver shields.

Supported Kinematics & Applications:

Mini Sumo Robots: Integrated motor control and gyro feedback for rapid opponent tracking and high-torque maneuvers.

Inverted Pendulum / Self-Balancing: Direct IMU integration for low-latency loop control and pitch stabilization.

Heading-Corrected Rovers: Closed-loop yaw monitoring for straight-line differential driving and precise turn angles.

 V1 Key Features:

  Native dual DC motor drivers with PWM speed and direction control
  Dual TI DRV8870 motor driver IC's with PWM speed and direction control
  supporting motors with peak currents of up to 3.6 A .
  
  Onboard 6-axis mpu-6050 gyroscope/accelerometer using I2C interface.
  
  Integrated power regulation optimized for 7.4V LiPo batteries.
  
  Exposed GPIO headers for edge sensors, line detectors, and custom expansions.
  
  100% open-source hardware (KiCad schematics, PCB layout, and production files provided).
