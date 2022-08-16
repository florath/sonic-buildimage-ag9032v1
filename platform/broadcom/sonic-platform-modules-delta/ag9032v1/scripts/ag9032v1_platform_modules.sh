#!/bin/sh

echo "Setting up ag9032v1 modules "

depmod -a
rmmod i2c-i801
rmmod i2c-ismt
modprobe i2c-dev
modprobe i2c-i801
modprobe i2c-ismt
modprobe i2c-mux-pca954x
modprobe dni_ag9032v1_psu
modprobe dni_emc2305
modprobe at24
modprobe delta_ag9032v1_platform
modprobe delta_ag9032v1_cpupld

echo "Finished setting up ag9032v1 modules"
