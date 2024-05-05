import numpy as np
from scipy.optimize import minimize

class Tanks():
    def __init__(self, propellant_mass, propellant_density, yield_stress, tank_density, SF, tank_radius, R_spec_press, T_press_initial, gamma, init_guess, bounds, pc):
        self.propellant_mass = propellant_mass
        self.propellant_density = propellant_density
        self.propellant_volume = propellant_mass / (0.9* propellant_density)  # 10 % ullage

        self.R_spec_press = R_spec_press
        self.T_press_initial = T_press_initial
        self.gamma = gamma
        self.init_guess = init_guess
        self.bounds = bounds
        self.pc = pc    
        

        # get radius sphere? then see if sphere is too large, if so, get cylinder, assume a length?, for thickness use hoop stress

        self.yield_stress = yield_stress
        self.SF = SF
        self.tank_density = tank_density
        self.tank_radius = tank_radius

        # put a check for sphere or cylinder
        self.tank_length = (self.propellant_volume - ((4/3) * np.pi * self.tank_radius**3)) / (np.pi * self.tank_radius** 2) # THIS ALREADY ASSUMES CYLINDER...
        self.total_tank_length = self.tank_length + 2 * self.tank_radius




    # PROPELLANT
    def tank_thickness(self):
        t = self.pc * self.tank_radius / self.yield_stress
        if t < 0.001:
            t = 0.001
        t = t * self.SF
        self.t_tank = t 
        return t 
    
    def total_mass_propellant_tank(self):
        surface_area = 2*np.pi*self.tank_radius*self.tank_length + 4 * np.pi * self.tank_radius**2 
        self.propellant_tank_mass = self.tank_thickness() * surface_area
        return self.propellant_tank_mass
    
    

    # PRESSURANT
    def pressurant_mass_obj_func(self, po):
        Mpress = self.pc * self.propellant_volume * self.gamma / (self.R_spec_press * self.T_press_initial * (1 - (self.pc/po)))
        return Mpress
    
    def total_mass_pressurant(self):
        result = minimize(self.pressurant_mass_obj_func, self.init_guess, bounds=self.bounds)
        self.initial_pressurization_tank_pressure = result.x[0]
        self.mass_pressurant = result.fun
        self.pressurant_density = self.initial_pressurization_tank_pressure / (self.R_spec_press * self.T_press_initial)
        self.pressurant_volume = self.mass_pressurant / self.pressurant_density
        self.pressurant_tank_radius =  ((3/(4* np.pi))  * self.pressurant_volume)**(1/3)
        return self.mass_pressurant


    def pressurant_tank_thickness(self):
        t = self.initial_pressurization_tank_pressure * self.pressurant_tank_radius / self.yield_stress
        if t < 0.001:
            t = 0.001
        t = t * self.SF
        self.t_pressurant_tank = t
        return t


    def total_mass_pressurant_tank(self):
        _ = self.total_mass_pressurant()
        self.pressurant_tank_thickness()
        surface_area = 4 * np.pi * self.pressurant_tank_radius**2    
        mass = self.t_pressurant_tank * surface_area
        self.pressurant_tank_mass = mass
        return mass
    
    def total_mass(self):
        self.total_mass_propellant_tank()
        self.total_mass_pressurant_tank()
        self.total_mass_all = self.propellant_tank_mass + self.pressurant_tank_mass + self.mass_pressurant + self.propellant_mass
        return self.total_mass_all
    

    
    
    
    
    