#!/usr/bin/python3 -u
from time import sleep

import serial
from datetime import datetime
import re

if __name__ == '__main__':
    ser = serial.Serial(port="/dev/ttyUSB2",
                        baudrate=19200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=0.1)

    nibbleDict = dict()
    iteration = 1

    while True:
        result = ser.read(512)
        if len(result) == 21:
            # print(":".join("{:02x}".format(b) for b in result) + " [" + str(len(result)) + "]")
            currentTime = datetime.now()
            currentTimeInt = currentTime.hour * 100 + currentTime.minute
            upperNibble = (currentTimeInt & 0xF00) >> 8
            upperNibbleBinarySequence = "{:04b}".format(upperNibble)
            binarySequence = "".join("{:08b}".format(b) for b in result)
            for m in re.finditer(upperNibbleBinarySequence, binarySequence):
                nibbleDict[m.start()] = nibbleDict.get(m.start(), 0) + 1
            nibbleDict_sorted = sorted(nibbleDict.items(), key=lambda x: x[1], reverse=True)
            # print(binarySequence)
            print('Binary search:', upperNibbleBinarySequence, 'Iteration:', iteration)
            step = 0
            for i in nibbleDict_sorted:
                if step > 5:
                    break
                print(i[0], '->', i[1])
                step += 1
            print("{} - {} - ".format(currentTimeInt, ((ord(result[8:9]) & 0xf0) << 4) + ord(result[7:8]))
                  + ";".join("{:>3}".format(b) for b in result))
            iteration += 1
            # print("T1={}, T2={}, T3={}, T4={}".format(int.from_bytes(result[2:4], byteorder='big', signed=True),
            #                                           int.from_bytes(result[4:6], byteorder='big', signed=True),
            #                                           int.from_bytes(result[6:8], byteorder='big', signed=True),
            #                                           int.from_bytes(result[8:10], byteorder='big', signed=True)))
            # print("{} - {:08b} {:08b} - [{} {}]".format(datetime.now(),
            #                                            ord(result[6:7]), ord(result[7:8]),
            #                                            ord(result[6:7]), ord(result[7:8])))
            # print("{}:{} - {}:{}".format(ord(result[6:7]) >> 6, ord(result[6:7]) & 0x3F,
            #                              ord(result[7:8]) >> 6, ord(result[7:8]) & 0x3F))
