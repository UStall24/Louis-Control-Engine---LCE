# Matlab Github

**Table of Contents**

[[_TOC_]]

This MATLAB script calculates the required thruster outputs for a given desired movement in six degrees of freedom (DoF): Surge (X), Sway (Y), Heave (Z), Roll (Mx), Pitch (My), and Yaw (Mz).

## Calculation Method for Thrusters

1. **Constants and Geometry**: Define the radii and positions of the thrusters relative to the center of gravity.
2. **B Matrix**: Construct the B matrix based on the geometry and angles.
3. **Thruster Outputs Calculation**: For each DoF, the script calculates the necessary thruster efforts and normalizes them.

## Running the Script

Simply run the script in MATLAB to see the thruster outputs for each DoF.

## Changelog

- **17 April 2025**: Initial version of the document.
