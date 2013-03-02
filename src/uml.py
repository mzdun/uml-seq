# encoding: utf-8

'''
Created on 01-03-2013

@author: Marcin
'''

import sys

PAGE_MARGIN = 50
OBJECT_DISTANCE = 125
OBJECT_WIDTH=75
OBJECT_HEIGHT=30
STEP_WIDTH=10
STEP_HEIGHT=25
STEP_OFFSET=5

def xmlize(s): return s

def def_object():
    return '''    <rect
      xml:id="object"
      x="0" y="0" width="%s" height="%s"
      />
''' % (OBJECT_WIDTH, OBJECT_HEIGHT)

def def_lifeline(length, suffix = ""):
    return '''    <line
      xml:id="lifeline%s"
      class="lifeline"
      x1="%.1f" y1="%s" x2="%.1f" y2="%s"
      />
''' % (suffix, float(OBJECT_WIDTH)/2, OBJECT_HEIGHT, float(OBJECT_WIDTH)/2, OBJECT_HEIGHT/2 + length)

def def_activity(length):
    return '''    <rect
      xml:id="activity%s"
      x="%.1f" y="%s" width="%s" height="%s"
      />
''' % (length, float(OBJECT_WIDTH)/2 - float(STEP_WIDTH)/2, OBJECT_HEIGHT/2, STEP_WIDTH, length)

def def_destroy():
    return '''      <g
      xml:id="destroy"
      class="destroy"
      transform="translate(%.1f,%s)">
      <line x1="-10" y1="-10" x2="10" y2="10" />
      <line x1="10" y1="-10" x2="-10" y2="10" />
    </g>
''' % (float(OBJECT_WIDTH)/2, OBJECT_HEIGHT/2)

DOC_START = '''<?xml version="1.0" encoding="utf-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="%.4fin" height="%.4fin" viewBox="0 0 %s %s">
  <title>SVG Drawing</title>
  <style type="text/css">
    text {
      font-family: sans-serif;
      font-size: 8pt;
      stroke: none;
      fill: #333;
      text-anchor: middle
    }
    text.object {
      text-decoration: underline
    }
    rect {
      stroke: black;
      stroke-linecap: butt;
      fill: #ffa
    }
    .signal, .line {
      stroke: black;
      stroke-linecap: butt;
      fill: none
    }
    .block {
      stroke: black;
      stroke-linecap: butt;
      fill: black
    }
    .lifeline, .return {
      stroke: black;
      stroke-dasharray: 5 5
    }
    .destroy {
      stroke: black;
      stroke-width: 2;
      stroke-linecap: butt;
      fill: none
    }
  </style>
  <defs>
%s    <polyline
      xml:id="signalArrow"
      class="block"
      points="-10,-3 0,0 -10,3"
      />
    <polyline
      xml:id="asyncSignalArrow"
      class="line"
      points="-10,-3 0,0 -10,3"
      />
    <g
      xml:id="signal"
      class="signal"
      transform="translate(42.5, 50.71)">
      <line x1="0" y1="0" x2="113" y2="0" />
      <use xlink:href="#signalArrow" transform="translate(113)" />
    </g>
    <g
      xml:id="selfSignal"
      class="signal"
      transform="translate(42.5, 50.71)">
      <polyline class="line" points="0,0 62.5,0 62.5,25 0,25" />
      <use xlink:href="#syncSignalArrow" transform="translate(0, 25) scale(-1, 1)" />
    </g>
  </defs>'''

DOC_END = '</svg>'

