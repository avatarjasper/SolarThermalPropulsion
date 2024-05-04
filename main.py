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
STORAGE_TEMP = 300 # K
CHANNEL_THICKNESS = 0.005 #m = 5mm
CONE_OUTER_WALL_THICKNESS = 0.01 # 1 cm


#NOZZLE
DELTA_V = 200 # m/s (at least)
SC_MASS_MAX = 24 # kg
GAMMA = 1.33
RA = 8.31446261815324
M = 18.01528e-3 # kg/mol
TIME_BURN = 8*3600
ANGLE_DIVERGENCE = 15 * np.pi / 180 #15 degrees
NOZZLE_DENSITY = 8190 # inconel
NOZZLE_ULTIMATE_STRENGTH = 1375e6 #Pa
NOZZLE_SF = 1.5 # from the barry book


def check(Tc, Temp_max, cone_Mtotal, ae_at_rat, mass_prop, F, CR, nozzle_Mtotal, collector_Mtotal, tanks_Mtotal):
    if Tc > Temp_max or cone_Mtotal > 12 or ae_at_rat < 1 or mass_prop > 12 or F > 2 or CR > 13000 or nozzle_Mtotal > 12 or collector_Mtotal > 12 or tanks_Mtotal > 12:
        return False
    return True



# AT = 8e-6
# AE = 160e-6


minAT = np.pi * 0.0005**2
maxAT = np.pi * 0.05**2

minAE = np.pi * 0.005**2 
maxAE = np.pi * 0.1**2

AT = np.linspace(minAT, maxAT, 100)
AE = np.linspace(minAE, maxAE, 100)

for at in AT:
    for ae in AE:

        cone = Cone(CONE_RADIUS, CONE_LENGTH, CONE_THICKNESS, GRAPHITE_DENSITY, GRAPIHITE_C_P, GRAPHITE_THERMAL_CONDUCTIVITY, T_MAX_GRAPHITE, MDOT_INIT, STORAGE_TEMP, CHANNEL_THICKNESS, CONE_OUTER_WALL_THICKNESS)

        nozzle = Nozzle(DELTA_V, SC_MASS_MAX, GAMMA, RA, M, TIME_BURN, at, ae, cone.Tc, ANGLE_DIVERGENCE, NOZZLE_DENSITY, NOZZLE_ULTIMATE_STRENGTH, NOZZLE_SF)

        MDOT = 0
        delta = 0.00000001
        while abs(MDOT - nozzle.m_dot) > delta:
            MDOT = nozzle.m_dot
            cone = Cone(CONE_RADIUS, CONE_LENGTH, CONE_THICKNESS, GRAPHITE_DENSITY, GRAPIHITE_C_P, GRAPHITE_THERMAL_CONDUCTIVITY, T_MAX_GRAPHITE, MDOT, STORAGE_TEMP, CHANNEL_THICKNESS, CONE_OUTER_WALL_THICKNESS)
            nozzle = Nozzle(DELTA_V, SC_MASS_MAX, GAMMA, RA, M, TIME_BURN, at, ae, cone.Tc, ANGLE_DIVERGENCE, NOZZLE_DENSITY, NOZZLE_ULTIMATE_STRENGTH, NOZZLE_SF)

        #TRANSMISSION, COLLECTOR
        TRANSMISSION_EFFICIENCY = 0.8
        COLLECTOR_NUMBER = 5
        TRANSMISSION_DIAMETER = 760e-6 # m
        SOLAR_FLUX = 1361 # W/m^2
        NUMBER_CABLES = 7 #random but from paper for now
        LENGTH_TRANSMISSION = 0.5 #m assumption
        TRANSMISSION_DENSITY = 2650 #kg/m^3

        collector = Collector(cone.power_to_prop, TRANSMISSION_EFFICIENCY, COLLECTOR_NUMBER, TRANSMISSION_DIAMETER, SOLAR_FLUX, NUMBER_CABLES, LENGTH_TRANSMISSION, TRANSMISSION_DENSITY)

        # TANKS
        WATER_DENSITY = 1000 #kg
        TANK_YIELD_STRESS = 90e6 # Pa
        TANK_DENSITY = 2700 # kg/m^3
        TANK_SF = 2
        TANK_RADIUS = 0.05 #m , = 1 cm
        M_HELIUM = 4.002602e-3 # kg/mol
        R_PRESSURANT_SPEC = RA/M_HELIUM
        GAMMA_HELIUM = 1.66
        INITIAL_GUESS_PRESSURANT_PRESSURE = nozzle.pc + 1
        BOUNDS = [(nozzle.pc, 300e5)]


        tanks = Tanks(nozzle.mp, WATER_DENSITY, TANK_YIELD_STRESS, TANK_DENSITY, TANK_SF, TANK_RADIUS, R_PRESSURANT_SPEC, STORAGE_TEMP, GAMMA_HELIUM, INITIAL_GUESS_PRESSURANT_PRESSURE, BOUNDS, nozzle.pc)


        # print(cone.__dict__)
        # print('\n')
        # print(nozzle.__dict__)
        # print('\n')
        # print(collector.__dict__)
        # print('\n')
        # print(tanks.__dict__)
        # print(cone.mass_total(nozzle.rt))
        # print(nozzle.mass_total())
        # print(collector.mass_total())
        # print(tanks.total_mass())
        cone_mass_total = cone.mass_total(nozzle.rt)
        nozzle_mass_total = nozzle.mass_total()
        collector_mass_total = collector.mass_total()
        tanks_mass_total = tanks.total_mass()
        system_mass = cone_mass_total + nozzle_mass_total + collector_mass_total + tanks_mass_total


        if check(cone.Tc, T_MAX_GRAPHITE, cone_mass_total, nozzle.ae_at_ratio, nozzle.mp, nozzle.F_compl, collector.concentration_ratio, nozzle_mass_total, collector_mass_total, tanks_mass_total):
            
            



