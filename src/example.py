#!/usr/local/bin/python2.7
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
Created on 01-03-2013

@author: Marcin Zdun
'''

import uml.sequence

def main():
    diag = uml.sequence.Diagram()

    o = diag.object("o:Toolkit")
    p = diag.pobject("p:Peer")
    diag.step()

    o.active()
    diag.step()

    o.active()
    o.sendTo(o, "callbackLoop()")
    o.inactive()

    o.create(p)
    o.sendTo(p, "handleExpose()")
    p.active()
    p.returnTo(o)
    p.inactive()
    o.destroy(p)
    o.inactive()

    diag.step();
    diag.printOut();

if __name__ == '__main__':
    main()