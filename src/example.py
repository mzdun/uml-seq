#!/usr/local/bin/python2.7
# encoding: utf-8

'''
Created on 01-03-2013

@author: Marcin
'''

import uml

def main():
    diag = uml.Diagram()
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