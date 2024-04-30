import numpy as np



T_MAX_GRAPHITE = 3500 # K
GRAPHITE_C_P = 707.7 # J/kgK
GRAPHITE_DENSITY = 2250 # kg/m^3
GRAPHITE_THERMAL_CONDUCTIVITY = 24.0 # W/mK

CONE_RADIUS = 0.05 # m
CONE_LENGTH = 0.075 # m
CONE_THICKNESS = 0.002 # m


cone_volume = np.pi * CONE_LENGTH* CONE_RADIUS**2 / 3

cone_mass = cone_volume*GRAPHITE_DENSITY

t_shine = 400 # s


energy_receiver = cone_mass * GRAPHITE_C_P * T_MAX_GRAPHITE
P_to_receiver = energy_receiver / t_shine

print(P_to_receiver)

CONE_AREA_LATERAL = CONE_RADIUS * np.sqrt(CONE_RADIUS**2 + CONE_LENGTH**2)

sf_to_receiver = P_to_receiver/CONE_AREA_LATERAL





Tc = T_MAX_GRAPHITE - (sf_to_receiver*CONE_THICKNESS)/(GRAPHITE_THERMAL_CONDUCTIVITY)
print(f'{Tc=}')


TRANSMISSION_EFFICIENCY = 0.8

COLLECTOR_NUMBER = 5


sf_to_transmission_each = sf_to_receiver/(TRANSMISSION_EFFICIENCY*COLLECTOR_NUMBER)
print(f'{sf_to_transmission_each=}')


TRANSMISSION_DIAMETER = 760e-6 # m
TRANSMISSION_CORE_AREA = np.pi * (TRANSMISSION_DIAMETER/2)**2
print(TRANSMISSION_CORE_AREA)

SOLAR_FLUX = 1361 # W/m^2


concentration_ratio = sf_to_transmission_each/SOLAR_FLUX

collector_area = TRANSMISSION_CORE_AREA * concentration_ratio
print(f'{collector_area=}')
print(np.sqrt(collector_area/np.pi))
print(np.sqrt(collector_area/np.pi))
print(concentration_ratio) 

DELTA_V = 200 # m/s (at least)
PROPELLANT_MASS = 2 # kg
SC_MASS_MAX = 24 # kg
w = DELTA_V / (np.log(SC_MASS_MAX/(SC_MASS_MAX - PROPELLANT_MASS)))
isp = w/9.81
print(f'{w=}')

GAMMA = 1.33
RA = 8.31446261815324
M = 18.01528e-3 # kg/mol
pe_pc_ratio = (1-((w**2 * (GAMMA-1) * M)/(2 * GAMMA * RA * Tc)))**(GAMMA/(GAMMA-1)) 
print(f'{pe_pc_ratio=}')

pc = 0.15e5 # Pa

pe = pe_pc_ratio * pc

print(f'{pe=}')

TIME_BURN = 8 * 3600 # s

R = RA/M

m_dot = PROPELLANT_MASS/TIME_BURN
print(f'{m_dot=}')
print(f'{m_dot*1000=}')

def vandenkerckhove_func(_gamma):
    return np.sqrt(_gamma) * (2/(_gamma+1))**((_gamma+1) / (2*(_gamma-1)))

vandenkerckhove = vandenkerckhove_func(GAMMA)
print(f'{vandenkerckhove=}')

At = m_dot * np.sqrt(R*Tc) / (pc * vandenkerckhove)
print(At)
print(At*1e6)

print(np.sqrt(At/np.pi))

# iteration for Area ratio
denominator = np.sqrt( (2*GAMMA / (GAMMA-1)) * (pe_pc_ratio)**(2/GAMMA) * (1- (pe_pc_ratio)**((GAMMA-1)/GAMMA))  )

Ae_At_ratio = vandenkerckhove / denominator

print(f'{Ae_At_ratio=}')

Ae = At * Ae_At_ratio

print(f'{Ae=}')
print(f'{np.sqrt(Ae/np.pi)=}')

# F = m_dot *   














