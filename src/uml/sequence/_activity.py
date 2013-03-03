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
Created on 03-03-2013

@author: Marcin Zdun
'''

class Activity:
    def __init__(self, parent, start, finish, level = 0):
        self.parent = parent
        self.start = start
        self.finish = finish
        self.level = level
    def length(self):
        return self.finish - self.start

    def printOut(self, canvas):
        canvas.ref(self.level * self.parent.parent.config.STEP_OFFSET,
                   self.start,
                   "activity%s" % self.length())

    def __str__(self):
        if self.level == 0: return repr([self.start, self.finish])
        return "[%s: %s, %s]" % (self.level, self.start, self.finish)
    def __repr__(self): return str(self)

    def __eq__(self, other): return self.start == other.start and self.finish == other.finish
    def __ne__(self, other): return not self.__eq__(other)
    def __lt__(self, other):
        if self.start == other.start: return self.finish < other.finish
        return self.start < other.start
    def __le__(self, other):
        if self.start == other.start: return self.finish <= other.finish
        return self.start <= other.start
    def __gt__(self, other):
        if self.start == other.start: return self.finish > other.finish
        return self.start > other.start
    def __ge__(self, other):
        if self.start == other.start: return self.finish >= other.finish
        return self.start >= other.start
