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

class Block:
    def __init__(self, parent, indexLeft, indexRight, name, expr):
        self.parent = parent
        self.indexLeft = indexLeft
        self.indexRight = indexRight
        self.constructed_on = self.parent.now()
        self.destroyed_on = -1
        self.name = name
        self.expr = expr
        self.is_opaque = False
        self.tweaks = 0
        self.left_tweaks = 0
        self.alts = []

    def _config(self): return self.parent.config

    def opaque(self, op = True): self.is_opaque = op; return self
    def longer(self, how_much = 1): self.tweaks += how_much; return self
    def shorter(self, how_much = 1): self.tweaks -= how_much; return self
    def sooner(self, how_much = 1): self.left_tweaks += how_much; return self
    def later(self, how_much = 1): self.left_tweaks -= how_much; return self

    def alt(self, expr = None):
        self.alts.append( (self.parent.now() + self._config().STEP_HEIGHT/2 - self.constructed_on, expr) )

    def close(self):
        self.destroyed_on = self.parent.now()

    def getAnchor(self, index):
        if self.constructed_on == -1: return
        length = self.destroyed_on

        if length == -1: length = self.parent.now()
        length -= self.constructed_on

        tweak_scale = self._config().OBJECT_DISTANCE / 20

        x0 = self.indexRight * self._config().OBJECT_DISTANCE + self._config().OBJECT_WIDTH / 2
        x = self.indexLeft * self._config().OBJECT_DISTANCE - float(self._config().OBJECT_DISTANCE - self._config().OBJECT_WIDTH) / 2 - tweak_scale * self.left_tweaks
        y = self.constructed_on
        w = (self.indexRight - self.indexLeft + 1) * self._config().OBJECT_DISTANCE + (self.tweaks + self.left_tweaks) * tweak_scale
        h = length
        return _anchor.boxAnchor(index, 4, x - x0, y, x - x0 + w, y + h)

    def printOut(self, parent_canvas):
        if self.constructed_on == -1: return
        length = self.destroyed_on

        if length == -1: length = self.parent.now()
        length -= self.constructed_on

        tweak_scale = self._config().OBJECT_DISTANCE / 20
        width = (self.indexRight - self.indexLeft + 1) * self._config().OBJECT_DISTANCE + (self.tweaks + self.left_tweaks) * tweak_scale

        canvas = parent_canvas.canvas(self.indexLeft * self._config().OBJECT_DISTANCE - float(self._config().OBJECT_DISTANCE - self._config().OBJECT_WIDTH) / 2 - tweak_scale * self.left_tweaks, self.constructed_on)

        if self.is_opaque:
            canvas.rectangle(0, 0, width, length, "opt-opaque")

        canvas.poly(0, self._config().LABEL_HEIGHT, "optalt")\
            .lineTo(self._config().LABEL_WIDTH, self._config().LABEL_HEIGHT)\
            .lineTo(self._config().LABEL_WIDTH + self._config().LABEL_CORNER, self._config().LABEL_HEIGHT - self._config().LABEL_CORNER)\
            .lineTo(self._config().LABEL_WIDTH + self._config().LABEL_CORNER, 0)\
            .lineTo(0, 0)

        canvas.rectangle(0, 0, width, length, "optalt")
        canvas.text(float(self._config().LABEL_WIDTH)/2, self._config().LABEL_HEIGHT - 8, self.name, "optalt")
        if self.expr is not None:
            scale = 7 if self.is_opaque else 8
            canvas.text(self._config().LABEL_WIDTH * scale / 5, self._config().LABEL_HEIGHT - 8, self.expr, "optalt_expr")

        for when, expr in self.alts:
            canvas.line(0, when, width, 0, "optalt")
            if expr is not None:
                canvas.text(self._config().LABEL_WIDTH / 5, when + self._config().LABEL_HEIGHT - 8, expr, "optalt_expr")
