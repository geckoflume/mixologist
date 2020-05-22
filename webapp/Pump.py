from pyA20.gpio import gpio, port

pumps = {'bottle1': port.PA10, 'bottle2': port.PA9, 'bottle3': port.PA8, 'bottle4': port.PA7}


def init_pumps():
    gpio.init()
    for pin in pumps.values():
        gpio.setcfg(pin, gpio.OUTPUT)
        gpio.output(pin, gpio.HIGH)


class Pump:
    def __init__(self, name):
        self.name = name

    def enable(self):
        gpio.output(pumps[self.name], gpio.LOW)

    def disable(self):
        gpio.output(pumps[self.name], gpio.HIGH)
