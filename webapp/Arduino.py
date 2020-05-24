import json
import threading
from datetime import datetime, timedelta
from json.decoder import JSONDecodeError

import serial
from serial import SerialException


def round_measure(measure):
    return 0 if measure < 0 else measure


class Arduino:
    def __init__(self, port, baudrate, con_timeout, pump_timeout):
        self.con_timeout = timedelta(seconds=con_timeout)
        self.pump_timeout = timedelta(seconds=pump_timeout)
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baudrate
        self.ser.timeout = 1
        # Prevent the Arduino from rebooting
        # (+ cutting the RESET EN trace, thanks to https://forum.arduino.cc/index.php?topic=28723.msg212677#msg212677)
        self.ser.setDTR(False)
        self.open()
        self.json_line = {'b1': 0, 'b2': 0, 'b3': 0, 'b4': 0, 'g': 0}
        self.initial_glass_volume = 0
        self.target_glass_volume = 0
        self.lock = threading.Lock()
        self.abort = False

    def open(self):
        self.ser.open()

    def close(self):
        self.ser.close()

    def poll(self):
        if self.ser.is_open:
            wait_until = datetime.now() + self.con_timeout
            successful_read = False
            while not successful_read:
                line = ''
                temp = {}
                try:
                    line = self.ser.readline().decode().rstrip('\r\n')
                except SerialException:
                    pass
                if len(line) >= 59:
                    try:
                        temp = json.loads(line)
                    except JSONDecodeError:
                        print("Cannot decode received json from arduino: " + line)
                is_timeout = wait_until < datetime.now()
                if ((('b1' in temp) and ('b2' in temp) and ('b3' in temp) and ('b4' in temp) and ('g' in temp)) and (
                        (temp['b1'] != self.json_line['b1']) or (temp['b2'] != self.json_line['b2']) or (
                        temp['b3'] != self.json_line['b3']) or (temp['b4'] != self.json_line['b4']) or (
                                temp['g'] != self.json_line['g']))) or is_timeout:
                    for key, value in temp.items():
                        temp[key] = round_measure(value)
                    self.json_line = temp
                    successful_read = True
        return self.json_line

    def tare(self, n):
        if self.ser.is_open:
            self.lock.acquire()
            wait_until = datetime.now() + self.con_timeout
            self.ser.write((str(n) + '\r\n').encode())
            while True:
                line = self.ser.readline().decode()
                is_timeout = wait_until < datetime.now()
                if (line == 'Tare load cell ' + str(n) + ' complete\r\n') or is_timeout:
                    self.lock.release()
                    return not is_timeout
        else:
            return False

    def poll_once(self):
        self.lock.acquire()
        ret = self.poll()
        self.lock.release()
        return ret

    def wait_for_glass_measure(self, measure):
        wait_until = datetime.now() + self.pump_timeout
        self.initial_glass_volume = self.json_line['g']
        while True:
            self.lock.acquire()
            self.poll()
            is_timeout = wait_until < datetime.now()
            self.lock.release()
            if self.abort or (('b1' in self.json_line) and ('b2' in self.json_line) and ('b3' in self.json_line) and (
                    'b4' in self.json_line) and ('g' in self.json_line) and self.json_line[
                    'g'] >= self.initial_glass_volume + measure) or is_timeout:
                return not (self.abort or is_timeout)

    def broadcast_loadcells(self, e, socketio):
        while not e.isSet():
            e.wait()
            old_json_line = {}
            while e.isSet():
                self.lock.acquire()
                self.poll()
                if ('b1' not in old_json_line) or (
                        int(old_json_line['b1']) != int(self.json_line['b1'])) or (
                        int(old_json_line['b2']) != int(self.json_line['b2'])) or (
                        int(old_json_line['b3']) != int(self.json_line['b3'])) or (
                        int(old_json_line['b4']) != int(self.json_line['b4'])) or (
                        int(old_json_line['g']) != int(self.json_line['g'])):
                    old_json_line = self.json_line
                    socketio.emit('load_cells', self.json_line, room='settings')
                    socketio.emit('load_cells', self.json_line, room='index')
                self.lock.release()

    def update_progression(self, e, socketio, ws2812):
        old_glass = -1
        while not e.isSet():
            e.wait()
            self.initial_glass_volume = self.json_line['g']
            while e.isSet():
                self.lock.acquire()
                self.poll()
                if self.json_line['g'] != old_glass:
                    old_glass = self.json_line['g']
                    percentage = (self.json_line['g'] - self.initial_glass_volume) / (
                            self.target_glass_volume - self.initial_glass_volume) * 100
                    if percentage > 100:
                        percentage = 100
                    print("actual vol: " + str(self.json_line['g']) + " target: " + str(
                        self.target_glass_volume) + " (" + str(percentage) + "%)")
                    socketio.emit('progression', percentage, room='index')
                    ws2812.enable_percentage(percentage)
                self.lock.release()
