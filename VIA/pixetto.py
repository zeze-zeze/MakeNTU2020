################################################################################
#                                                                              #
# Copyright (c) 2020 VIA Technologies, Inc. All Rights Reserved.               #
#                                                                              #
# This PROPRIETARY SOFTWARE is the property of VIA Technologies, Inc.          #
# and may contain trade secrets and/or other confidential information of       #
# VIA Technologies, Inc. This file shall not be disclosed to any third         #
# party, in whole or in part, without prior written consent of VIA.            #
#                                                                              #
# THIS PROPRIETARY SOFTWARE AND ANY RELATED DOCUMENTATION ARE PROVIDED AS IS,  #
# WITH ALL FAULTS, AND WITHOUT WARRANTY OF ANY KIND EITHER EXPRESS OR IMPLIED, #
# AND VIA TECHNOLOGIES, INC. DISCLAIMS ALL EXPRESS OR IMPLIED                  #
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, QUIET       #
# ENJOYMENT OR NON-INFRINGEMENT.                                               #
#                                                                              #
################################################################################

import serial
import time
import sys
import json

class Pixetto:
    def __init__(self):
        self.ser = None
        self.id  = 0
        self.num = 0
        self.objs_list = {}
        self.raw_data = ""

    def open(self, port):
        """
        Open a serial connection to Pixetto and initialize Pixetto. 
        Args:
            port: COM port of Pixetto.
        """
        self.ser = serial.Serial(port, 115200, timeout=3)

        #if self.ser.isOpen():
        #    print("OK")
        #else:
        #    print("failed")

        time.sleep(0.1)

        self.ser.write("{\"header\":\"STREAMON\"};".encode())
        self.ser.flushInput()

    def close(self):
        """
        Turn off Pixetto camera and close the serial connection.        
        """
        self.ser.write("{\"header\":\"STREAMOFF\"};".encode())
        self.ser.flushInput()
        self.ser.close()
        #print("closed!!")

    def is_detected(self):
        """
        Check if there is any object detected.
        Returns:
            True if any object is detected, False if none.
        """
        line = []

        count = self.ser.inWaiting()
        if count == 0:
            return False
        #print("count=", count)
        while count > 0:
            aa = self.ser.read(1)
            if aa == b';':
                break
            line.append(aa.decode("ascii"))
            count -= 1

        self.raw_data = "".join(x for x in line)
        #print("line=", joined_seq)

        thing = json.loads(self.raw_data)

        if thing['header'] == 'DETECT':
            self.id  = thing['id']
            self.num = thing['num'] 
            if self.num > 0:
                self.objs_list = thing['objects']
                return True
            else:
                return False
        else:
            return False

    def get_data_list(self):
        """
        Parse the received data of detected objects.
        Returns: 
            id: function id
            num: number of detected objects
            objs_list: list of objects
        """
        return self.id, self.num, self.objs_list

    def get_raw_data(self):
        """
        Returns:
            Received raw data.        
        """
        return self.raw_data
