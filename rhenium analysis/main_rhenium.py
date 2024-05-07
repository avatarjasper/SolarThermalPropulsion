import numpy as np
from receiver_rhenium import Cone
from collector import Collector
from nozzle import Nozzle
from tanks import Tanks
import pandas as pd
import os
from tqdm import tqdm


#RECEIVER
CONE_RADIUS = 0.05 # m
CONE_LENGTH = 0.075 # m
CONE_THICKNESS = 0.002 # m
RHENIUM_DENSITY = 21030 # kg/m^3
RHENIUM_C_P = 138 # J/kgK
RHENIUM_THERMAL_CONDUCTIVITY = 48 # W/mK
T_MAX_RHENIUM = 3100 # K
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

def dftocsv(df):
    if os.path.isfile('gridsearch_results.csv'):
        df.to_csv('gridsearch_results.csv', mode='a', header=False)
    else:
        df.to_csv('gridsearch_results.csv', mode='w', header=True)
###########################
#ITERATION FOR GRID SEARCH
###########################
# minAT = np.pi * 0.0005**2
# maxAT = np.pi * 0.05**2

# minAE = np.pi * 0.005**2 
# maxAE = np.pi * 0.1**2
# print(minAT, maxAT, minAE, maxAE)

# AT = np.linspace(minAT, maxAT, 100)
# AE = np.linspace(minAE, maxAE, 100)
# min_mass = float('inf')
# best_values = None


# for at in tqdm(AT):
#     for ae in AE:
#     # while CR_INIT>13000:
#         cone = Cone(CONE_RADIUS, CONE_LENGTH, CONE_THICKNESS, RHENIUM_DENSITY, RHENIUM_C_P, RHENIUM_THERMAL_CONDUCTIVITY, T_MAX_RHENIUM, MDOT_INIT, STORAGE_TEMP, CHANNEL_THICKNESS, CONE_OUTER_WALL_THICKNESS)

#         nozzle = Nozzle(DELTA_V, SC_MASS_MAX, GAMMA, RA, M, TIME_BURN, at, ae, cone.Tc, ANGLE_DIVERGENCE, NOZZLE_DENSITY, NOZZLE_ULTIMATE_STRENGTH, NOZZLE_SF)

#         MDOT = 0
#         delta = 0.00000001
#         while abs(MDOT - nozzle.m_dot) > delta:
#             MDOT = nozzle.m_dot
#             cone = Cone(CONE_RADIUS, CONE_LENGTH, CONE_THICKNESS, RHENIUM_DENSITY, RHENIUM_C_P, RHENIUM_THERMAL_CONDUCTIVITY, T_MAX_RHENIUM, MDOT, STORAGE_TEMP, CHANNEL_THICKNESS, CONE_OUTER_WALL_THICKNESS)
#             nozzle = Nozzle(DELTA_V, SC_MASS_MAX, GAMMA, RA, M, TIME_BURN, at, ae, cone.Tc, ANGLE_DIVERGENCE, NOZZLE_DENSITY, NOZZLE_ULTIMATE_STRENGTH, NOZZLE_SF)
#         # if MDOT- nozzle.m_dot < delta:
#             # print('MDOT converged')

#         #TRANSMISSION, COLLECTOR
#         TRANSMISSION_EFFICIENCY = 0.6
#         COLLECTOR_NUMBER = 5
#         TRANSMISSION_DIAMETER = 5 * 760e-6 # m #for 19 cables 
#         SOLAR_FLUX = 1361 # W/m^2
#         NUMBER_CABLES = 19 #random but from paper for now
#         LENGTH_TRANSMISSION = 0.5 #m assumption
#         TRANSMISSION_DENSITY = 2650 #kg/m^3

#         collector = Collector(cone.power_to_prop, TRANSMISSION_EFFICIENCY, COLLECTOR_NUMBER, TRANSMISSION_DIAMETER, SOLAR_FLUX, NUMBER_CABLES, LENGTH_TRANSMISSION, TRANSMISSION_DENSITY)

#         # TANKS
#         WATER_DENSITY = 1000 #kg
#         TANK_YIELD_STRESS = 90e6 # Pa
#         TANK_DENSITY = 2700 # kg/m^3
#         TANK_SF = 2
#         TANK_RADIUS = 0.05 #m , = 1 cm
#         M_HELIUM = 4.002602e-3 # kg/mol
#         R_PRESSURANT_SPEC = RA/M_HELIUM
#         GAMMA_HELIUM = 1.66
#         INITIAL_GUESS_PRESSURANT_PRESSURE = nozzle.pc + 1
#         BOUNDS = [(nozzle.pc, 300e5)]


