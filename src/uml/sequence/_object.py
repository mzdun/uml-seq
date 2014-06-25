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

import _activity, base

class Object(base.Object):
    def __init__(self, parent, index, name, alive):
        self.parent = parent
        self.index = index
        self.name = name
        if alive: self.constructed_on = 0
        else: self.constructed_on = -1
        self.destroyed_on = -1
        self.activity = []
        self.messages = []
        self.activity_stack = []

    def _config(self): return self.parent.config

    def active(self):
        self.activity_stack.append(self.parent.now())

    def inactive(self):
        level = len(self.activity_stack)
        if level == 0: return
        level -= 1
        start = self.activity_stack[level]
        finish = self.parent.now()
        if start == finish: return
        if self.constructed_on > 0:
            start -= self.constructed_on
            finish -= self.constructed_on
        self.activity_stack = self.activity_stack[:level]
        self.activity.append(_activity.Activity(self, start, finish, level))

    def sendTo(self, oth, name = None):
        self.messages.append(self.parent.addMessage(False, self, oth, name))
        oth.active()

    def returnTo(self, oth, name = None):
        self.messages.append(self.parent.addMessage(True, self, oth, name))
        self.inactive()

    def create(self, oth, proto = None):
        if proto is None: proto = "create"
        self.sendTo(oth, "«%s»" % proto)
        oth.constructed_on = self.parent.now()
        self.parent.hstep();

    def destroy(self, oth, proto = None):
        if proto is None: proto = "destroy"
        self.messages.append(self.parent.addMessage(False, self, oth, "«%s»" % proto))
        oth.destroyed_on = self.parent.now()

    def level_at(self, timestamp):
        max_level = 0
        if self.constructed_on != -1:
            timestamp -= self.constructed_on
        for activity in self.activity:
            if activity.start <= timestamp and activity.finish >= timestamp:
                if max_level < activity.level:
                    max_level = activity.level
        return max_level

    def printOut(self, parent_canvas):
        if self.constructed_on == -1: return

        lifeline_suffix = ""
        if self.constructed_on != 0 or self.destroyed_on != -1:
            length = self.destroyed_on
            if length == -1: length = self.parent.now()
            length -= self.constructed_on
            lifeline_suffix = str(length)
        
        canvas = parent_canvas.canvas(self.index * self._config().OBJECT_DISTANCE,
                                      self.constructed_on)
        canvas.ref(0, 0, "lifeline%s" % lifeline_suffix)
        canvas.ref(0, 0, "object")

        canvas.text(float(self._config().OBJECT_WIDTH)/2, self._config().OBJECT_HEIGHT - 12, self.name, "object")

        while len(self.activity_stack) > 0: self.inactive()
        activity = sorted(self.activity)
        for a in activity:
            a.printOut(canvas)
        if self.destroyed_on != -1:
            canvas.ref(0, self.destroyed_on - self.constructed_on, "destroy")

    def printOutMessages(self, parent_canvas):
        canvas = parent_canvas.canvas(float(self._config().OBJECT_WIDTH)/2 + self.index * self._config().OBJECT_DISTANCE, 0)

        for msg in self.messages:
            msg.printOut(canvas)
