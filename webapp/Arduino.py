import json
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError

import serial
from serial import SerialException


class Arduino:
    def __init__(self):
        self.con_timeout = timedelta(seconds=5)
        self.pump_timeout = timedelta(seconds=60)
        self.ser = serial.Serial()
        self.ser.port = '/dev/ttyACM0'
        self.ser.baudrate = 57600
        self.ser.timeout = 1
        # Prevent the Arduino from rebooting
        # (+ cutting the RESET EN trace, thanks to https://forum.arduino.cc/index.php?topic=28723.msg212677#msg212677)
        self.ser.setDTR(False)
        try:
            self.ser.open()
        except SerialException:
            pass

    def close(self):
        self.ser.close()

    def readline(self):
        return self.ser.readline()

    def get_measure(self):
        json_line = {}
        if self.ser.is_open:
            wait_until = datetime.now() + self.con_timeout
            break_loop = False
            while not break_loop:
                line = self.readline().decode().rstrip('\r\n')
                if len(line) >= 59:
                    try:
                        json_line = json.loads(line)
                    except JSONDecodeError:
                        print("Cannot decode received json from arduino: " + line)
                is_timeout = wait_until < datetime.now()
                if (('b1' in json_line) and ('b2' in json_line) and ('b3' in json_line) and ('b4' in json_line) and (
                        'g' in json_line)) or is_timeout:
                    break_loop = True
        for key, value in json_line.items():
            json_line[key] = self.round_measure(value)
        return json_line

    def tare(self, n):
        if self.ser.is_open:
            wait_until = datetime.now() + self.con_timeout
            self.ser.write((str(n) + '\r\n').encode())
            while True:
                line = self.readline().decode()
                is_timeout = wait_until < datetime.now()
                if (line == 'Tare load cell ' + str(n) + ' complete\r\n') or is_timeout:
                    return not is_timeout
        else:
            return False

    def round_measure(self, measure):
        if measure < 0:
            return 0
        else:
            return int(measure)

    def wait_for_glass_measure(self, measure):
        json_line = {}
        actual_glass_vol = self.get_measure()['g']
        if self.ser.is_open:
            wait_until = datetime.now() + self.pump_timeout
            while True:
                line = self.readline().decode().rstrip('\r\n')
                if len(line) >= 59:
                    try:
                        json_line = json.loads(line)
                    except JSONDecodeError:
                        print("Cannot decode received json from arduino: " + line)
                is_timeout = wait_until < datetime.now()
                if (('b1' in json_line) and ('b2' in json_line) and ('b3' in json_line) and ('b4' in json_line) and (
                        'g' in json_line) and json_line['g'] >= actual_glass_vol + measure) or is_timeout:
                    return not is_timeout
