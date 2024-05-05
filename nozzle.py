import numpy as np
from scipy.optimize import fsolve



class Nozzle():
    def __init__(self, delta_v, sc_mass_max, gamma, ra, m, time_burn, at, ae, Tc, divergence_angle, nozzle_density, nozzle_ultimate_strength, SF):
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

        
        self.pe_pc_ratio = fsolve(self.pe_pc_ratio_func, 0.000000001)[0]

        self.Ue = np.sqrt((2*self.gamma*self.r*self.Tc/(self.gamma-1)) * (1 - (self.pe_pc_ratio)**((self.gamma-1)/self.gamma)))
        self.mp = self.sc_mass_max  - self.sc_mass_max * (np.exp(-self.delta_v/self.Ue))
        self.m_dot = self.mp/self.time_burn
        self.pc = self.m_dot * np.sqrt(self.r * self.Tc) / (self.vandenkerckhove * self.at)
        self.pe = self.pe_pc_ratio * self.pc

        # self.Ue = np.sqrt((2*self.gamma*self.r*self.Tc/(self.gamma-1)) * (1 - (self.pe_pc_ratio)**((self.gamma-1)/self.gamma)))
        self.F_compl = self.m_dot * self.Ue + (self.pe) * self.ae
        self.tbit = 0.2 / self.F_compl  # 200mNs = Ft * tbit
        self.divergence_angle = divergence_angle
        self.nozzle_density = nozzle_density
        self.nozzle_ultimate_strength = nozzle_ultimate_strength
        self.SF = SF
        
        self.nozzle_corrected = "Thickness nozzle not too small to manufacture"
        self.nozzle_thickness = self.t_nozzle() 
        self.rt = np.sqrt(self.at / np.pi)

    def pe_pc_ratio_func(self, x):
        return self.vandenkerckhove / np.sqrt( (2*self.gamma / (self.gamma-1)) * (x)**(2/self.gamma) * (1- (x)**((self.gamma-1)/self.gamma))) - self.ae_at_ratio

    def t_nozzle(self):
        radius_throat = np.sqrt(self.at/np.pi)
        radius_exit = np.sqrt(self.ae/np.pi)
        t = (self.pc * (radius_exit + radius_throat) * self.SF) / (2 * self.nozzle_ultimate_strength)
        if t < 0.005:
            t = 0.005
            self.nozzle_corrected = "Thickness nozzle too small to manufacture, was made 5 mm, such that regenerative cooling can be used"
        return t

    def mass_total(self):
        area_lat = self.at * ( (self.ae_at_ratio-1)/np.sin(self.divergence_angle) )
        self.total_mass_all = self.nozzle_thickness * area_lat * self.nozzle_density
        return self.total_mass_all
    
 

        








