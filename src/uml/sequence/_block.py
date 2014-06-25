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

class Block:
    def __init__(self, parent, indexLeft, indexRight, name):
        self.parent = parent
        self.indexLeft = indexLeft
        self.indexRight = indexRight
        self.constructed_on = self.parent.now()
        self.destroyed_on = -1
        self.name = name

    def _config(self): return self.parent.config

    def close(self):
        self.destroyed_on = self.parent.now()

    def printOut(self, parent_canvas):
        if self.constructed_on == -1: return
        length = self.destroyed_on

        if length == -1: length = self.parent.now()
        length -= self.constructed_on

        canvas = parent_canvas.canvas(self.indexLeft * self._config().OBJECT_DISTANCE - float(self._config().OBJECT_DISTANCE - self._config().OBJECT_WIDTH) / 2, self.constructed_on)
        canvas.poly(0, self._config().LABEL_HEIGHT, "optalt")\
            .lineTo(self._config().LABEL_WIDTH, self._config().LABEL_HEIGHT)\
            .lineTo(self._config().LABEL_WIDTH + self._config().LABEL_CORNER, self._config().LABEL_HEIGHT - self._config().LABEL_CORNER)\
            .lineTo(self._config().LABEL_WIDTH + self._config().LABEL_CORNER, 0)\
            .lineTo(0, 0)

        canvas.rectangle(0, 0, (self.indexRight - self.indexLeft + 1) * self._config().OBJECT_DISTANCE, length, "optalt")
        canvas.text(float(self._config().LABEL_WIDTH)/2, self._config().LABEL_HEIGHT - 8, self.name, "optalt")
    
