# encoding: utf-8

# 
# Copyright (C) 2017 midnightBITS/Marcin Zdun
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
Created on 09-05-2017

@author: Marcin Zdun
'''

import sys, base, _message, _activity, _block

class Comment(base.Comment):
    def __init__(self, parent, text, anchor = None):
        self.parent = parent
        self.text = text
        self.width = parent.config.COMMENT_WIDTH
        self.height = parent.config.COMMENT_HEIGHT
        self.obj = None
        self.anchor = -1
        if anchor is not None:
            self.anchor = anchor
        self.obj_lane = -1
        self.lane = -1
    def _config(self): return self.parent.config

    def attachTo(self, obj, anchor = -1):
        self.obj = obj
        if anchor >= 0:
            self.anchor = anchor
        if isinstance(obj, _message.Message):
            start = obj.start.index
            finish = obj.finish.index
            self.obj_lane = start if start > finish else finish
        elif isinstance(obj, _activity.Activity):
            self.obj_lane = obj.parent.index
        elif isinstance(obj, _block.Block):
            self.obj_lane = obj.indexRight
        else:
            self.obj_lane = obj.index
        self.lane = self.obj_lane + 1

    def setWidth(self, width):
        self.width = width

    def printOut(self, parent_canvas):
        if not self.obj: return

        node = self.obj.getAnchor(self.anchor)

        x0 = self.obj_lane * self._config().OBJECT_DISTANCE
        x = (self.lane - self.obj_lane + 1) * self._config().OBJECT_DISTANCE
        y = -self._config().STEP_HEIGHT

        canvas = parent_canvas.canvas(x0, node[1])
        canvas.poly(self._config().OBJECT_WIDTH / 2 + node[0], 0, "comment anchor").lineTo(x, y)

        y -= self.height / 2
        canvas.poly(x + self.width - self._config().COMMENT_FLAP, y, "comment")\
            .lineTo(x, y).lineTo(x, y + self.height)\
            .lineTo(x + self.width, y + self.height)\
            .lineTo(x + self.width, y + self._config().COMMENT_FLAP)\
            .lineTo(x + self.width - self._config().COMMENT_FLAP, y)\
            .lineTo(x + self.width - self._config().COMMENT_FLAP, y + self._config().COMMENT_FLAP)\
            .lineTo(x + self.width, y + self._config().COMMENT_FLAP)

        line_height = 12
        x += self._config().COMMENT_FLAP / 2
        y += self._config().COMMENT_FLAP / 2 + line_height

        for line in self.text.split("\n"):
            canvas.text(x, y, line, "comment").alignStart()
            y += line_height
