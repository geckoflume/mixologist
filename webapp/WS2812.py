import spidev


class WS2812:
    # color = [g, r, b]
    ready = [50, 25, 255]
    error = [10, 255, 0]
    warning = [220, 255, 25]
    success = [255, 10, 100]

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.leds_count = 18

    def close(self):
        self.spi.close()

    def reset(self):
        self.enable_all()

    def parse_color(self, color):
        if isinstance(color, str):
            if color == 'ready':
                color = self.ready
            elif color == 'error':
                color = self.error
            elif color == 'warning':
                color = self.warning
            elif color == 'success':
                color = self.success
        return color

    def enable_all(self, color=None):
        if color is None:
            color = [0, 0, 0]
        else:
            color = self.parse_color(color)
        self.write2812([color] * self.leds_count)

    def enable_one(self, led, color=None):
        if color is None:
            color = [255, 255, 255]
        else:
            color = self.parse_color(color)
        d = [[0, 0, 0]] * self.leds_count
        d[led % self.leds_count] = color
        self.write2812(d)

    def enable_n(self, n, color):
        if color is None:
            color = [255, 255, 255]
        else:
            color = self.parse_color(color)
        d = [color] * int((n * self.leds_count / 100))
        self.write2812(d)

    def write2812(self, data):
        tx = [0x00]
        for rgb in data:
            for byte in rgb:
                for ibit in range(3, -1, -1):
                    tx.append(((byte >> (2 * ibit + 1)) & 1) * 0x60 + ((byte >> (2 * ibit + 0)) & 1) * 0x06 + 0x88)
        self.spi.xfer(tx, int(4 / 1.05e-6))
