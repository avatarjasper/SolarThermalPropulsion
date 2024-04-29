import numpy as np

class Collector():
    def __init__(self, power_to_receiver, transmission_efficiency, collector_number, transmission_diameter, solar_flux):
        self.power_to_receiver = power_to_receiver
        self.transmission_efficiency = transmission_efficiency
        self.collector_number = collector_number
        self.transmission_diameter = transmission_diameter
        self.solar_flux = solar_flux

        self.power_to_transmission_each = self.power_to_receiver/(self.transmission_efficiency*self.collector_number)

        self.flux_in_transmission = self.power_to_transmission_each/(np.pi * (self.transmission_diameter/2)**2)
        self.concentration_ratio = self.flux_in_transmission/self.solar_flux
        


TRANSMISSION_EFFICIENCY = 0.8

COLLECTOR_NUMBER = 5


sf_to_transmission_each = sf_to_receiver/(TRANSMISSION_EFFICIENCY*COLLECTOR_NUMBER)
print(f'{sf_to_transmission_each=}')


TRANSMISSION_DIAMETER = 760e-6 # m
TRANSMISSION_CORE_AREA = np.pi * (TRANSMISSION_DIAMETER/2)**2
print(TRANSMISSION_CORE_AREA)

SOLAR_FLUX = 1361 # W/m^2


concentration_ratio = sf_to_transmission_each/SOLAR_FLUX

collector_area = TRANSMISSION_CORE_AREA * concentration_ratio
print(f'{collector_area=}')
print(np.sqrt(collector_area/np.pi))
print(np.sqrt(collector_area/np.pi))
print(concentration_ratio) 

