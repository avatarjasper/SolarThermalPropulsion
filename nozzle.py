import numpy as np




class nozzle():
    def __init__(self, delta_v, propellant_mass, sc_mass_max, gamma, ra, m, time_burn, w, isp, pe_pc_ratio, pe,  vandenkerckhove, at, ae_at_ratio, ae):
        self.delta_v = delta_v
        self.propellant_mass = propellant_mass
        self.sc_mass_max = sc_mass_max
        self.gamma = gamma
        self.ra = ra
        self.m = m
        self.time_burn = time_burn
        self.w = w
        self.isp = isp
        self.pe_pc_ratio = pe_pc_ratio
        self.pe = pe
        self.m_dot = 
        self.vandenkerckhove = vandenkerckhove
        self.at = at
        self.ae_at_ratio = ae_at_ratio
        self.ae = ae
        











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