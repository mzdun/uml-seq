# encoding: utf-8

'''
Created on 02-03-2013

@author: Marcin
'''

from sys import stdout
import base, printer
import _object, _message
import _utils

class Diagram(base.Diagram):
    def __init__(self):
        self.objects = []
        self.messages = []
        self.timeline = 0
        self.is_async = False
        self.config = base.Config()

    def object(self, name):
        o = _object.Object(self, len(self.objects), name, True)
        self.objects.append(o)
        return o

    def pobject(self, name):
        o = _object.Object(self, len(self.objects), name, False)
        self.objects.append(o)
        return o

    def async(self): self.is_async = True
    def sync(self): self.is_async = False
    def step(self): self.timeline += self.config.STEP_HEIGHT
    def hstep(self): self.timeline += self.config.STEP_HEIGHT/2
    def now(self): return self.timeline

    def addMessage(self, isReturn, start, finish, name):
        self.step()
        when = self.timeline
        m = _message.Message(self.is_async, isReturn, when, start, finish, name)
        self.messages.append(m)
        if start.index == finish.index:
            self.step()
        return m

    def printOut(self):
        #find the lifeline markers needed
        lifeline_lengths = {}
        activity_lengths = {}
        destroyed_needed = False
        for obj in self.objects:
            if obj.constructed_on == -1:
                continue
            destroyed = obj.destroyed_on
            if destroyed == -1:
                destroyed = self.timeline
            else:
                destroyed_needed = True
            length = destroyed - obj.constructed_on
            lifeline_lengths[length] = 1
            for activity in obj.activity:
                activity_lengths[activity.length()] = 1

        prn = printer.DefaultPrinter()

        #extend the definition list
        defs = prn.defs()
        defs.rectangle("object", 0, 0, self.config.OBJECT_WIDTH, self.config.OBJECT_HEIGHT)
        if self.timeline in lifeline_lengths:
            defs.line("lifeline", float(self.config.OBJECT_WIDTH)/2, self.config.OBJECT_HEIGHT, 0, self.timeline, [5, 5])
        for length in lifeline_lengths:
            if length == self.timeline: continue
            defs.line("lifeline%s" % length, float(self.config.OBJECT_WIDTH)/2, self.config.OBJECT_HEIGHT, 0, length, [5, 5])
        for length in sorted(activity_lengths.keys()):
            defs.rectangle("activity%s" % length, 0, 0, self.config.STEP_WIDTH, length)

        if destroyed_needed:
            defs += _utils.def_destroy(self.config)
            
        for _def in (("asyncSignalArrow", "line"), ("signalArrow", "block")):
            defs.poly(_def[0], -10, -3, _def[1]).lineTo(0,0).lineTo(-10, 3)

        canvas = prn.canvas(self.config.PAGE_MARGIN,
                            (len(self.objects) - 1) * self.config.OBJECT_DISTANCE + self.config.OBJECT_WIDTH,
                            self.config.OBJECT_HEIGHT + self.timeline)
        for obj in self.objects:
            obj.printOut(canvas)
        prn.output(stdout)

        #write the contents of the document
        #print _utils.DOC_START % (float(doc_width)/72, float(doc_height)/72, doc_width, doc_height, defs)
        #print '  <g transform="translate(%s, %s)">' % (self.config.PAGE_MARGIN, self.config.PAGE_MARGIN)
        #for obj in self.objects:
        #    obj.printOut()
        #for obj in self.objects:
        #    obj.printOutMessages()
        #print '  </g>'
        #print _utils.DOC_END
