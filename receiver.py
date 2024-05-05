import numpy as np

class Cone():
    def __init__(self, radius, length, thickness, density, c_p, thermal_cond, temp_max, mdot, storage_temp, t_channel, thickness_outer):
        self.radius = radius
        self.length = length
        self.thickness = thickness
        self.density = density
        self.c_p = c_p
        self.thermal_cond = thermal_cond
        self.temp_max = temp_max
        self.t_channel = t_channel
        self.thickness_outer = thickness_outer

        self.area_lateral = self.radius * np.pi * np.sqrt(self.radius**2 + self.length**2)
        self.volume = self.area_lateral * self.thickness
        self.mass = self.volume*self.density
        
        self.Tc = (self.temp_max + (self.thickness * mdot * self.c_p * storage_temp) / (self.thermal_cond * self.area_lateral)) / (1 + self.thickness * mdot * self.c_p / (self.thermal_cond * self.area_lateral))
        self.power_to_prop = mdot * self.c_p * (self.Tc - storage_temp)
        # self.Tc_lin = self.temp_max - (self.power_to_prop*self.thickness)/(self.thermal_cond*self.area_lateral)


    def mass_lateral_outer(self, R_t):
        base = self.radius + self.thickness + self.t_channel- R_t
        height = self.length
        S_lat_outer = np.pi * base * np.sqrt(base**2 + height**2)
        return S_lat_outer * self.thickness_outer * self.density
    
    def mass_total(self, R_t):
        self.total_mass_all = self.mass + self.mass_lateral_outer(R_t)
        return self.total_mass_all
    
    
    
        

    


