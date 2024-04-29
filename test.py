import numpy as np

t = 0.002
mdot = 0.1
cp = 1000
k = 24
Slat = 0.05
Tmax = 3500
Tst = 400

def Tc(t, mdot, cp, k, Slat, Tmax, Tst):
    return (Tmax + (t * mdot * cp * Tst) / (k * Slat)) / (1 + t * mdot * cp / (k * Slat))

def func(x):
    return Tmax - (mdot * cp * (x - Tst) * t) / (k * Slat) - x

Tc_act = Tc(t, mdot, cp, k, Slat, Tmax, Tst)
print(Tc_act)

from scipy.optimize import fsolve
Tc_fsolve = fsolve(func, 3500)
print(Tc_fsolve)