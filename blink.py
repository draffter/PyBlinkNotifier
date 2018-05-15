#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from blink1.blink1 import blink1, Blink1


class Blink(object):

    def __init__(self):
        blink1_serials = Blink1.list()
        self.serial = blink1_serials[0]
        self.blink1 = Blink1(serial_number=self.serial)

    def set_unread_pattern(self):
        self.blink1.writePatternLine(500, '#0000AA', 0)
        self.blink1.writePatternLine(1000, '#000000', 1)
        self.blink1.writePatternLine(0, '#000000', 2)
        self.blink1.writePatternLine(0, '#000000', 3)
        self.blink1.writePatternLine(0, '#000000', 4)
        self.blink1.writePatternLine(0, '#000000', 5)
        self.blink1.writePatternLine(1, '#000000', 6)
        self.blink1.writePatternLine(1, '#000000', 7)
        self.blink1.writePatternLine(1, '#000000', 8)
        self.blink1.writePatternLine(1, '#000000', 9)
        self.blink1.writePatternLine(1, '#000000', 10)
        self.blink1.writePatternLine(1, '#000000', 11)
        self.blink1.savePattern()

    def start_unread_blink(self):
        self.set_unread_pattern()
        self.blink1.play(0, 0)

    def stop_unread_blinking(self):
        self.blink1.stop()
        self.blink1.off()

    def blink_pattern(self, color, on_time, off_time, count=4):
        r, g, b = color
        for i in range(count):
            self.blink1.fade_to_rgb(on_time, r, g, b)
            time.sleep(off_time)
            self.blink1.fade_to_color(on_time, 'black')
            time.sleep(off_time)
        self.blink1.off()
