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

class Config:
    PAGE_MARGIN = 50
    OBJECT_DISTANCE = 125
    OBJECT_WIDTH = 75
    OBJECT_HEIGHT = 30
    LABEL_WIDTH = 50
    LABEL_HEIGHT = 20
    LABEL_CORNER = 10
    STEP_WIDTH = 10
    STEP_HEIGHT = 25
    STEP_OFFSET = 5

class Diagram:
    def object(self, name):
        return None
    def pobject(self, name):
        return None
    def block(self, name, left, right, expr = None):
        return None

    def async(self):
        pass
    def sync(self):
        pass
    def step(self):
        pass

    def printOut(self, prn = None):
        pass

class Object:
    def active(self):
        pass
    def inactive(self):
        pass
    def sendTo(self, oth, name = None):
        return None
    def returnTo(self, oth, name = None):
        return None
    def create(self, oth, proto = None):
        return None
    def destroy(self, oth, proto = None):
        return None

class Block:
    def alt(self, expr = None):
        pass
    def close(self):
        pass
