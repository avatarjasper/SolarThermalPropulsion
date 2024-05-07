import unittest
from receiver import Cone
from nozzle import Nozzle
from collector import Collector
from tanks import Tanks
import numpy as np

class TestReceiver(unittest.TestCase):
    def setUp(self):
        self.cone = Cone(0.5, 1, 0.002, 2250, 707, 24, 3500, 0.0001, 300, 0.005, 0.01)
        self.rt = 0.001
    def test_area_lateral(self):
        self.assertAlmostEqual(self.cone.area_lateral, 1.756203683, 5, "Later area is not correct")
    def test_volume(self):
        self.assertAlmostEqual(self.cone.volume, 0.00351240736, 5, "Volume is not correct")
    def test_mass(self):
        self.assertAlmostEqual(self.cone.mass, 7.902916572, 5, "Mass is not correct")
    def test_Tc(self):
        self.assertAlmostEqual(self.cone.Tc, 3499.989265, 5, "Tc is not correct")
    def test_power_to_prop(self):
        self.assertAlmostEqual(self.cone.power_to_prop, 0.0707*(self.cone.Tc - 300), 5, "Power to prop is not correct")
    def test_mass_lateral_outer(self):
        self.assertAlmostEqual(self.cone.mass_lateral_outer(self.rt), 40.08519044 , 5, "Mass lateral outer is not correct")
    def test_mass_total(self):
        self.assertAlmostEqual(self.cone.mass_total(self.rt), 47.98810701, 5, "Total mass is not correct")
    

class TestNozzle(unittest.TestCase):
    def setUp(self):
        self.nozzle = Nozzle(200, 24, 1.33, 8.3, 18e-3, 8*3600, 0.0005, 0.05, 3499, 15*np.pi/180, 8190, 1375e6, 1.5)
    def test_r(self):
        self.assertAlmostEqual(self.nozzle.r, 461.1111111, 5, "r is not correct")
    def test_vandenkerckhove(self):
        self.assertAlmostEqual(self.nozzle.vandenkerckhove, 0.6726284075, 5, "vandenkerckhove is not correct")
    def test_ae_at_ratio(self):
        self.assertAlmostEqual(self.nozzle.ae_at_ratio, 100, 5, "ae_at_ratio is not correct")
    def test_pe_pc_ratio(self):
        self.assertAlmostEqual(self.nozzle.pe_pc_ratio_func(0.00001), 1302.300084, 3, "pe_pc_ratio is not correct")
    def test_Ue(self):
        self.assertAlmostEqual(self.nozzle.Ue, 3501.12411, 5, "Ue is not correct")
    def test_mp(self):
        self.assertAlmostEqual(self.nozzle.mp, 1.332564838, 5, "mp is not correct")
    def test_m_dot(self):
        self.assertAlmostEqual(self.nozzle.m_dot, 0.00004626961, 5, "m_dot is not correct")
    def test_pc(self):
        self.assertAlmostEqual(self.nozzle.pc, 174.7533127, 5, "pc is not correct")
    def test_pe(self):
        self.assertAlmostEqual(self.nozzle.pe, 0.001747533127, 5, "pe is not correct")
    def test_F_compl(self):
        self.assertAlmostEqual(self.nozzle.F_compl, 0.1620830238, 3, "F_compl is not correct")
    def test_tbit(self):
        self.assertAlmostEqual(self.nozzle.tbit, 1.233935519, 3, "tbit is not correct")
    def test_nozzle_thickness(self):
        if self.nozzle.nozzle_corrected == "Thickness nozzle too small to manufacture, was made 5 mm, such that regenerative cooling can be used":
            self.assertAlmostEqual(self.nozzle.nozzle_thickness, 0.005, 5, "nozzle_thickness is not correct")
        else:
            self.assertAlmostEqual(self.nozzle.nozzle_thickness, 0.00000001322, 5, "nozzle_thickness is not correct")
    def test_rt(self):
        self.assertAlmostEqual(self.nozzle.rt, 0.01261566261, 3, "rt is not correct")
    def test_mass_total(self):
        self.assertAlmostEqual(self.nozzle.mass_total(), 7.831823192, 3, "mass_total is not correct")


