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
        self.tbit = 0.2 / self.F_compl  # 200mNs = Ft * tbit
        self.divergence_angle = divergence_angle
        self.nozzle_density = nozzle_density
        self.nozzle_ultimate_strength = nozzle_ultimate_strength
        self.SF = SF
        self.nozzle_thickness = self.t_nozzle() 
        self.nozzle_corrected = "Thickness nozzle not too small to manufacture"
        self.rt = np.sqrt(self.ae / np.pi)

    def t_nozzle(self):
        radius_throat = np.sqrt(self.at/np.pi)
        radius_exit = np.sqrt(self.ae/np.pi)
        return (self.pc * (radius_exit + radius_throat) * self.SF) / (2 * self.nozzle_ultimate_strength)

    def mass_total(self):
        # s = (radius_exit - radius_throat) / np.arcsin(self.divergence_angle)
        # S_lat = np.pi * (radius_exit + radius_throat) * s
        # t_nozzle = (self.pc * (radius_exit + radius_throat) * self.SF) / (2 * self.nozzle_ultimate_strength)
        area_lat = self.at * ( (self.ae_at_ratio-1)/np.sin(self.divergence_angle) )

        # left = self.nozzle_density * self.SF / self.nozzle_ultimate_strength # NO K_Loads
        # brackets = (self.at * ( (self.ae_at_ratio-1)/np.sin(self.divergence_angle) ) * ((self.pc * (radius_exit + radius_throat)) / 2)  )
        # return left * brackets
        if self.nozzle_thickness < 0.005:
            self.nozzle_thickness = 0.005
            self.nozzle_corrected = "Thickness nozzle too small to manufacture, was made 5 mm, such that regenerative cooling can be used"
        return self.nozzle_thickness * area_lat * self.nozzle_density
    


        