#         tanks = Tanks(nozzle.mp, WATER_DENSITY, TANK_YIELD_STRESS, TANK_DENSITY, TANK_SF, TANK_RADIUS, R_PRESSURANT_SPEC, STORAGE_TEMP, GAMMA_HELIUM, INITIAL_GUESS_PRESSURANT_PRESSURE, BOUNDS, nozzle.pc)



#         cone_mass_total = cone.mass_total(nozzle.rt)
#         nozzle_mass_total = nozzle.mass_total()
#         collector_mass_total = collector.mass_total()
#         tanks_mass_total = tanks.total_mass()
#         system_mass = cone_mass_total + nozzle_mass_total + collector_mass_total + tanks_mass_total


#         if check(cone.Tc, T_MAX_RHENIUM, cone_mass_total, nozzle.ae_at_ratio, nozzle.mp, nozzle.F_compl, collector.concentration_ratio, nozzle_mass_total, collector_mass_total, tanks_mass_total):
#             info = pd.DataFrame([cone.__dict__, nozzle.__dict__, collector.__dict__, tanks.__dict__, {'system_mass': system_mass}])
#             dftocsv(info)
#             if system_mass < min_mass:
#                 min_mass = system_mass
#                 best_values = {'at':at, 'ae':ae}
            
# print(min_mass)
# print(best_values)
# print(nozzle.ae_at_ratio)
# print(cone.Tc)




#################################
#BEST VALUES FROM GRID SEARCH: use this in case you do not want to run the whole iteration, but just see the values using the throat and exit areas that give the lowest mass.
#################################
at = 8.011061266653972e-05
ae = 0.0029273931544813976


#RHENIUM
cone = Cone(CONE_RADIUS, CONE_LENGTH, CONE_THICKNESS, RHENIUM_DENSITY, RHENIUM_C_P, RHENIUM_THERMAL_CONDUCTIVITY, T_MAX_RHENIUM, MDOT_INIT, STORAGE_TEMP, CHANNEL_THICKNESS, CONE_OUTER_WALL_THICKNESS)

nozzle = Nozzle(DELTA_V, SC_MASS_MAX, GAMMA, RA, M, TIME_BURN, at, ae, cone.Tc, ANGLE_DIVERGENCE, NOZZLE_DENSITY, NOZZLE_ULTIMATE_STRENGTH, NOZZLE_SF)

MDOT = 0
delta = 0.00000001
while abs(MDOT - nozzle.m_dot) > delta:
    MDOT = nozzle.m_dot
    cone = Cone(CONE_RADIUS, CONE_LENGTH, CONE_THICKNESS, RHENIUM_DENSITY, RHENIUM_C_P, RHENIUM_THERMAL_CONDUCTIVITY, T_MAX_RHENIUM, MDOT, STORAGE_TEMP, CHANNEL_THICKNESS, CONE_OUTER_WALL_THICKNESS)
    nozzle = Nozzle(DELTA_V, SC_MASS_MAX, GAMMA, RA, M, TIME_BURN, at, ae, cone.Tc, ANGLE_DIVERGENCE, NOZZLE_DENSITY, NOZZLE_ULTIMATE_STRENGTH, NOZZLE_SF)
# if MDOT- nozzle.m_dot < delta:
    # print('MDOT converged')

#TRANSMISSION, COLLECTOR
TRANSMISSION_EFFICIENCY = 0.6
COLLECTOR_NUMBER = 5
TRANSMISSION_DIAMETER = 5 * 760e-6 # m #for 19 cables 
SOLAR_FLUX = 1361 # W/m^2
NUMBER_CABLES = 19 #random but from paper for now
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

cone_mass_total = cone.mass_total(nozzle.rt)
nozzle_mass_total = nozzle.mass_total()
collector_mass_total = collector.mass_total()
tanks_mass_total = tanks.total_mass()
system_mass = cone_mass_total + nozzle_mass_total + collector_mass_total + tanks_mass_total

print(cone.__dict__)
print(f'{cone.mass_lateral_outer(nozzle.rt)=}')
print(f'{cone.mass_lateral_outer(nozzle.rt)/cone.density=}')

print('\n')
print(nozzle.__dict__)

print(f'{np.sqrt(at/np.pi)=}')
print(f'{np.sqrt(ae/np.pi)=}')

print('\n')
print(collector.__dict__)
print(collector.mass_parabolic())
print(collector.collector)
print(collector.collector_area)
print(collector.collector_radius)
print('\n')
print(tanks.__dict__)

V_chamber = np.pi * cone.radius**2 * cone.length * 1/3 - np.pi * (cone.radius + cone.thickness + cone.t_channel + cone.thickness_outer - nozzle.rt)**2 * cone.length * 1/3
c_star = nozzle.pc * nozzle.at / nozzle.m_dot

tau = V_chamber / (nozzle.at * c_star * nozzle.vandenkerckhove**2)
print(f'{tau=}')
print(system_mass)

