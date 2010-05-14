import math

import emen2.Database.globalns
g = emen2.Database.globalns.GlobalNamespace()

import emen2.Database.datatypes

Property = emen2.Database.datatypes.Property



class prop_transmittance(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "%T"
		self.units = {'%T': 1.0}
		self.equiv = {}


		


class prop_force(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "N"
		self.units = {'N': 1.0}
		self.equiv = {'newton': 'N'}


		


class prop_energy(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "J"
		self.units = {'J': 1.0}
		self.equiv = {'joule': 'J'}


		


class prop_resistance(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "ohm"
		self.units = {'ohm': 1.0}
		self.equiv = {}


		


class prop_dose(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "e/A2/sec"
		self.units = {'e/A2/sec': 1.0}
		self.equiv = {'e/A^2/sec': 'e/A2/sec'}


		


class prop_currency(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "dollars"
		self.units = {'dollars': 1.0}
		self.equiv = {}


		


class prop_voltage(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "volt"
		self.units = {'mv': 0.001, 'kv': 1000.0, 'V': 1.0}
		self.equiv = {'kilovolt': 'kv', 'millivolt': 'mv', 'kilovolts': 'kv', 'millivolts': 'mv', 'volts': 'V', 'volt': 'V'}


		


class prop_pH(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "pH"
		self.units = {'pH': 1.0}
		self.equiv = {}


		


class prop_concentration(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "mg/ml"
		self.units = {'p/ml': 1.0, 'mg/ml': 1.0, 'pfu': 1.0}
		self.equiv = {}


		


class prop_angle(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "degree"
		self.units = 	{"degree":1.0,"radian":180.0/math.pi, "mrad":0.18/math.pi}
		self.equiv = {'degrees': 'degree', 'deg': 'degree'}


		


class prop_temperature(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "K"
		self.units = {'K': 1.0, 'C': 1, 'F': 1}
		self.equiv = {'kelvin': 'K', 'degrees F': 'F', 'degrees C': 'C'}


		


class prop_area(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "m^2"
		self.units = {'cm^2': 0.0001, 'm^2': 1.0}
		self.equiv = {}


		


class prop_current(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "amp"
		self.units = {'amp': 1.0}
		self.equiv = {'ampere': 'amp'}


		


class prop_filesize(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "bytes"
		self.units = {'kB': 1000, 'MB': 1000000, 'MiB': 1048576, 'bytes': 1.0, 'GB': 1000000000, 'KiB': 1024, 'GiB': 1073741824}
		self.equiv = {'B': 'bytes'}


		


class prop_percentage(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "%"
		self.units = {'%': 1.0}
		self.equiv = {}


		


class prop_momentum(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "kg m/s"
		self.units = {'kg m/s': 1.0}
		self.equiv = {}


		


class prop_volume(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "m^3"
		self.units = 	{"m^3":1,"ml":1.0e-6,"l":1.0e-3,"ul":1.0e-9,"ul":1.0e-9}
		self.equiv = {'cm^3': 'ml', 'milliliter': 'ml', 'uL': 'ul', 'milliliters': 'ml'}


		


class prop_pressure(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "Pa"
		self.units = 	{"Pa":1.0,"bar":1.0e-5,"atm":9.8692327e-6,"torr":7.500617e-6,"psi":1.450377e-4}
		self.equiv = {'mmHg': 'torr', 'pascal': 'Pa'}


		


class prop_unitless(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "unitless"
		self.units = {'unitless': 1}
		self.equiv = {}


		


class prop_inductance(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "henry"
		self.units = {'H': 1.0}
		self.equiv = {'henry': 'H'}


		


class prop_currentdensity(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "Pi Amp/cm2"
		self.units = {'Pi Amp/cm2': 1.0}
		self.equiv = {}


		


class prop_exposure(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "e/A2"
		self.units = {'e/A2': 1.0}
		self.equiv = {'e/A^2': 'e/A2'}


		


class prop_count(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "count"
		self.units = {'count': 1, 'K': 1000, 'pixels': 1}
		self.equiv = {'k': 'K'}


		


class prop_bfactor(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "A^2"
		self.units = {'A^2': 1.0}
		self.equiv = {'A2': 'A^2'}


		


class prop_relative_humidity(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "%RH"
		self.units = {'%RH': 1.0}
		self.equiv = {}


		


class prop_length(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "m"
		self.units = 	{"m":1., "km":1000., "cm":0.01, "mm":0.001, "um":1.0e-6, "nm":1.0e-9, "A":1.0e-10}
		self.equiv = {'microns': 'um', 'nanometers': 'nm', 'nanometer': 'nm', 'Angstroms': 'A', 'meter': 'm', 'angstroms': 'A', 'millimeter': 'mm', 'kilometer': 'km', 'meters': 'm', 'angstrom': 'A', 'millimeters': 'mm', 'kilometers': 'km', 'micron': 'um', 'centimeters': 'cm', 'centimeter': 'cm', 'Angstrom': 'A'}


		


class prop_mass(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "gram"
		self.units = 	{"g":1.,"mg":.001,"Da":1.6605387e-24,"KDa":1.6605387e-21, "MDa":1.6605387e-18}
		self.equiv = {'kilodaltons': 'KDa', 'grams': 'g', 'milligrams': 'mg', 'daltons': 'Da', 'milligram': 'mg', 'megadaltons': 'MDa', 'megadalton': 'MDa', 'gram': 'g', 'dalton': 'Da', 'kilodalton': 'KDa'}


		


class prop_time(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "s"
		self.units = {'hour': 3600, 'min': 60, 'us': 1e-6, 's': 1.0, 'ms': 0.001, 'ns': 1e-09, 'day': 86400}
		self.equiv = {'millisecond': 'ms', 'seconds': 's', 'nanoseconds': 'ns', 'nanosecond': 'ns', 'days': 'day', 'hours': 'hour', 'secs': 's', 'microsecond': 'us', 'sec': 's', 'microseconds': 'us', 'mins': 'min', 'milliseconds': 'ms'}


		


class prop_velocity(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "m/s"
		self.units = {'m/s': 1.0}
		self.equiv = {}


		


class prop_resolution(Property):
	__metaclass__ = Property.register_view
	

	def __init__(self):
		self.conv = {}
		self.defaultunits = "A/pix"
		self.units = {'A/pix': 1.0}
		self.equiv = {}