# DELTA_V = 200 # m/s (at least)
# PROPELLANT_MASS = 2 # kg
# SC_MASS_MAX = 24 # kg
# w = DELTA_V / (np.log(SC_MASS_MAX/(SC_MASS_MAX - PROPELLANT_MASS)))
# isp = w/9.81
# print(f'{w=}')

# GAMMA = 1.33
# RA = 8.31446261815324
# M = 18.01528e-3 # kg/mol
# pe_pc_ratio = (1-((w**2 * (GAMMA-1) * M)/(2 * GAMMA * RA * Tc)))**(GAMMA/(GAMMA-1)) 
# print(f'{pe_pc_ratio=}')

# pc = 0.15e5 # Pa

# pe = pe_pc_ratio * pc

# print(f'{pe=}')

# TIME_BURN = 8 * 3600 # s

# R = RA/M

# m_dot = PROPELLANT_MASS/TIME_BURN
# print(f'{m_dot=}')
# print(f'{m_dot*1000=}')

# def vandenkerckhove_func(_gamma):
#     return np.sqrt(_gamma) * (2/(_gamma+1))**((_gamma+1) / (2*(_gamma-1)))

# vandenkerckhove = vandenkerckhove_func(GAMMA)
# print(f'{vandenkerckhove=}')

# At = m_dot * np.sqrt(R*Tc) / (pc * vandenkerckhove)
# print(At)
# print(At*1e6)

# print(np.sqrt(At/np.pi))

# # iteration for Area ratio
# denominator = np.sqrt( (2*GAMMA / (GAMMA-1)) * (pe_pc_ratio)**(2/GAMMA) * (1- (pe_pc_ratio)**((GAMMA-1)/GAMMA))  )

# Ae_At_ratio = vandenkerckhove / denominator

# print(f'{Ae_At_ratio=}')

# Ae = At * Ae_At_ratio

# print(f'{Ae=}')
# print(f'{np.sqrt(Ae/np.pi)=}')

# # F = m_dot * 






class Nozzle():
    def __init__(self, delta_v, propellant_mass, sc_mass_max, gamma, ra, m, time_burn, at, ae, Tc):
        self.delta_v = delta_v
        self.propellant_mass = propellant_mass
        self.sc_mass_max = sc_mass_max
        self.gamma = gamma
        self.ra = ra
        self.m = m
        self.r = self.ra/self.m
        self.time_burn = time_burn
        self.Tc = Tc
        self.w = self.delta_v / (np.log(self.sc_mass_max/(self.sc_mass_max - self.propellant_mass)))
        self.isp = self.w/9.81
        self.m_dot = self.propellant_mass/self.time_burn
        self.vandenkerckhove = np.sqrt(self.gamma) * (2/(self.gamma+1))**((self.gamma+1) / (2*(self.gamma-1)))
        self.at = at
        self.ae = ae
        self.ae_at_ratio = self.ae/self.at

        def pe_pc_ratio_func(x):
            return self.vandenkerckhove / np.sqrt( (2*self.gamma / (self.gamma-1)) * (x)**(2/self.gamma) * (1- (x)**((self.gamma-1)/self.gamma))) - self.ae_at_ratio
        self.pe_pc_ratio = fsolve(pe_pc_ratio_func, 0.0000001)[0]
        self.pc = self.m_dot * np.sqrt(self.r * self.Tc) / (self.vandenkerckhove * self.at)
        self.pe = self.pe_pc_ratio * self.pc
        self.F_simp = self.m_dot * self.w
        self.Ue = np.sqrt((2*self.gamma*self.r*self.Tc/(self.gamma-1)) * (1 - (self.pe_pc_ratio)**((self.gamma-1)/self.gamma)))
        self.F_compl = self.m_dot * self.Ue + (self.pe) * self.ae

a = Nozzle(200, 2, 24, 1.33, 8.31446261815324, 18.01528e-3, 8*3600, 8e-6, 160e-6, 3000)

print(a.Ue)
print(a.F_simp)
print(a.F_compl)
print(a.m_dot)

attrs = vars(a)
# {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
# now dump this in some way or another
print(', '.join("%s: %s" % item for item in attrs.items()))

        







