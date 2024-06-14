import numpy as np

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
DELTA_V = 200 
SC_MASS_MAX = 24 
GAMMA = 1.33
RA = 8.31446261815324
M = 18.01528e-3 
TIME_BURN = 8*3600
ANGLE_DIVERGENCE = 15 * np.pi / 180 #15 degrees
NOZZLE_DENSITY = 8190 # inconel
NOZZLE_ULTIMATE_STRENGTH = 1375e6 #Pa
NOZZLE_SF = 1.5 


#TRANSMISSION, COLLECTOR
TRANSMISSION_EFFICIENCY = 0.6
COLLECTOR_NUMBER = 5
TRANSMISSION_DIAMETER = 5 * 760e-6 
SOLAR_FLUX = 1361 
NUMBER_CABLES = 19 
LENGTH_TRANSMISSION = 0.5
TRANSMISSION_DENSITY = 2650

# TANKS
WATER_DENSITY = 1000
TANK_YIELD_STRESS = 90e6 
TANK_DENSITY = 2700 
TANK_SF = 2
TANK_RADIUS = 0.05
M_HELIUM = 4.002602e-3 
R_PRESSURANT_SPEC = RA/M_HELIUM
GAMMA_HELIUM = 1.66
RATIO_BLOW_DOWN = 2


default_cone_params = {
    'radius': CONE_RADIUS,
    'length': CONE_LENGTH,
    'thickness': CONE_THICKNESS,
    'density': RHENIUM_DENSITY,
    'c_p': RHENIUM_C_P,
    'thermal_cond': RHENIUM_THERMAL_CONDUCTIVITY,
    'temp_max': T_MAX_RHENIUM,
    'mdot': None,  # Initial MDOT
    'storage_temp': STORAGE_TEMP,
    't_channel': CHANNEL_THICKNESS,
    'thickness_outer': CONE_OUTER_WALL_THICKNESS,
}

default_nozzle_params = {
    'delta_v': DELTA_V,
    'sc_mass_max': SC_MASS_MAX,
    'gamma': GAMMA,
    'ra': RA,
    'm': M,
    'time_burn': TIME_BURN,
    'at': None,  # To be set in the loop
    'ae': None,  # To be set in the loop
    'Tc': None,  # To be updated based on Cone
    'divergence_angle': ANGLE_DIVERGENCE,
    'nozzle_density': NOZZLE_DENSITY,
    'nozzle_ultimate_strength': NOZZLE_ULTIMATE_STRENGTH,
    'SF': NOZZLE_SF,
}


default_collector_params = {
    'power_to_receiver': None,  # Example value, adjust as needed
    'transmission_efficiency': TRANSMISSION_EFFICIENCY,  # Transmission efficiency
    'collector_number': COLLECTOR_NUMBER,  # Number of collectors
    'transmission_diameter_bundle': TRANSMISSION_DIAMETER,  # Diameter in meters
    'solar_flux': SOLAR_FLUX,  # Solar constant, W/m^2
    'number_of_cables': NUMBER_CABLES,  # Number of transmission cables
    'transmission_length': LENGTH_TRANSMISSION,  # Length of transmission in meters
    'density_cable': TRANSMISSION_DENSITY  # Density of transmission material, kg/m^3
}

# Default parameters for the Tanks
default_tanks_params = {
    'propellant_mass': None,  # Propellant mass, kg
    'propellant_density': WATER_DENSITY,  # Density of water, kg/m^3
    'yield_stress': TANK_YIELD_STRESS,  # Yield stress of tank material, Pa
    'tank_density': TANK_DENSITY,  # Density of tank material, kg/m^3
    'SF': TANK_SF,  # Safety factor
    'tank_radius': TANK_RADIUS,  # Radius of tank, m
    'R_spec_press': R_PRESSURANT_SPEC,  # Specific gas constant for pressurant, J/(kg*K)
    'T_press_initial': STORAGE_TEMP,  # Storage temperature, K
    'gamma': GAMMA_HELIUM,  # Specific heat ratio for helium
    'init_guess': None,  # Initial guess for pressurant pressure, Pa
    'bounds': None,  # Bounds for optimization, Pa
    'pc': None  # Chamber pressure, Pa
}
