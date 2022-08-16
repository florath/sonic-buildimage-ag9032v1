
# LEDs

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

* off
* green
* amber


pwr1_off
pwr2_off
sys_blinking_green
fan_green
fan1_green
fan2_green
fan3_off
fan4_off
fan5_off
