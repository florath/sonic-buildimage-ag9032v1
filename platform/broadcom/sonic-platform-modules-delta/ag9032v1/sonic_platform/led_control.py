
class LEDControl:
    '''The complete LED set and get subsystem uses sys fs.

    There is one file which can be read to get the current state
    and can be written to set the LED state.

    This switch has 9 system LEDs:

    * Power 1 (pwr1)
    * Power 2 (pwr2)
    * System (sys)
    * Fan front (fan)
    * Fan 1 back (fan1)
    * Fan 2 back (fan2)
    * Fan 3 back (fan3)
    * Fan 4 back (fan4)
    * Fan 5 back (fan5)

    The status can of the LEDs can be read and set using
    /sys/devices/platform/delta-ag9032v1-swpld.0/led_control

    Each of the LEDs can have a different set of states
    (see ag9032v1/modules/delta_ag9032v1_platform.c)

    * pwr1_off pwr1_green pwr1_amber
    * pwr2_off pwr2_green pwr2_amber
    * sys_off sys_green sys_blinking_green sys_red
    * fan_off fan_green fan_amber
    * fanX_off fanX_green fanX_red
    '''
    sysfs = "/sys/devices/platform/delta-ag9032v1-swpld.0/led_control"

    def __update_status(self):
        with open(LEDControl.sysfs, "r") as sysfs_fd:
            data = sysfs_fd.read()
            for line in data.split("\n"):
                kv = line.split("_", 1)
                if len(kv) == 2:
                    self.__led_status[kv[0]] = kv[1]

    def __init__(self):
        self.__led_status = {}

    def get_status(self, name):
        self.__update_status()
        return self.__led_status[name]

    def set_status(self, name, status):
        cmd = "%s_%s\n" % (name, status)
        with open(LEDControl.sysfs, "w") as sysfs_fd:
            sysfs_fd.write(cmd)

