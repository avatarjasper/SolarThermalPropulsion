import numpy as np
from scipy.optimize import fsolve




class NozzleA():
    def __init__(self, delta_v, sc_mass_max, gamma, ra, m, time_burn, at, ae, Tc):
        self.delta_v = delta_v
        self.sc_mass_max = sc_mass_max
        self.gamma = gamma
        self.ra = ra
        self.m = m
        self.r = self.ra/self.m
        self.time_burn = time_burn
        self.Tc = Tc
        self.vandenkerckhove = np.sqrt(self.gamma) * (2/(self.gamma+1))**((self.gamma+1) / (2*(self.gamma-1)))
        self.at = at
        self.ae = ae
        self.ae_at_ratio = self.ae/self.at

        def pe_pc_ratio_func(x):
            return self.vandenkerckhove / np.sqrt( (2*self.gamma / (self.gamma-1)) * (x)**(2/self.gamma) * (1- (x)**((self.gamma-1)/self.gamma))) - self.ae_at_ratio
        self.pe_pc_ratio = fsolve(pe_pc_ratio_func, 0.0000001)[0]
        self.Ue = np.sqrt((2*self.gamma*self.r*self.Tc/(self.gamma-1)) * (1 - (self.pe_pc_ratio)**((self.gamma-1)/self.gamma)))
        self.mp = self.sc_mass_max  - self.sc_mass_max * (np.exp(-self.delta_v/self.Ue))
        self.m_dot = self.mp/self.time_burn
        self.pc = self.m_dot * np.sqrt(self.r * self.Tc) / (self.vandenkerckhove * self.at)
        self.pe = self.pe_pc_ratio * self.pc

        self.Ue = np.sqrt((2*self.gamma*self.r*self.Tc/(self.gamma-1)) * (1 - (self.pe_pc_ratio)**((self.gamma-1)/self.gamma)))
        self.F_compl = self.m_dot * self.Ue + (self.pe) * self.ae

a = NozzleA(200, 24, 1.33, 8.31446261815324, 18.01528e-3, 8*3600, 8e-6, 160e-6, 3000)
attrs = vars(a)
# {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
# now dump this in some way or another
print(', '.join("%s: %s" % item for item in attrs.items()))

        



# class NozzleMP():
#     def __init__(self, delta_v, propellant_mass, sc_mass_max, gamma, ra, m, time_burn, at, Tc):
#         self.delta_v = delta_v
#         self.propellant_mass = propellant_mass
#         self.sc_mass_max = sc_mass_max
#         self.gamma = gamma
#         self.ra = ra
#         self.m = m
#         self.r = self.ra/self.m
#         self.time_burn = time_burn
#         self.Tc = Tc
#         self.Ue = self.delta_v / (np.log(self.sc_mass_max/(self.sc_mass_max - self.propellant_mass)))
#         self.isp = self.Ue/9.81
#         self.m_dot = self.propellant_mass/self.time_burn
#         self.vandenkerckhove = np.sqrt(self.gamma) * (2/(self.gamma+1))**((self.gamma+1) / (2*(self.gamma-1)))

#         self.pe_pc_ratio = (1-((self.Ue**2 * (self.gamma-1) * self.m)/(2 * self.gamma * self.ra * Tc)))**(self.gamma/(self.gamma-1)) 

#         self.at = at
#         self.ae_at_ratio = self.vandenkerckhove / np.sqrt( (2*self.gamma / (self.gamma-1)) * (self.pe_pc_ratio)**(2/self.gamma) * (1- (self.pe_pc_ratio)**((self.gamma-1)/self.gamma)))
#         self.ae = self.at * self.ae_at_ratio
#         self.pc = self.m_dot * np.sqrt(self.r * self.Tc) / (self.vandenkerckhove * self.at)
#         self.pe = self.pe_pc_ratio * self.pc
#         self.F_compl = self.m_dot * self.Ue + (self.pe) * self.ae

# a = NozzleMP(200, 1.595, 24, 1.33, 8.31446261815324, 18.01528e-3, 8*3600, 8e-6, 3000)
# attrs = vars(a)
# # {'kids': 0, 'name': 'Dog', 'color': 'Spotted', 'age': 10, 'legs': 2, 'smell': 'Alot'}
# # now dump this in some way or another
# print(', '.join("%s: %s" % item for item in attrs.items()))

        





