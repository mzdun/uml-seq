# encoding: utf-8

'''
Created on 02-03-2013

@author: Marcin
'''

import base
import _object
import _message
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
        doc_width = (len(self.objects) - 1) * self.config.OBJECT_DISTANCE + self.config.PAGE_MARGIN*2 + self.config.OBJECT_WIDTH
        doc_height = self.config.OBJECT_HEIGHT + self.timeline + self.config.PAGE_MARGIN*2

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

        #extend the definition list
        defs = _utils.def_object(self.config)
        if self.timeline in lifeline_lengths:
            defs += _utils.def_lifeline(self.config, self.timeline)
        for length in lifeline_lengths:
            if length == self.timeline: continue
            defs += _utils.def_lifeline(self.config, length, length)
        for length in sorted(activity_lengths.keys()):
            defs += _utils.def_activity(self.config, length)
        
        if destroyed_needed:
            defs += _utils.def_destroy(self.config)

        #write the contents of the document
        print _utils.DOC_START % (float(doc_width)/72, float(doc_height)/72, doc_width, doc_height, defs)
        print '  <g transform="translate(%s, %s)">' % (self.config.PAGE_MARGIN, self.config.PAGE_MARGIN)
        for obj in self.objects:
            obj.printOut()
        for obj in self.objects:
            obj.printOutMessages()
        print '  </g>'
        print _utils.DOC_END