class Message:
    def __init__(self, isAsync, isReturn, when, start, finish, name):
        self.isAsync = isAsync
        self.isReturn = isReturn
        self.when = when
        self.start = start
        self.finish = finish
        self.name = name

    def printOut(self):
        print '      <g transform="translate(0, %s)">' % \
            (self.when + OBJECT_HEIGHT/2)

        if self.finish.index == self.start.index:
            self.printOutSelf()
        else:
            self.printOutExchange()

        print '      </g>'

    def printOutExchange(self):
        start = self.start.index
        finish = self.finish.index
        reverse = False
        creator = self.when == self.finish.constructed_on
        if finish < start:
            reverse = True
            t = start
            start = finish
            finish = t

        level = 0
        if reverse: level = self.finish.level_at(self.when)
        else: level = self.start.level_at(self.when)
        depth = (level + 1)* float(STEP_WIDTH) / 2
        depth += float(STEP_WIDTH) / 4
        print >>sys.stderr, level, depth

        width = finish - start
        width *= OBJECT_DISTANCE
        start = 0
        if reverse:
            start = -width
        start += depth
        width -= depth + STEP_WIDTH*3/4
        
        if creator:
            if reverse: start += OBJECT_WIDTH/2
            width -= OBJECT_WIDTH/2 - STEP_WIDTH/2

        if self.name is not None:
            print '        <text transform="translate(%.1f,-5.5)">%s</text>' % (start + float(width)/2, xmlize(self.name))
        clazz = "signal"
        if self.isReturn: clazz = "return"
        print '        <line class="%s" x1="%s" y1="0" x2="%s" y2="0" />' % (clazz, start, start + width)
        arrow = "signalArrow"
        if self.isAsync: arrow = "asyncSignalArrow"
        pos = start + width
        scale = ""
        if reverse:
            pos = start
            scale=" scale(-1, 1)"
        print '        <use xlink:href="#%s" transform="translate(%s)%s" />' % \
            (arrow, pos, scale)

    def printOutSelf(self):
        level = self.start.level_at(self.when)
        depth = (level + 1)* float(STEP_WIDTH) / 2
        depth += float(STEP_WIDTH) / 4

        if self.name is not None:
            print '        <text transform="translate(%.1f,-5.5)" style="text-anchor:start">%s</text>' % (depth, xmlize(self.name))
        if self.name is not None:
            print '        <polyline class="line" points="%.1f,0 %.1f,0 %.1f,%s %.1f,%s" />' % \
                (depth, float(OBJECT_DISTANCE) / 2, float(OBJECT_DISTANCE) / 2, STEP_HEIGHT, depth, STEP_HEIGHT)

        arrow = "signalArrow"
        if self.isAsync: arrow = "asyncSignalArrow"
        print '        <use xlink:href="#%s" transform="translate(%.1f, %s) scale(-1, 1)" />' % \
            (arrow, depth, STEP_HEIGHT)

        sys.stdout.write('{')
        if self.isAsync: sys.stdout.write('|')
        sys.stdout.write('}')
        if self.name is not None:
            sys.stdout.write(" ")
            sys.stdout.write(self.name)
        sys.stdout.write("\n")

    def __str__(self):
        s = ""
        if self.start.index > self.finish.index:
            s += "&lt; "
        else:
            s += "&gt; "
        s += "%s " % (self.finish.index - self.start.index)
        if self.isAsync: s += "(a)"
        if self.isReturn: s += "(r)"
        if self.name is not None: s += self.name
        return s

class Activity:
    def __init__(self, start, finish, level = 0):
        self.start = start
        self.finish = finish
        self.level = level
    def length(self):
        return self.finish - self.start
    def printOut(self):
        print '      <use xlink:href="#activity%s" transform="translate(%s, %s)"/>' % \
            (self.length(), self.level * STEP_OFFSET, self.start)

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

