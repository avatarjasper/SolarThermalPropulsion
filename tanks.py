import numpy as np

class Tanks():
    def __init__(self, propellant_mass, propellant_density, yield_stress, tank_density, SF):
        self.propellant_mass = propellant_mass
        self.propellant_density = propellant_density
        self.propellant_volume = propellant_mass / (0.9* propellant_density)  # 10 % ullage

        # get radius sphere? then see if sphere is too large, if so, get cylinder, assume a length?, for thickness use hoop stress

        self.yield_stress = yield_stress
        self.SF = SF
        self.t_tank = self.tank_thickness()

    def tank_thickness(self):
        return 