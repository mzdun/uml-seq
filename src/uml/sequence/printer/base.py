'''
Created on 03-03-2013

@author: Marcin
'''

class Canvas:
    def canvas(self, offX, offY): pass

class Predefines:
    def rectangle(self, name, x, y, width, height, clazz = None): pass
    def line(self, x, y, width, height, dash_pattern = None): pass
    def poly(self, name, startX, startY, clazz = None): pass

class Printer:
    def defs(self): return None
    def createCanvas(self, margin, width, height): return None
    def output(self, out): pass
