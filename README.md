# Phishing
Course Project for Causal Learning

Requirements are in requirements.txt

Usage:

python phishing.py run_all a y l
 run_all: 0 for running the calculations on all edges investigated in writeup or 1 for a specific edge (defaults to 0)
 A: the treatment (not required if run_all is 0)
 Y: the outcome  (not required if run_all is 0)
 L: the confounder (never required) 

Possible variable names in the dataset are P, F, I, S, W, D, L, A, R, and T. See the report writeup for what these stand for.