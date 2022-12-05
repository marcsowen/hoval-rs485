#!/usr/bin/python3 -u

import serial

if __name__ == '__main__':
    ser = serial.Serial(port="/dev/ttyUSB2",
                        baudrate=19200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=0.1)

    while True:
        result = ser.read(512)
        if len(result) == 21:
            # print(":".join("{:02x}".format(b) for b in result) + " [" + str(len(result)) + "]")
            print(";".join("{:>3}".format(b) for b in result))
            # print("T1 = " + str(int.from_bytes(result[5:7], byteorder='big', signed=True)))
            # print("T2 = " + str(int.from_bytes(result[5:7], byteorder='little', signed=True)))
            # print("T3 = " + str(int.from_bytes(result[5:7], byteorder='big', signed=False)))
            # print("T4 = " + str(int.from_bytes(result[5:7], byteorder='little', signed=False)))
            print("{}:{} - {}:{}".format(ord(result[6:7]) & 0xF, ord(result[6:7]) >> 4,
                                         ord(result[7:8]) & 0xF, ord(result[7:8]) >> 4))
