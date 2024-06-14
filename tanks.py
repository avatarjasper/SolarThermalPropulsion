import numpy as np
from scipy.optimize import minimize

class Tanks():
    def __init__(self, propellant_mass, propellant_density, yield_stress, tank_density, SF, tank_radius, R_spec_press, T_press_initial, gamma, init_guess, bounds, pc):
        self.propellant_mass = propellant_mass
        self.propellant_density = propellant_density
        self.propellant_volume = propellant_mass / (0.9* propellant_density)  # 10 % ullage
        # R_spec_water = 8.314462 / 0.01801528
        # self.propellant_volume = propellant_mass * R_spec_water * T_press_initial / pc

        self.R_spec_press = R_spec_press
        self.T_press_initial = T_press_initial
        self.gamma = gamma
        self.init_guess = init_guess
        self.bounds = bounds
        self.pc = pc    
        


        self.yield_stress = yield_stress
        self.SF = SF
        self.tank_density = tank_density
        self.tank_radius = tank_radius
        self.tank_length = (self.propellant_volume - ((4/3) * np.pi * self.tank_radius**3)) / (np.pi * self.tank_radius** 2) 
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
        self.propellant_tank_mass = self.tank_thickness() * surface_area * self.tank_density
        return self.propellant_tank_mass
    
    

    # PRESSURANT
    def pressurant_mass_obj_func(self, po):
        Mpress = self.pc * self.propellant_volume * self.gamma / (self.R_spec_press * self.T_press_initial * (1 - (self.pc/po)))
        return Mpress
    
    def total_mass_pressurant(self):
        result = minimize(self.pressurant_mass_obj_func, self.init_guess, bounds=self.bounds)
        self.initial_pressurization_tank_pressure = result.x[0]
        self.mass_pressurant = result.fun
        self.pressurant_density = 0.1598
        self.pressurant_volume = self.mass_pressurant / self.pressurant_density
        self.pressurant_tank_radius =  ((3/(4* np.pi))  * self.pressurant_volume)**(1/3)
        return self.mass_pressurant


    def pressurant_tank_thickness(self):
        t = self.initial_pressurization_tank_pressure * self.pressurant_tank_radius / (2 * self.yield_stress)
        if t < 0.001:
            t = 0.001
        t = t * self.SF
        self.t_pressurant_tank = t
        return t


    def total_mass_pressurant_tank(self):
        _ = self.total_mass_pressurant()
        self.pressurant_tank_thickness()
        surface_area = 4 * np.pi * self.pressurant_tank_radius**2    
        vol = self.t_pressurant_tank * surface_area
        self.pressurant_tank_mass = vol*self.tank_density 
        return self.pressurant_tank_mass
    
    def total_mass_regulated(self):
        self.total_mass_propellant_tank()
        self.total_mass_pressurant_tank()
        self.total_mass_all = self.propellant_tank_mass + self.pressurant_tank_mass + self.mass_pressurant + self.propellant_mass
        return self.total_mass_all
    


    def total_mass_blow_down(self, _ratio):
        R = _ratio 
        pressurant_volume = R * self.propellant_volume - self.propellant_volume
        total_volume = pressurant_volume + self.propellant_volume
        self.total_volume_blow_down = total_volume
        self.pressurant_mass_blow_down = (self.pc * total_volume) / (self.R_spec_press * self.T_press_initial)
        
        total_mass_gas_blow_down = self.pressurant_mass_blow_down + self.propellant_mass
        pressure_init = self.pc*R
        tank_radius =  ((3/(4* np.pi))  * total_volume)**(1/3)
        
        self.tank_radius_blow_down = tank_radius

        thickness = pressure_init * tank_radius / (2 * self.yield_stress)
        if thickness < 0.001:
            thickness = 0.001
        thickness = thickness * self.SF
        
        self.thickness_tank_blow_down = thickness  
        surface_area = 4 * np.pi * tank_radius**2   
        self.tank_mass_blow_down = surface_area * thickness *self.tank_density
        self.total_mass_blowdown = self.tank_mass_blow_down + total_mass_gas_blow_down 
        return self.total_mass_blowdown


    
    
    
    
    