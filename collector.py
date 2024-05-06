import numpy as np

class Collector():
    def __init__(self, power_to_receiver, transmission_efficiency, collector_number, transmission_diameter_bundle, solar_flux, number_of_cables, transmission_length, density_cable):
        self.power_to_receiver = power_to_receiver
        self.transmission_efficiency = transmission_efficiency
        self.collector_number = collector_number
        self.transmission_diameter_bundle = transmission_diameter_bundle
        self.solar_flux = solar_flux

        self.power_to_transmission_each_bundle = self.power_to_receiver/(self.transmission_efficiency*self.collector_number)

        self.flux_in_transmission_bundle = self.power_to_transmission_each_bundle/(np.pi * (self.transmission_diameter_bundle/2)**2)
        self.concentration_ratio = self.flux_in_transmission_bundle/self.solar_flux
        self.collector_area = self.concentration_ratio * np.pi * (self.transmission_diameter_bundle/2)**2
        self.collector_diameter = np.sqrt(self.collector_area/np.pi)

        self.number_of_cables = number_of_cables
        self.transmission_length = transmission_length
        self.density_cable = density_cable

    def mass_parabolic(self):
        density = 1213  # kg/m^3  from 6fda-apb
        thickness = 0.002 # m
        structure_density = 2800 # kg/m^3 from aluminium
        structure_thickness = 0.005 # m
        return ((self.collector_area * thickness * density + self.collector_area*structure_density*structure_thickness) * 1.2) * self.collector_number # 1.2 for the cassegrain configuration and parabolic is harder to manufacture.
    

    def mass_fresnel(self):
        density = 1420 # kg/m^3  from kapton 300 jp film
        thickness = 0.002 # m
        return (self.collector_area * thickness * density * 2) * self.collector_number # 2 for the struts
    
    def mass_spherical(self):
        density = 1213  # kg/m^3  from 6fda-apb
        thickness = 0.002 # m
        structure_density = 2800 # kg/m^3 from aluminium
        structure_thickness = 0.02 # m
        return ((self.collector_area * thickness * density + self.collector_area*structure_density*structure_thickness) * 1.1)* self.collector_number # 1.1 for the cassegrain configuration.
    

    def mass_total_collector(self):
        if self.concentration_ratio > 1000:
            self.collector = 'parabolic'
            return self.mass_parabolic()
        if (self.concentration_ratio <= 1000) and (self.concentration_ratio > 150):
            if self.mass_fresnel() < self.mass_parabolic():
                self.collector = 'fresnel'
                return self.mass_fresnel()
            else:
                self.collector = 'parabolic'
                return self.mass_parabolic()
        if self.concentration_ratio <= 150:
            if self.mass_fresnel() < self.mass_spherical():
                self.collector = 'fresnel'
                return self.mass_fresnel()
            else:
                self.collector = 'spherical'
                return self.mass_spherical()
        

    def mass_total_transmission(self):
        area = np.pi * (self.transmission_diameter_bundle/2)**2
        mass_transmission = self.transmission_length * self.density_cable * area
        return mass_transmission * self.collector_number
        
    def mass_total(self):
        self.total_mass_all = self.mass_total_collector() + self.mass_total_transmission()
        return self.total_mass_all




# TRANSMISSION_EFFICIENCY = 0.8

# COLLECTOR_NUMBER = 5


# sf_to_transmission_each = sf_to_receiver/(TRANSMISSION_EFFICIENCY*COLLECTOR_NUMBER)
# print(f'{sf_to_transmission_each=}')


# TRANSMISSION_DIAMETER = 760e-6 # m
# TRANSMISSION_CORE_AREA = np.pi * (TRANSMISSION_DIAMETER/2)**2
# print(TRANSMISSION_CORE_AREA)

# SOLAR_FLUX = 1361 # W/m^2


# concentration_ratio = sf_to_transmission_each/SOLAR_FLUX

# collector_area = TRANSMISSION_CORE_AREA * concentration_ratio
# print(f'{collector_area=}')
# print(np.sqrt(collector_area/np.pi))
# print(np.sqrt(collector_area/np.pi))
# print(concentration_ratio) 

