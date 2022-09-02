'''
sfputil for the ag9032v1
'''

import time

try:
    from sonic_platform_base.sonic_sfp.sfputilbase import SfpUtilBase
    from sonic_platform.sfp import Sfp
except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

class SfpUtil(SfpUtilBase):

    # SFP related
    PORT_START = 0
    PORT_END = 31
    PORTS_IN_BLOCK = 32

    EEPROM_OFFSET = 50

    SFP_STATUS_INSERTED = '1'
    SFP_STATUS_REMOVED = '0'
    
    _port_to_eeprom_mapping = {}
    port_dict = {}
    
    @property
    def port_start(self):
        return self.PORT_START

    @property
    def port_end(self):
        return self.PORT_END

    @property
    def port_to_eeprom_mapping(self):
        return self._port_to_eeprom_mapping

    @property
    def osfp_ports(self):
        """ OSFP/QSFP-DD Ports """
        return []

    @property
    def qsfp_ports(self):
        """ QSFP Ports """
        return list(range(self.PORT_START, self.PORTS_IN_BLOCK))
    
    def __init__(self, sfp_list):
        '''Pass in the sfp_list from the chassis which is used in this class'''
        self._sfp_list = sfp_list
        SfpUtilBase.__init__(self)

        self._port_to_eeprom_mapping = {}
        
        # self._sfp_list.append(None)
        eeprom_base = "/sys/class/i2c-adapter/i2c-{0}/{0}-0050/eeprom"
        for index in range(self.PORT_START, self.PORTS_IN_BLOCK):
            eeprom_path = eeprom_base.format(index + self.EEPROM_OFFSET)
            port_type = 'QSFP'
            sfp_node = Sfp(self, index, port_type, eeprom_path)
            self._sfp_list.append(sfp_node)
            self._port_to_eeprom_mapping[index] = eeprom_path

    def get_change_event(self, timeout=0):
        start_time = time.time()
        current_port_dict = { 'sfp': {}, 'sfp_error': {} }
        error_port_dict = { 'sfp': {}, 'sfp_error': {} }
        forever = False

        if timeout == 0:
            forever = True
        elif timeout > 0:
            timeout = timeout / float(1000) # Convert to secs
        else:
            print ("get_transceiver_change_event:Invalid timeout value", timeout)
            return False, error_port_dict

        end_time = start_time + timeout
        if start_time > end_time:
            print ('get_transceiver_change_event:' \
                       'time wrap / invalid timeout value', timeout)

            return False, error_port_dict # Time wrap or possibly incorrect timeout

        while timeout >= 0:
            # Check for OIR events and return updated port_dict
            for x in self._sfp_list:
                if x.get_presence():
                    current_port_dict['sfp'][x.get_port_num()] = self.SFP_STATUS_INSERTED
                else:
                    current_port_dict['sfp'][x.get_port_num()] = self.SFP_STATUS_REMOVED
                
            if (current_port_dict == self.port_dict):
                if forever:
                    time.sleep(1)
                else:
                    timeout = end_time - time.time()
                    if timeout >= 1:
                        time.sleep(1) # We poll at 1 second granularity
                    else:
                        if timeout > 0:
                            time.sleep(timeout)
                        return True, error_port_dict
            else:
                # Update reg value
                self.port_dict = current_port_dict
                return True, self.port_dict
        print("get_transceiver_change_event: Should not reach here.")
        return False, error_port_dict
