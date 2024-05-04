import numpy as np
from receiver import Cone
from collector import Collector
from nozzle import Nozzle
from tanks import Tanks
#RECEIVER
CONE_RADIUS = 0.05 # m
CONE_LENGTH = 0.075 # m
CONE_THICKNESS = 0.002 # m
GRAPHITE_DENSITY = 2250 # kg/m^3
GRAPIHITE_C_P = 707.7 # J/kgK
GRAPHITE_THERMAL_CONDUCTIVITY = 24.0 # W/mK
T_MAX_GRAPHITE = 3500 # K
MDOT_INIT = 5.141931363082546e-05 # kg/s
STORAGE_TEMP = 400 # K
CHANNEL_THICKNESS = 0.005 #m = 5mm
CONE_OUTER_WALL_THICKNESS = 0.01 # 1 cm

#NOZZLE
DELTA_V = 200 # m/s (at least)
SC_MASS_MAX = 24 # kg
GAMMA = 1.33
RA = 8.31446261815324
M = 18.01528e-3
TIME_BURN = 8*3600
AT = 8e-6
AE = 160e-6
ANGLE_DIVERGENCE = 15 * np.pi / 180 #15 degrees
NOZZLE_DENSITY = 8190 # inconel
NOZZLE_ULTIMATE_STRENGTH = 1375e6 #Pa
NOZZLE_SF = 1.5 # from the barry book


cone = Cone(CONE_RADIUS, CONE_LENGTH, CONE_THICKNESS, GRAPHITE_DENSITY, GRAPIHITE_C_P, GRAPHITE_THERMAL_CONDUCTIVITY, T_MAX_GRAPHITE, MDOT_INIT, STORAGE_TEMP, CHANNEL_THICKNESS, CONE_OUTER_WALL_THICKNESS)

nozzle = Nozzle(DELTA_V, SC_MASS_MAX, GAMMA, RA, M, TIME_BURN, AT, AE, cone.Tc, ANGLE_DIVERGENCE, NOZZLE_DENSITY, NOZZLE_ULTIMATE_STRENGTH, NOZZLE_SF)


MDOT = 0
delta = 0.00000001
while abs(MDOT - nozzle.m_dot) > delta:
    MDOT = nozzle.m_dot
    cone = Cone(CONE_RADIUS, CONE_LENGTH, CONE_THICKNESS, GRAPHITE_DENSITY, GRAPIHITE_C_P, GRAPHITE_THERMAL_CONDUCTIVITY, T_MAX_GRAPHITE, MDOT, STORAGE_TEMP, CHANNEL_THICKNESS, CONE_OUTER_WALL_THICKNESS)
    nozzle = Nozzle(DELTA_V, SC_MASS_MAX, GAMMA, RA, M, TIME_BURN, AT, AE, cone.Tc, ANGLE_DIVERGENCE, NOZZLE_DENSITY, NOZZLE_ULTIMATE_STRENGTH, NOZZLE_SF)

print(f'{cone.Tc=}')
print(f'{cone.mass=}')
print(f'{nozzle.m_dot=}')


TRANSMISSION_EFFICIENCY = 0.8
COLLECTOR_NUMBER = 5
TRANSMISSION_DIAMETER = 760e-6 # m
SOLAR_FLUX = 1361 # W/m^2
NUMBER_CABLES = 7 #random but from paper for now
LENGTH_TRANSMISSION = 0.5 #m assumption
TRANSMISSION_DENSITY = 2650 #kg/m^3



collector = Collector(cone.power_to_prop, TRANSMISSION_EFFICIENCY, COLLECTOR_NUMBER, TRANSMISSION_DIAMETER, SOLAR_FLUX, NUMBER_CABLES, LENGTH_TRANSMISSION, TRANSMISSION_DENSITY)


WATER_DENSITY = 1000 #kg
TANK_YIELD_STRESS = 90e6 # Pa
TANK_DENSITY = 2700 # kg/m^3
TANK_SF = 2
TANK_RADIUS = 0.05 #m , = 1 cm

tanks = Tanks(nozzle.mp, WATER_DENSITY, TANK_YIELD_STRESS, TANK_DENSITY, TANK_SF, TANK_RADIUS)


#TODO:
# does not yet include all components that attribute to mass, like pressurant, 

#print all the tank attributes
# attrs = vars(nozzle)
# print(', '.join("%s: %s" % item for item in attrs.items()))
print(nozzle.__dict__)
print(tanks.__dict__)

print(cone.mass_total(nozzle.rt))
print(nozzle.mass_total())
print(collector.mass_total())
print(tanks.total_mass(nozzle.pc))



system_mass = cone.mass_total(nozzle.rt) + nozzle.mass_total() + collector.mass_total() + tanks.total_mass(nozzle.pc)
print(system_mass)
