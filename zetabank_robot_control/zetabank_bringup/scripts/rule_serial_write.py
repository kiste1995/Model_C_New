#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, time, threading
import subprocess

from yaml import compose_all
import rospy
from zetabot_main.msg import BatteryInformationMsgs
from zetabot_main.msg import EnvironmentMsgs

# ros start
class PWR:
    def __init__(self, battery_topic):
        self.check_flag = ''
        self.battery_sub = rospy.Subscriber(battery_topic, BatteryInformationMsgs, self.battery_callback)
        
    def battery_callback(self,msg):
        self.check_flag = 'PWR'
        print(self.check_flag)

class AIR:
    def __init__(self, air_topic):
        self.check_flag = ''
        self.air_sub = rospy.Subscriber(air_topic, EnvironmentMsgs, self.air_callback)

    def air_callback(self, msg):
        self.check_flag = 'AIR'
        print(self.check_flag)

class command:
# terminal input
    def __init__(self):
        self.command_rosrun = "rosrun rosserial_python serial_node.py _port:=/dev/ttyUSB{} _baud:=115200"
        self.command_udevadm = "udevadm info -a /dev/ttyUSB{}" # | grep ‘{serial}’"

    def usb_check(self):
       
        for i in range(3):
            command_rosrun = self.command_rosrun.format(i)
            command_udevadm = self.command_udevadm.format(i)
            # command = subprocess.Popen(command_rosrun, stdout = subprocess.PIPE).communicate()[0]
# threading 1
# password
            echo = "echo 'zetabank' | sudo -S tee"
            os.system(echo)
            permission_ = "sudo chmod 777 /dev/ttyUSB0 && sudo chmod 777 /dev/ttyUSB1 && sudo chmod 777 /dev/ttyUSB2"
            os.system(permission_)
            t1 = threading.Thread(target= thread_rosrun, name= "USB thread" ,args =(command_rosrun,))
            t1.setDaemon(True)
            t1.start()
# ros start            
            battery_topic = '/battery'
            check = PWR(battery_topic)

            time.sleep(5)
# wait time
            if check.check_flag == 'PWR':
                print('PWR')
                nodes = os.popen("rosnode list").readline()
                os.system("rosnode kill /serial_node")
                t1.join()
                t2= threading.Thread(target= thread_PWR, name= "Module", args=(command_udevadm,))
                t2.start()
                t2.join()

            else:
                air_topic = '/air'
                check_ = AIR(air_topic)
                time.sleep(15)
                
                if check_.check_flag == 'AIR':
                    print('AIR')
                    nodes = os.popen("rosnode list").readline()
                    os.system("rosnode kill /serial_node")
                    t1.join()
    # threading 2
                    t2 = threading.Thread(target= thread_AIR, name= "AIR", args= (command_udevadm, ))
                    t2.start()
                    t2.join()
                else: 
                    print('MC')
                    nodes = os.popen("rosnode list").readline()
                    os.system("rosnode kill /serial_node")
                    t1.join()
    # threading 2
                    t2 = threading.Thread(target= thread_MC, name= "Motor" , args= (command_udevadm, ))
                    t2.start()
                    t2.join()
            
################AIR#################            
def thread_AIR(command_udev):
    command_add = 'ACTION==\"add\"'
    command_udev_s = command_udev + " | grep '{serial}'"
    command_udev_idV = command_udev + " | grep '{idVendor}'"
    command_udev_idP = command_udev + " | grep '{idProduct}'"
    command_mode = 'MODE:="0777"'
    command_sym = 'SYMLINK+="ttyUSB-AIR"'
    serial_result = os.popen(command_udev_s).read()
    idVendor_result = os.popen(command_udev_idV).read()
    idProduct_result = os.popen(command_udev_idP).read()
# print(serial_result)
    serial_r = serial_result.split('\n')[0]
    idV_r = idVendor_result.split('\n')[0]
    idP_r = idProduct_result.split('\n')[0]
# threading3
    data = [command_add, idV_r, idP_r, serial_r, command_mode, command_sym]
    t3 = threading.Thread(target= thread_data, name= "data3", args= (data,))
    t3.start()
    t3.join()


#################MC#################
def thread_MC(command_udev):
    command_add = 'ACTION==\"add\"'
    command_udev_s = command_udev + " | grep '{serial}'"
    command_udev_idV = command_udev + " | grep '{idVendor}'"
    command_udev_idP = command_udev + " | grep '{idProduct}'"
    command_mode = 'MODE:="0777"'
    command_sym = 'SYMLINK+="ttyUSB-MC"'
    serial_result = os.popen(command_udev_s).read()
    idVendor_result = os.popen(command_udev_idV).read()
    idProduct_result = os.popen(command_udev_idP).read()

# print(serial_result)
    serial_r = serial_result.split('\n')[0]
    idV_r = idVendor_result.split('\n')[0]
    idP_r = idProduct_result.split('\n')[0]
# threading3
    data = [command_add, idV_r, idP_r, serial_r, command_mode, command_sym]
    t3 = threading.Thread(target= thread_data, name= "data2", args= (data,))
    t3.start()
    t3.join()

################PWR################
def thread_PWR(command_udev):
    command_add = 'ACTION==\"add\"'
    command_udev_s = command_udev + " | grep '{serial}'"
    command_udev_idV = command_udev + " | grep '{idVendor}'"
    command_udev_idP = command_udev + " | grep '{idProduct}'"
    command_mode = 'MODE:="0777"'
    command_sym = 'SYMLINK+="ttyUSB-PWR"'

    serial_result = os.popen(command_udev_s).read()
    idVendor_result = os.popen(command_udev_idV).read()
    idProduct_result = os.popen(command_udev_idP).read()
# print(serial_result)
    serial_r = serial_result.split('\n')[0]
    idV_r = idVendor_result.split('\n')[0]
    idP_r = idProduct_result.split('\n')[0]
   
# threading 3
    data = [command_add, idV_r, idP_r, serial_r, command_mode, command_sym]
    t3 = threading.Thread(target= thread_data, name= "data1", args= (data,))
    t3.start()
    t3.join()
############################################################   

def thread_data(data):
# write
    data_ = "echo '" +  data[0] + ", " + data[1] + ", " + data[2] + ", " + data[3] + ", " + data[4] + ", " + data[5] + "' | sudo tee -a /etc/udev/rules.d/99-usb-serial.rules"
    print(data_)
    os.system(data_)

def thread_rosrun(command_rosrun):
    os.system(command_rosrun)

if __name__ == '__main__':
    rospy.init_node("serial")
    command().usb_check()