class Object:
    '''
    classdocs
    '''


    def __init__(self, parent, index, name, alive):
        '''
        Constructor
        '''
        self.parent = parent
        self.index = index
        self.name = name
        if alive: self.constructed_on = 0
        else: self.constructed_on = -1
        self.destroyed_on = -1
        self.activity = []
        self.messages = []
        self.activity_stack = []

    def active(self):
        self.activity_stack.append(self.parent.now())

    def inactive(self):
        level = len(self.activity_stack)
        if level == 0: return
        level -= 1
        start = self.activity_stack[level]
        finish = self.parent.now()
        if start == finish: return
        if self.constructed_on > 0:
            start -= self.constructed_on
            finish -= self.constructed_on
        self.activity_stack = self.activity_stack[:level]
        self.activity.append(Activity(start, finish, level))

    def sendTo(self, oth, name = None):
        self.messages.append(self.parent.addMessage(False, self, oth, name))

    def returnTo(self, oth, name = None):
        self.messages.append(self.parent.addMessage(True, self, oth, name))

    def create(self, oth):
        self.sendTo(oth, "«create»")
        oth.constructed_on = self.parent.now()
        self.parent.hstep();

    def destroy(self, oth):
        self.sendTo(oth, "«destroy»")
        oth.destroyed_on = self.parent.now()

    def level_at(self, timestamp):
        max_level = 0
        if self.constructed_on != -1:
            timestamp -= self.constructed_on
        for activity in self.activity:
            if activity.start <= timestamp and activity.finish >= timestamp:
                if max_level < activity.level:
                    max_level = activity.level
        print >>sys.stderr, timestamp, max_level, self.activity
        return max_level

    def object_label(self, offY = 0):
        return '      <text class="object" transform="translate(%.1f,%s)">%s</text>' % \
            (float(OBJECT_WIDTH)/2, offY + OBJECT_HEIGHT - 12, xmlize(self.name))

    def printOut(self):
        if self.constructed_on == -1: return

        lifeline_suffix = ""
        if self.constructed_on != 0 or self.destroyed_on != -1:
            length = self.destroyed_on
            if length == -1: length = self.parent.now()
            length -= self.constructed_on
            lifeline_suffix = str(length)

        translate = ""
        start = self.constructed_on
        if self.index != 0 or self.constructed_on > 0:
            if self.index == 0:
                translate = "0"
            else:
                translate = "%s" % (self.index * OBJECT_DISTANCE)
            if self.constructed_on > 0:
                translate = "%s, %s" % (translate, start)
        if translate == "":
            print '    <g>'
        else:
            print '    <g transform="translate(%s)">' % translate

        print '      <use xlink:href="#lifeline%s"/>' % lifeline_suffix
        print '      <use xlink:href="#object"/>'
        print self.object_label();

        while len(self.activity_stack) > 0: self.inactive()
        activity = sorted(self.activity)
        for a in activity:
            a.printOut()
        if self.destroyed_on != -1:
            print '      <use xlink:href="#destroy" transform="translate(0, %s)"/>' % \
                (self.destroyed_on - self.constructed_on)

        print '    </g>'

    def printOutMessages(self):
        print '    <g transform="translate(%.1f)">' % \
            (float(OBJECT_WIDTH)/2 + self.index * OBJECT_DISTANCE)

        for msg in self.messages:
            msg.printOut()
        print '    </g>'

class Diagram:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.objects = []
        self.messages = []
        self.timeline = 0
        self.is_async = False

    def object(self, name):
        o = Object(self, len(self.objects), name, True)
        self.objects.append(o)
        return o

    def pobject(self, name):
        o = Object(self, len(self.objects), name, False)
        self.objects.append(o)
        return o

    def async(self): self.is_async = True
    def sync(self): self.is_async = False
    def step(self): self.timeline += STEP_HEIGHT
    def hstep(self): self.timeline += STEP_HEIGHT/2
    def now(self): return self.timeline

    def addMessage(self, isReturn, start, finish, name):
        self.step()
        when = self.timeline
        m = Message(self.is_async, isReturn, when, start, finish, name)
        self.messages.append(m)
        if start.index == finish.index:
            self.step()
        return m

    def printOut(self):
        doc_width = (len(self.objects) - 1) * OBJECT_DISTANCE + PAGE_MARGIN*2 + OBJECT_WIDTH
        doc_height = OBJECT_HEIGHT + self.timeline + PAGE_MARGIN*2

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
            
        defs = def_object()
        if self.timeline in lifeline_lengths:
            defs += def_lifeline(self.timeline)
        for length in lifeline_lengths:
            if length == self.timeline: continue
            defs += def_lifeline(length, length)
        for length in sorted(activity_lengths.keys()):
            defs += def_activity(length)
        
        if destroyed_needed:
            defs += def_destroy()

        print DOC_START % (float(doc_width)/72, float(doc_height)/72, doc_width, doc_height, defs)
        print '  <g transform="translate(%s, %s)">' % (PAGE_MARGIN, PAGE_MARGIN)
        for obj in self.objects:
            obj.printOut()
        for obj in self.objects:
            obj.printOutMessages()
        print '  </g>'
        print DOC_END
