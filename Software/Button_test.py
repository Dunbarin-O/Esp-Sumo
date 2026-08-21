#MADE FOR MICROPYTHON 
Python
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
