# encoding: utf-8

'''
Created on 02-03-2013

@author: Marcin
'''
from _utils import xmlize

class Message:
    def __init__(self, isAsync, isReturn, when, start, finish, name):
        self.isAsync = isAsync
        self.isReturn = isReturn
        self.when = when
        self.start = start
        self.finish = finish
        self.name = name

    def _config(self): return self.start.parent.config

    def printOut(self):
        print '      <g transform="translate(0, %s)">' % \
            (self.when + self._config().OBJECT_HEIGHT/2)

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
        depth = (level + 1)* float(self._config().STEP_WIDTH) / 2
        depth += float(self._config().STEP_WIDTH) / 4

        width = finish - start
        width *= self._config().OBJECT_DISTANCE
        start = 0
        if reverse:
            start = -width
        start += depth
        width -= depth + self._config().STEP_WIDTH*3/4
        
        if creator:
            if reverse: start += self._config().OBJECT_WIDTH/2
            width -= self._config().OBJECT_WIDTH/2 - self._config().STEP_WIDTH/2

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
        depth = (level + 1)* float(self._config().STEP_WIDTH) / 2
        depth += float(self._config().STEP_WIDTH) / 4

        if self.name is not None:
            print '        <text transform="translate(%.1f,-5.5)" style="text-anchor:start">%s</text>' % (depth, xmlize(self.name))
        if self.name is not None:
            print '        <polyline class="line" points="%.1f,0 %.1f,0 %.1f,%s %.1f,%s" />' % \
                (depth, float(self._config().OBJECT_DISTANCE) / 2, float(self._config().OBJECT_DISTANCE) / 2, self._config().STEP_HEIGHT, depth, self._config().STEP_HEIGHT)

        arrow = "signalArrow"
        if self.isAsync: arrow = "asyncSignalArrow"
        print '        <use xlink:href="#%s" transform="translate(%.1f, %s) scale(-1, 1)" />' % \
            (arrow, depth, self._config().STEP_HEIGHT)

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
