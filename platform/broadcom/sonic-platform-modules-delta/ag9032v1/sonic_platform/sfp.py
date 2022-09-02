'''
sonic_platform Sfp implementation for ag9032v1
'''

try:
    from sonic_platform_base.sonic_xcvr.sfp_optoe_base import SfpOptoeBase
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class Sfp(SfpOptoeBase):

    def __init__(self, sfp_util_base, port_num, sfp_type, eeprom_path):
        SfpOptoeBase.__init__(self)
        self.sfp_util_base = sfp_util_base
        self.sfp_type = sfp_type
        self.port_num = port_num
        self.eeprom_path = eeprom_path

    def get_presence(self):
        try:
            reg_file = open("/sys/devices/platform/delta-ag9032v1-swpld.0/sfp_present")
        except IOError as e:
            print("Error: unable to open file: %s" % str(e))
            return False

        content = reg_file.readline().rstrip()

        # content is a string containing the hex representation of the register
        reg_value = int(content, 16)

        # Mask off the bit corresponding to our port
        mask = (1 << self.port_num)

        # ModPrsL is active low
        if reg_value & mask == 0:
            return True

        return False

    def get_port_num(self):
        return self.port_num

    def get_eeprom_path(self):
        return self.eeprom_path

    def get_transceiver_info(self):
        return self.sfp_util_base.get_transceiver_info_dict(self.port_num)

    def get_transceiver_bulk_status(self):
        return self.sfp_util_base.get_transceiver_dom_info_dict(self.port_num)

    def get_transceiver_threshold_info(self):
        return self.sfp_util_base.get_transceiver_dom_threshold_info_dict(self.port_num)
