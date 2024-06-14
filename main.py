import numpy as np
from receiver import Cone
from collector import Collector
from nozzle import Nozzle
from tanks import Tanks
import pandas as pd
import os
from tqdm import tqdm
from constants import *
import matplotlib.pyplot as plt

def check(Tc, Temp_max, cone_Mtotal, ae_at_rat, mass_prop, F, CR, nozzle_Mtotal, collector_Mtotal, tanks_Mtotal):
    if Tc > Temp_max or cone_Mtotal > 12 or ae_at_rat < 1 or mass_prop > 12 or F > 2 or CR > 13000 or nozzle_Mtotal > 12 or collector_Mtotal > 12 or tanks_Mtotal > 12:
        return False
    return True

def dftocsv(df, filename='gridsearch_results.csv'):
    write_header = not os.path.isfile(filename)
    df.to_csv(filename, mode='a' if write_header else 'w', header=write_header)

def iteration(_at, _ae, _mdot_init):
    cone_params = default_cone_params.copy()
    cone_params['mdot'] = _mdot_init
    
    cone = Cone(**cone_params)


    nozzle_params = default_nozzle_params.copy()
    nozzle_params['at'] = _at
    nozzle_params['ae'] = _ae
    nozzle_params['Tc'] = cone.Tc

    nozzle = Nozzle(**nozzle_params)

    MDOT = 0
    delta = 0.00000001
    while abs(MDOT - nozzle.m_dot) > delta:
        MDOT = nozzle.m_dot
        cone_params = default_cone_params.copy()
        cone_params['mdot'] = MDOT
        cone = Cone(**cone_params)

        nozzle_params = default_nozzle_params.copy()
        nozzle_params['at'] = _at
        nozzle_params['ae'] = _ae
        nozzle_params['Tc'] = cone.Tc
        nozzle = Nozzle(**nozzle_params)

    

    collector_params = default_collector_params.copy()
    collector_params['power_to_receiver'] = cone.power_to_prop

    collector = Collector(**collector_params)


    INITIAL_GUESS_PRESSURANT_PRESSURE = nozzle.pc + 1
    BOUNDS = [(nozzle.pc, 300e5)]

    tanks_params = default_tanks_params.copy()
    tanks_params['propellant_mass'] = nozzle.mp
    tanks_params['init_guess'] = INITIAL_GUESS_PRESSURANT_PRESSURE
    tanks_params['bounds'] = BOUNDS
    tanks_params['pc'] = nozzle.pc

    tanks = Tanks(**tanks_params)
    return cone, nozzle, collector, tanks


###########################
#ITERATION FOR GRID SEARCH: uncomment this whole thing and comment the best values part to run the grid search
###########################
# MIN_AT = np.pi * 0.0005**2
# MAX_AT = np.pi * 0.05**2

# MIN_AE = np.pi * 0.005**2 
# MAX_AE = np.pi * 0.1**2

# AT = np.linspace(MIN_AT, MAX_AT, 100)
# AE = np.linspace(MIN_AE, MAX_AE, 100)
# min_mass = float('inf')
# best_values = None


# for at in tqdm(AT):
#     for ae in AE:
#         cone, nozzle, collector, tanks = iteration(at, ae, MDOT_INIT)

#         cone_mass_total = cone.mass_total(nozzle.rt)
#         nozzle_mass_total = nozzle.mass_total()
#         collector_mass_total = collector.mass_total()
#         tanks_mass_total = tanks.total_mass_blow_down(RATIO_BLOW_DOWN)
#         system_mass = cone_mass_total + nozzle_mass_total + collector_mass_total + tanks_mass_total

#         if check(cone.Tc, T_MAX_GRAPHITE, cone_mass_total, nozzle.ae_at_ratio, nozzle.mp, nozzle.F_compl, collector.concentration_ratio, nozzle_mass_total, collector_mass_total, tanks_mass_total):
#             info = pd.DataFrame([cone.__dict__, nozzle.__dict__, collector.__dict__, tanks.__dict__, {'system_mass': system_mass}])
#             dftocsv(info)
#             if system_mass < min_mass:
#                 min_mass = system_mass
#                 best_values = {'at':at, 'ae':ae}
            
# print(min_mass)
# print(best_values)
# print(cone_mass_total)
# print(nozzle_mass_total)
# print(collector_mass_total)
# print(tanks_mass_total)

# print(tanks.__dict__)


################################
# BEST VALUES FROM GRID SEARCH: use this in case you do not want to run the whole iteration, but just see the values using the throat and exit areas that give the lowest mass.
################################

at = 7.853981633974482e-07
ae = 0.0003950790761332618


cone, nozzle, collector, tanks = iteration(at, ae, MDOT_INIT)

