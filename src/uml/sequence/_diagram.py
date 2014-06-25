# encoding: utf-8

# 
# Copyright (C) 2013 midnightBITS/Marcin Zdun
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, copy,
# modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

'''
Created on 02-03-2013

@author: Marcin Zdun
'''

from sys import stdout
import base, printer
import _object, _block, _message

class Diagram(base.Diagram):
    def __init__(self):
        self.objects = []
        self.blocks = []
        self.messages = []
        self.timeline = 0
        self.is_async = False
        self.config = base.Config()

    def object(self, name):
        o = _object.Object(self, len(self.objects), name, True)
        self.objects.append(o)
        return o

    def pobject(self, name):
        o = _object.Object(self, len(self.objects), name, False)
        self.objects.append(o)
        return o

    def block(self, name, left, right, expr = None):
        b = _block.Block(self, left.index, right.index, name, expr)
        self.blocks.append(b)
        return b

    def async(self): self.is_async = True
    def sync(self): self.is_async = False
    def step(self): self.timeline += self.config.STEP_HEIGHT
    def stepBack(self): self.timeline -= self.config.STEP_HEIGHT
    def hstep(self): self.timeline += self.config.STEP_HEIGHT/2
    def now(self): return self.timeline

    def __message(self, isReturn, start, finish, name, isAsync):
        self.step()
        when = self.timeline
        m = _message.Message(isAsync, isReturn, when, start, finish, name)
        self.messages.append(m)
        if start.index == finish.index:
            self.step()
        return m

    def addMessage(self, isReturn, start, finish, name):
        return self.__message(isReturn, start, finish, name, self.is_async)

    def syncAddMessage(self, isReturn, start, finish, name):
        return self.__message(isReturn, start, finish, name, False)

    def asyncAddMessage(self, isReturn, start, finish, name):
        return self.__message(isReturn, start, finish, name, True)

    def printOut(self, prn = None):
        #find the lifeline markers needed
        lifeline_lengths = {}
        activity_lengths = {}
        destroyed_needed = False
        for obj in self.objects:
            if obj.constructed_on == -1:
                continue
            destroyed = obj.destroyed_on
            if destroyed == -1:
                destroyed = self.timeline
            else:
                destroyed_needed = True
            length = destroyed - obj.constructed_on
            lifeline_lengths[length] = 1
            for activity in obj.activity:
                activity_lengths[activity.length()] = 1

        if prn is None:
            prn = printer.DefaultPrinter()

        #extend the definition list
        defs = prn.defs()
        defs.rectangle("object", 0, 0, self.config.OBJECT_WIDTH, self.config.OBJECT_HEIGHT)
        if self.timeline in lifeline_lengths:
            defs.line("lifeline",
                      float(self.config.OBJECT_WIDTH)/2, self.config.OBJECT_HEIGHT,
                      0, self.timeline - self.config.OBJECT_HEIGHT/2,
                      "lifeline")
        for length in lifeline_lengths:
            if length == self.timeline: continue
            defs.line("lifeline%s" % length,
                      float(self.config.OBJECT_WIDTH)/2, self.config.OBJECT_HEIGHT,
                      0, length - self.config.OBJECT_HEIGHT/2,
                      "lifeline")
        for length in sorted(activity_lengths.keys()):
            defs.rectangle("activity%s" % length,
                           float(self.config.OBJECT_WIDTH)/2 - float(self.config.STEP_WIDTH)/2,
                           self.config.OBJECT_HEIGHT/2,
                           self.config.STEP_WIDTH, length)

        if destroyed_needed:
            destroy = defs.canvas("destroy", float(self.config.OBJECT_WIDTH)/2, self.config.OBJECT_HEIGHT/2, "destroy")
            destroy.line(-10, -10, 20, 20)
            destroy.line(10, -10, -20, 20)

        for _def in (("asyncSignalArrow", "line"), ("signalArrow", "block")):
            defs.poly(_def[0], -10, -3, _def[1]).lineTo(0,0).lineTo(-10, 3)

        canvas = prn.canvas(self.config.PAGE_MARGIN,
                            (len(self.objects) - 1) * self.config.OBJECT_DISTANCE + self.config.OBJECT_WIDTH,
                            self.config.OBJECT_HEIGHT + self.timeline)
        for obj in self.objects:
            obj.printOut(canvas)
        for obj in self.objects:
            obj.printOutMessages(canvas)
        for block in self.blocks:
            block.printOut(canvas)
        prn.output(stdout)
