'''
Created on 03-03-2013

@author: Marcin
'''

from base import Printer, Canvas, Predefines

class _SvgTransform:
    def __init__(self):
        self.transforms = []
    def _add(self, func):
        self.transforms.append(func)
        return self

    def translate(self, offX, offY):
        if offX != 0 or offY != 0:
            if offY != 0:
                return self._add("translate(%s, %s)" % (offX, offY))
            else:
                return self._add("translate(%s)" % offX)
        return self

    def scale(self, scaleX, scaleY):
        if scaleX != 1 or scaleY != 1:
            return self._add("scale(%s, %s)" % (scaleX, scaleY))
        return self

    def set(self, node):
        transforms = " ".join(self.transforms)
        if transforms != "":
            node.attr("transform", transforms)

class _SvgNode:
    def __init__(self, name):
        self._name = name
        self._attr = []
        self._style = {}
        self._children = []
        self._text = None

    def attr(self, name, value):
        for i in range(len(self._attr)):
            if self._attr[i][0] == name:
                self._attr[i][1] = value
                return self
        self._attr.append([name, value])
        return self
    def style(self, name, value):
        self._style[name] = value
        return self
    def add(self, child):
        self._children.append(child)
        return self
    def text(self, text):
        self._text = text
        return self

    def _print(self, out, indent):
        out.write("%s<%s" % (indent, self._name))

        attr_len = len(self._attr)
        styles = ""
        for style in sorted(self._style.keys()):
            styles += "%s:%s;" % (style, self._style[style])
        if styles != "":
            attr_len += 1

        pre = " "
        if attr_len > 1: pre = "\n" + indent + "  " #+ (" " * len(self._name))

        if styles != "":
            out.write('%sstyle="%s"' % (pre, styles))

        for attr in self._attr:
            out.write('%s%s="%s"' % (pre, attr[0], attr[1]))

        if attr_len > 1: out.write(pre)
        if self._text is None and len(self._children) == 0:
            out.write("/>\n")
            return
        if self._text is not None:
            out.write(">%s</%s>\n" % (self._text, self._name))
            return
        out.write(">\n")

        sub = indent + "  "
        for child in self._children:
            child._print(out, sub)
        
        out.write("%s</%s>\n" % (indent, self._name))

class _Graphics:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class _Rectangle(_Graphics):
    def __init__(self, x, y, width, height, clazz = None):
        _Graphics.__init__(self, x, y, width, height)
        self.clazz = clazz

    def _node(self):
        node = _SvgNode("rect")
        if self.clazz is not None:
            node.attr("class", self.clazz)
        return node.attr("x", self.x).attr("y", self.y).attr("width", self.width).attr("height", self.height)

class _Line(_Graphics):
    def __init__(self, x, y, width, height, dash_pattern = None):
        _Graphics.__init__(self, x, y, width, height)
        self.dash_pattern = dash_pattern

    def _node(self):
        node = _SvgNode("line")
        if self.dash_pattern is not None:
            pattern = []
            for dash in self.dash_pattern:
                pattern.append(str(dash))
            node.style("stroke-dasharray", " ".join(pattern))
        return node.attr("x1", self.x).attr("y1", self.y)\
            .attr("x2", self.x + self.width).attr("y2", self.y + self.height)

class _Poly(_Graphics):
    def __init__(self, x, y, clazz = None):
        _Graphics.__init__(self, x, y, 0, 0)
        self.points = [(x, y)]
        self.clazz = clazz
    def lineTo(self, x, y):
        self.points.append((x, y))

        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y + self.height

        if x < x1: x1 = x
        if x > x2: x2 = x
        if y < y1: y1 = y
        if y > y2: y2 = y

        self.x = x1
        self.y = y1
        self.width = x2 - x1
        self.height = y2 - y1

        return self

    def _node(self):
        node = _SvgNode("polyline")
        if self.clazz is not None:
            node.attr("class", self.clazz)
        points = []
        for pt in self.points:
            points.append("%s,%s" % pt)
        return node.attr("points", " ".join(points))

class SvgPredefines(Predefines):
    def __init__(self):
        self.defs = {}

    def rectangle(self, name, x, y, width, height, clazz = None):
        o = _Rectangle(x, y, width, height, clazz)
        self.defs[name] = o
        return o

    def line(self, name, x, y, width, height, dash_pattern = None):
        o = _Line(x, y, width, height, dash_pattern)
        self.defs[name] = o
        return o

    def poly(self, name, startX, startY, clazz = None):
        o = _Poly(startX, startY, clazz)
        self.defs[name] = o
        return o

    def _node(self):
        node= _SvgNode("defs")
        for name in self.defs:
            node.add(self.defs[name]._node().attr("name", name))
        return node

class SvgCanvas(Canvas):
    def __init__(self):
        self.offX = 0
        self.offY = 0
        self.objects = []

    def setOff(self, x, y):
        self.offX = x
        self.offY = y
    def _add(self, obj):
        self.objects.append(obj)
        return obj

    def canvas(self, offX, offY):
        c = SvgCanvas()
        c.setOff(offX, offY)
        return self._add(c)

    def _node(self):
        node= _SvgNode("g")
        _SvgTransform().translate(self.offX, self.offY).set(node)

        for obj in self.objects:
            node.add(obj._node())
        return node

class SvgPrinter(Printer):
    def __init__(self):
        self._width = 1
        self._height = 1
        self._defs = SvgPredefines()
        self._canvas = SvgCanvas()
    def defs(self): return self._defs

    def canvas(self, margin, width, height):
        self._width = width + 2 * margin
        self._height = height + 2 * margin
        self._canvas.setOff(margin, margin)
        return self._canvas

    def output(self, out):
        svg = _SvgNode("svg") \
            .attr("xmlns", "http://www.w3.org/2000/svg") \
            .attr("version", "1.1") \
            .attr("xmlns:xlink", "http://www.w3.org/1999/xlink") \
            .attr("width", "%.4fin" % (float(self._width)/72)) \
            .attr("height", "%.4fin" % (float(self._height)/72)) \
            .attr("viewBox", "0 0 %s %s" % (self._width, self._height)) \
            .add(_SvgNode("title").text("SVG Drawing"))\
            .add(self._defs._node())\
            .add(self._canvas._node())
        print '<?xml version="1.0" encoding="utf-8" standalone="no"?>'
        svg._print(out, "")