cone_mass_total = cone.mass_total(nozzle.rt)
nozzle_mass_total = nozzle.mass_total()
collector_mass_total = collector.mass_total()
tanks_mass_total = tanks.total_mass_blow_down(RATIO_BLOW_DOWN)
system_mass = cone_mass_total + nozzle_mass_total + collector_mass_total + tanks_mass_total

print(cone.__dict__)
print(f'{cone.mass_lateral_outer(nozzle.rt)=}')
print(f'{cone.mass_lateral_outer(nozzle.rt)/cone.density=}')

print('\n')
print(nozzle.__dict__)
print(f'{nozzle.Ue=}')
delta = nozzle.pe/nozzle.m_dot * nozzle.ae
print(f'{delta=}')
Ueq = nozzle.Ue + delta
print(f'{Ueq=}')
print(f'{Ueq/9.81=}')
difference = delta/nozzle.Ue * 100
print(f'{difference=}')
print(nozzle.mass_total())

radius_throat = np.sqrt(nozzle.at/np.pi)
radius_exit = np.sqrt(nozzle.ae/np.pi)
print(f'{radius_throat=}')
print(f'{radius_exit=}')


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


tanks_total_vol = tanks.total_volume_blow_down
print(f'{tanks_total_vol=}')
cone_vol = np.pi * cone.radius**2 * cone.length * 1/3
nozzle_vol = np.pi * (radius_exit)**2 * nozzle.length_nozzle * 1/3
collector_vol = 0.1*0.1*0.05

total_vol_propulsion = tanks_total_vol + cone_vol + nozzle_vol + collector_vol
print(f'{total_vol_propulsion=}')

print(system_mass)


###############################
#Plots for changing the dimensions of the cone. Uncomment this whole thing to run the plots: note that at and ae need to be specified.
###############################
# radius_list = np.linspace(5*TRANSMISSION_DIAMETER, 0.1, 100)
# length_list = np.linspace(0.025, 0.15, 100)
# thickness_list = np.linspace(0.001, 0.02, 100)
# Tc_list = np.zeros(len(radius_list)) 

# for i in range(len(radius_list)):
#     cone_params = default_cone_params.copy()
#     cone_params['mdot'] = MDOT_INIT
#     cone_params['radius'] = radius_list[i]
    
#     cone = Cone(**cone_params)


#     nozzle_params = default_nozzle_params.copy()
#     nozzle_params['at'] = at
#     nozzle_params['ae'] = ae
#     nozzle_params['Tc'] = cone.Tc

#     nozzle = Nozzle(**nozzle_params)

#     MDOT = 0
#     delta = 0.00000001
#     while abs(MDOT - nozzle.m_dot) > delta:
#         MDOT = nozzle.m_dot
#         cone_params = default_cone_params.copy()
#         cone_params['mdot'] = MDOT
#         cone = Cone(**cone_params)

#         nozzle_params = default_nozzle_params.copy()
#         nozzle_params['at'] = at
#         nozzle_params['ae'] = ae
#         nozzle_params['Tc'] = cone.Tc
#         nozzle = Nozzle(**nozzle_params)
    
#     Tc_list[i] = cone.Tc

# plt.xlabel('Radius [m]')
# plt.ylabel('$T_c$ [K]')
# plt.plot(radius_list, Tc_list, label='Tc vs Radius')
# plt.axvline(x=0.05, color='r', linestyle='--', label='Radius = 0.05')
# plt.legend()
# plt.savefig('Tc_vs_Radius.png')
# # plt.ticklabel_format(useOffset=False)
# plt.show()


# for i in range(len(length_list)):
#     cone_params = default_cone_params.copy()
#     cone_params['mdot'] = MDOT_INIT
#     cone_params['length'] = length_list[i]
    
#     cone = Cone(**cone_params)


#     nozzle_params = default_nozzle_params.copy()
#     nozzle_params['at'] = at
#     nozzle_params['ae'] = ae
#     nozzle_params['Tc'] = cone.Tc

#     nozzle = Nozzle(**nozzle_params)

#     MDOT = 0
#     delta = 0.00000001
#     while abs(MDOT - nozzle.m_dot) > delta:
#         MDOT = nozzle.m_dot
#         cone_params = default_cone_params.copy()
#         cone_params['mdot'] = MDOT
#         cone = Cone(**cone_params)

#         nozzle_params = default_nozzle_params.copy()
#         nozzle_params['at'] = at
#         nozzle_params['ae'] = ae
#         nozzle_params['Tc'] = cone.Tc
#         nozzle = Nozzle(**nozzle_params)
    
#     Tc_list[i] = cone.Tc

# plt.xlabel('Length [m]')
# plt.ylabel('$T_c$ [K]')
# plt.plot(length_list, Tc_list, label='Tc vs Length')
# plt.axvline(x=0.075, color='r', linestyle='--', label='Length = 0.075')
# plt.legend()
# plt.savefig('Tc_vs_Length.png')
# # plt.ticklabel_format(useOffset=False)
# plt.show()

