import numpy as np
import matplotlib.pyplot as plt
import csv
import json


# --- CONFIG ---
CSV_FILE = "t200_performance_chart.csv"
PWM_THRESHOLD_LOW = 1464
PWM_THRESHOLD_HIGH = 1536
POLY_DEGREE_PWM = 2  # degree for pwm fits
POLY_DEGREE_CURRENT = 2 # degree for current fit

# --- Load CSV ---
pwm = []
force = []
current = []

with open(CSV_FILE, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    next(reader)  # skip header
    for row in reader:
        try:
            pwm_val = int(row[0])
            current_val = float(row[2].replace(',', '.'))
            force_val = float(row[5].replace(',', '.'))
            pwm.append(pwm_val)
            force.append(force_val)
            current.append(current_val)
        except (ValueError, IndexError):
            continue

pwm = np.array(pwm)
force = np.array(force)
current = np.array(current)

# --- Split for PWM ---
mask_low = pwm < PWM_THRESHOLD_LOW
mask_high = pwm > PWM_THRESHOLD_HIGH

force_low = force[mask_low]
pwm_low = pwm[mask_low]

force_high = force[mask_high]
pwm_high = pwm[mask_high]

# --- Split for Current (positive/negative forces) ---
mask_positive_force = force > 0
mask_negative_force = force < 0

force_pos = force[mask_positive_force]
current_pos = current[mask_positive_force]

force_neg = force[mask_negative_force]
current_neg = current[mask_negative_force]

# --- Fit polynomials ---
coeff_pwm_low = np.polyfit(force_low, pwm_low, POLY_DEGREE_PWM)
coeff_pwm_high = np.polyfit(force_high, pwm_high, POLY_DEGREE_PWM)
coeff_current_pos = np.polyfit(force_pos, current_pos, POLY_DEGREE_CURRENT)
coeff_current_neg = np.polyfit(force_neg, current_neg, POLY_DEGREE_CURRENT)

poly_pwm_low = np.poly1d(coeff_pwm_low)
poly_pwm_high = np.poly1d(coeff_pwm_high)
poly_current_pos = np.poly1d(coeff_current_pos)
poly_current_neg = np.poly1d(coeff_current_neg)

# --- Print coefficients ---
print("PWM LOW REGION COEFF (force2pwm, PWM < 1464):")
print(coeff_pwm_low)

print("\nPWM HIGH REGION COEFF (force2pwm, PWM > 1536):")
print(coeff_pwm_high)

print("\nCURRENT COEFF POSITIVE FORCE (force2current):")
print(coeff_current_pos)

print("\nCURRENT COEFF NEGATIVE FORCE (force2current):")
print(coeff_current_neg)

# Collect coefficients into a dictionary
coefficients = {
    "force2pwm": {
        "low": coeff_pwm_low.tolist(),
        "high": coeff_pwm_high.tolist()
    },
    "force2current": {
        "low": coeff_current_neg.tolist(),
        "high": coeff_current_pos.tolist()
    },
    "max_force_forward": max(force),
    "max_force_reverse": abs(min(force))
}

# Save to JSON
with open("dynamic_throttle_data.json", "w") as f:
    json.dump(coefficients, f, indent=4)

print("Coefficients saved to dynamic_throttle_data.json")


# --- Plotting ---
force_range_pos = np.linspace(0, max(force), 300)
force_range_neg = np.linspace(min(force), 0, 300)
force_range_full = np.linspace(min(force), max(force), 300)

plt.figure(figsize=(12, 10))

# PWM
plt.subplot(2, 2, 1)
plt.plot(force, pwm, 'o', alpha=0.4, label="Data")
plt.plot(force_range_full, poly_pwm_low(force_range_full), 'r--', label="Fit: PWM < 1464")
plt.plot(force_range_full, poly_pwm_high(force_range_full), 'g--', label="Fit: PWM > 1536")
plt.axhline(PWM_THRESHOLD_LOW, linestyle=':', color='r', alpha=0.3)
plt.axhline(PWM_THRESHOLD_HIGH, linestyle=':', color='g', alpha=0.3)
plt.title("Force → PWM")
plt.xlabel("Force (N)")
plt.ylabel("PWM")
plt.legend()
plt.grid(True)

# Current (positive forces)
plt.subplot(2, 2, 2)
plt.plot(force, current, 'o', alpha=0.4, label="Positive Force Data")
plt.plot(force_range_pos, poly_current_pos(force_range_pos), 'b-', label="Positive Force Fit")
plt.plot(force_range_neg, poly_current_neg(force_range_neg), 'b-', label="Negative Force Fit")

plt.show()