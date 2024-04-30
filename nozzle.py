import numpy as np
from scipy.optimize import fsolve



class Nozzle():
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

        








