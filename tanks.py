import numpy as np

class Tanks():
    def __init__(self, propellant_mass, propellant_density, yield_stress, tank_density, SF, tank_radius):
        self.propellant_mass = propellant_mass
        self.propellant_density = propellant_density
        self.propellant_volume = propellant_mass / (0.9* propellant_density)  # 10 % ullage

        # get radius sphere? then see if sphere is too large, if so, get cylinder, assume a length?, for thickness use hoop stress

        self.yield_stress = yield_stress
        self.SF = SF
        self.tank_density = tank_density
        self.tank_radius = tank_radius
        self.tank_length = (self.propellant_volume - ((4/3) * np.pi * self.tank_radius**3)) / (np.pi * self.tank_radius** 2)
        self.total_tank_length = self.tank_length + 2 * self.tank_radius

        

    def tank_thickness(self, pc):
        t = pc * self.tank_radius / self.yield_stress
        if t < 0.001:
            t = 0.001
        self.t_tank = t
        return t
    
    def total_mass_propellant_tank(self, pc):
        surface_area = 2*np.pi*self.tank_radius*self.tank_length + 4 * np.pi * self.tank_radius**2    
        mass = self.tank_thickness(pc)* self.SF * surface_area
        self.propellant_tank_mass = mass
        return mass
    
    def total_mass_pressurant(self, pc, V_prop, R, T_press_initial, gamma):
        ...
        
        return mass
    
    # def pressurant_tank_thickness(self, pc):
    #     t = pc * self.tank_radius / self.yield_stress
    #     if t < 0.001:
    #         t = 0.001
    #     self.t_pressurant_tank = t
    #     return t
    # def total_mass_pressurant_tank(self, pc):
    #     surface_area = 2*np.pi*self.tank_radius*self.tank_length + 4 * np.pi * self.tank_radius**2    
    #     mass = self.pressurant_tank_thickness(pc)* self.SF * surface_area
    #     self.pressurant_tank_mass = mass
    #     return mass
    
    
    
    
    