class TestCollector(unittest.TestCase):
    def setUp(self):
        self.collector = Collector(100, 0.8, 5, 0.002, 1361, 19, 0.5, 2650)
    def test_power_to_transmission_each_bundle(self):
        self.assertAlmostEqual(self.collector.    power_to_transmission_each_bundle, 25, 5, "power_to_transmission_each_bundle is not correct")
    def test_flux_in_transmission_bundle(self):
        self.assertAlmostEqual(self.collector.flux_in_transmission_bundle, 7957747.155, 2, "flux_in_transmission_bundle is not correct")
    def test_concentration_ratio(self):
        self.assertAlmostEqual(self.collector.concentration_ratio,5846.985419, 5, "concentration_ratio is not correct")
    def test_collector_area(self):
        self.assertAlmostEqual(self.collector.collector_area, 0.01836884644, 5, "collector_area is not correct")
    def test_collector_diameter(self):
        self.assertAlmostEqual(self.collector.collector_diameter, 0.07646558323, 5, "collector_diameter is not correct")
    def test_mass_parabolic(self):
        self.assertAlmostEqual(self.collector.mass_parabolic(), 1.287861867, 5, "mass_parabolic is not correct")
    def test_mass_fresnel(self):
        self.assertAlmostEqual(self.collector.mass_fresnel(), 0.1043350478, 5, "mass_fresnel is not correct")
    def test_mass_spherical(self):
        self.assertAlmostEqual(self.collector.mass_spherical(), 1.180540045, 5, "mass_spherical is not correct")
    def test_mass_total_collector(self):
        self.assertAlmostEqual(self.collector.mass_total_collector(), 1.287861867, 5, "mass_total_collector is not correct")
    def test_mass_total_transmission(self):
        self.assertAlmostEqual(self.collector.mass_total_transmission(), 0.00416261026, 5, "mass_total_transmission is not correct")
    def test_mass_total(self):
        self.assertAlmostEqual(self.collector.mass_total(), 1.292024477, 5, "mass_total is not correct")


class TestTanks(unittest.TestCase):
    def setUp(self):
        self.tanks = Tanks(1, 1000, 90e6, 2700, 2, 0.05, 8.3, 300, 1.66, 200, [(174.7533127, 300e5)], 174)
    def test_propellant_volume(self):
        self.assertAlmostEqual(self.tanks.propellant_volume, 0.001111111111111, 5, "propellant_volume is not correct")
    def test_tank_length(self):
        self.assertAlmostEqual(self.tanks.tank_length, 0.07480439386, 5, "tank_length is not correct")
    def test_total_tank_length(self):
        self.assertAlmostEqual(self.tanks.total_tank_length, 0.1748043939, 5, "total_tank_length is not correct")
    def test_tank_thickness(self):
        _ = self.tanks.tank_thickness()
        if self.tanks.t_tank == 0.002:
            self.assertAlmostEqual(self.tanks.tank_thickness(), 0.002, 5, "tank_thickness is not correct")
        else:
            self.assertAlmostEqual(self.tanks.tank_thickness(), 0.00000009666, 3, "tank_thickness is not correct")
    def test_total_mass_propellant_tank(self):
        self.assertAlmostEqual(self.tanks.total_mass_propellant_tank(), 0.00010983283, 5, "total_mass_propellant_tank is not correct")
    def test_pressurant_mass_obj_func(self):
        self.assertAlmostEqual(self.tanks.pressurant_mass_obj_func(200), 0.00099145299, 5, "pressurant_mass_obj_func is not correct")
    def test_pressurant_tank_thickness(self):
        _ = self.tanks.total_mass_pressurant()
        self.assertAlmostEqual(self.tanks.pressurant_tank_thickness(), 0.002, 5, "pressurant_tank_thickness is not correct")
    def test_total_mass_pressurant_tank(self):
        self.assertAlmostEqual(self.tanks.total_mass_pressurant_tank(), 0.00051658453, 5, "total_mass_pressurant_tank is not correct")


if __name__ == "__main__":
    unittest.main()