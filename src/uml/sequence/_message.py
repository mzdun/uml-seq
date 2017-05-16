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

import _anchor

class Message:
    def __init__(self, isAsync, isReturn, when, start, finish, name):
        self.isAsync = isAsync
        self.isReturn = isReturn
        self.when = when
        self.start = start
        self.finish = finish
        self.name = name

    def _config(self): return self.start.parent.config

    def _pos(self):
        start = self.start.index
        finish = self.finish.index
        reverse = False
        creator = self.when == self.finish.constructed_on
        if finish < start:
            reverse = True
            t = start
            start = finish
            finish = t

        level = 0
        if reverse: level = self.finish.level_at(self.when)
        else: level = self.start.level_at(self.when)
        depth = (level + 1)* float(self._config().STEP_WIDTH) / 2
        depth += float(self._config().STEP_WIDTH) / 4

        width = finish - start
        width *= self._config().OBJECT_DISTANCE
        start = 0
        if reverse:
            start = -width
        start += depth
        width -= depth + self._config().STEP_WIDTH*3/4
        
        if creator:
            if reverse: start += self._config().OBJECT_WIDTH/2
            width -= self._config().OBJECT_WIDTH/2 - self._config().STEP_WIDTH/2

        return (start, width, reverse)

    def getAnchor(self, index):
        y = self.when + self._config().OBJECT_HEIGHT/2

        if self.finish.index == self.start.index:
            level = self.start.level_at(self.when)
            depth = (level + 1)* float(self._config().STEP_WIDTH) / 2
            depth += float(self._config().STEP_WIDTH) / 4
            return _anchor.boxAnchor(index, 4,
                depth, y,
                float(self._config().OBJECT_DISTANCE) / 2,
                y + float(self._config().STEP_HEIGHT) / 2)

        start, width, reverse = self._pos()
        return _anchor.getAnchor(index, 1, (start, y), (start + width, y))

    def printOut(self, parent_canvas):
        canvas = parent_canvas.canvas(0, self.when + self._config().OBJECT_HEIGHT/2)

        if self.finish.index == self.start.index:
            self.printOutSelf(canvas)
        else:
            self.printOutExchange(canvas)

    def printOutExchange(self, canvas):
        start, width, reverse = self._pos()

        if self.name is not None:
            canvas.text(start + float(width)/2, -5.5, self.name)
        clazz = "signal"
        if self.isReturn: clazz = "return"

        canvas.line(start, 0, width, 0, clazz)
        arrow = "signalArrow"
        if self.isAsync: arrow = "asyncSignalArrow"
        pos = start + width
        if reverse:
            pos = start
        ref = canvas.ref(pos, 0, arrow)
        if reverse:
            ref.mirror()

    def printOutSelf(self, canvas):
        level = self.start.level_at(self.when)
        depth = (level + 1)* float(self._config().STEP_WIDTH) / 2
        depth += float(self._config().STEP_WIDTH) / 4

        #style="text-anchor:start"
        if self.name is not None:
            canvas.text(depth, -5.5, self.name).alignStart()
        canvas.poly(depth, 0, "line")\
            .lineTo(float(self._config().OBJECT_DISTANCE) / 2, 0)\
            .lineTo(float(self._config().OBJECT_DISTANCE) / 2, float(self._config().STEP_HEIGHT) / 2)\
            .lineTo(depth, float(self._config().STEP_HEIGHT) / 2)

        arrow = "signalArrow"
        if self.isAsync: arrow = "asyncSignalArrow"
        #scale(-1, 1)
        canvas.ref(depth, float(self._config().STEP_HEIGHT) / 2, arrow).mirror()

    def __str__(self):
        s = ""
        if self.start.index > self.finish.index:
            s += "&lt; "
        else:
            s += "&gt; "
        s += "%s " % (self.finish.index - self.start.index)
        if self.isAsync: s += "(a)"
        if self.isReturn: s += "(r)"
        if self.name is not None: s += self.name
        return s
