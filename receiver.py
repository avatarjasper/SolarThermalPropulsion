import numpy as np

class Cone():
    def __init__(self, radius, length, thickness, density, c_p, thermal_cond, temp_max, mdot, storage_temp, temp_gas):
        self.radius = radius
        self.length = length
        self.thickness = thickness
        self.density = density
        self.c_p = c_p
        self.thermal_cond = thermal_cond
        self.temp_max = temp_max
        self.temp_gas = temp_gas

        self.volume = np.pi * self.length* self.radius**2 / 3
        self.mass = self.volume*self.density
        self.area_lateral = self.radius * np.sqrt(self.radius**2 + self.length**2)

        # self.power_to_prop = mdot * self.c_p * (self.temp_gas - storage_temp)
        self.Tc = (self.temp_max + (self.thickness * mdot * self.c_p * storage_temp) / (self.thermal_cond * self.area_lateral)) / (1 + self.thickness * mdot * self.c_p / (self.thermal_cond * self.area_lateral))
        
        # self.Tc_lin = self.temp_max - (self.power_to_prop*self.thickness)/(self.thermal_cond*self.area_lateral)

    


