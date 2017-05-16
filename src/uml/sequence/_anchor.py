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
Created on 09-05-2017

@author: Marcin Zdun
'''

def getAnchor(index, defndx, *points):
    if index < 0: return points[defndx]
    index %= len(points)
    return points[index]

def getAnchorDiag(diag, index, defndx, *points):
    if index < 0: return points[defndx]
    index %= len(points)
    return points[index]

def boxAnchor(index, defndx, x1, y1, x2, y2):
    w2 = float(x2 - x1)/2
    h2 = float(y2 - y1)/2
    w4 = w2/2
    h4 = h2/2
    return getAnchor(index, defndx,
        (x1, y1), (x1 + w4, y1), (x1 + w2, y1), (x1 + w2 + w4, y1),
        (x2, y1), (x2, y1 + h4), (x2, y1 + h2), (x2, y1 + h2 + h4),
        (x2, y2), (x1 + w2 + w4, y2), (x1 + w2, y2), (x1 + w4, y2),
        (x1, y2), (x1, y1 + h2 + h4), (x1, y1 + h2), (x1, y1 + h4)
        )
