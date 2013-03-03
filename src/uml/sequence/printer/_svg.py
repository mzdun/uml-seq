'''
Created on 03-03-2013

@author: Marcin
'''

from base import Printer, Canvas, Predefines, Graphics, TextGraphics, PolyGraphics

def xmlize(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")

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
            out.write('%sstyle="%s"' % (pre, xmlize(styles)))

        for attr in self._attr:
            out.write('%s%s="%s"' % (pre, attr[0], xmlize(attr[1])))

        if attr_len > 1: out.write(pre)
        if self._text is None and len(self._children) == 0:
            out.write("/>\n")
            return
        if self._text is not None:
            out.write(">%s</%s>\n" % (xmlize(self._text), self._name))
            return
        out.write(">\n")

        sub = indent + "  "
        for child in self._children:
            child._print(out, sub)
        
        out.write("%s</%s>\n" % (indent, self._name))

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
        return node

class _Graphics(Graphics):
    def __init__(self, x, y, width, height, clazz = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clazz = clazz
        self.mirrored = False
    def setClass(self, clazz):
        self.clazz = clazz
    def _node(self, name):
        node = _SvgNode(name)
        if self.clazz is not None:
            node.attr("class", self.clazz)
        return node
    def mirror(self): self.mirrored = not self.mirrored

class _Rectangle(_Graphics):
    def __init__(self, x, y, width, height, clazz = None):
        _Graphics.__init__(self, x, y, width, height, clazz)

    def _node(self):
        node = _Graphics._node(self, "rect")
        return node.attr("x", self.x).attr("y", self.y).attr("width", self.width).attr("height", self.height)

class _Line(_Graphics):
    def __init__(self, x, y, width, height, clazz = None):
        _Graphics.__init__(self, x, y, width, height, clazz)

    def _node(self):
        node = _Graphics._node(self, "line")
        return node.attr("x1", self.x).attr("y1", self.y)\
            .attr("x2", self.x + self.width).attr("y2", self.y + self.height)

class _Poly(_Graphics, PolyGraphics):
    def __init__(self, x, y, clazz = None):
        _Graphics.__init__(self, x, y, 0, 0, clazz)
        self.points = [(x, y)]

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
        node = _Graphics._node(self, "polyline")
        node.attr("points", " ".join("%s,%s" % pt for pt in self.points))
        scale = 1
        if self.mirrored: scale = -1
        return _SvgTransform().scale(scale, 1).set(node)

class _Reference(_Graphics):
    def __init__(self, x, y, ref, clazz = None):
        _Graphics.__init__(self, x, y, 0, 0, clazz)
        self.ref = ref

    def _node(self):
        node = _Graphics._node(self, "use")
        node.attr("xlink:href", "#" + self.ref)
        scale = 1
        if self.mirrored: scale = -1
        return _SvgTransform().translate(self.x, self.y).scale(scale, 1).set(node)

class _Text(_Graphics, TextGraphics):
    def __init__(self, x, y, text, clazz = None):
        _Graphics.__init__(self, x, y, 0, 0, clazz)
        self.text = text
        self.anchor = None

    def alignStart(self):
        self.anchor = "start"

    def alignMiddle(self):
        self.anchor = None

    def alignEnd(self):
        self.anchor = "end"

    def _node(self):
        node = _Graphics._node(self, "text")
        node.text(self.text)
        if self.anchor is not None:
            node.style("text-anchor", self.anchor)
        scale = 1
        if self.mirrored: scale = -1
        return _SvgTransform().translate(self.x, self.y).scale(scale, 1).set(node)

class SvgPredefines(Predefines):
    def __init__(self):
        self.defs = {}

    def canvas(self, name, offX, offY, clazz = None):
        o = SvgCanvas(offX, offY, clazz)
        self.defs[name] = o
        return o

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
        for name in sorted(self.defs.keys()):
            node.add(self.defs[name]._node().attr("xml:id", name))
        return node

class SvgCanvas(Canvas, _Graphics):
    def __init__(self, x, y, clazz = None):
        _Graphics.__init__(self, x, y, 0, 0, clazz)
        self.objects = []

    def setOff(self, x, y):
        self.x = x
        self.y = y
    def _add(self, obj):
        self.objects.append(obj)
        return obj

    def canvas(self, x, y, clazz = None):
        return self._add(SvgCanvas(x, y, clazz))
    def rectangle(self, x, y, width, height, clazz = None):
        return self._add(_Rectangle(x, y, width, height, clazz))
    def line(self, x, y, width, height, clazz = None):
        return self._add(_Line(x, y, width, height, clazz))
    def poly(self, startX, startY, clazz = None):
        return self._add( _Poly(startX, startY, clazz))
    def ref(self, x, y, name, clazz = None):
        return self._add(_Reference(x, y, name, clazz))
    def text(self, x, y, content, clazz = None):
        return self._add(_Text(x, y, content, clazz))

    def _node(self):
        node = _Graphics._node(self, "g")
        scale = 1
        if self.mirrored: scale = -1
        _SvgTransform().translate(self.x, self.y).scale(scale, 1).set(node)

        for obj in self.objects:
            node.add(obj._node())
        return node

class Rule:
    def __init__(self, name):
        self.names = [name]
        self.declarations = {}

    def attach(self, name):
        self.names.append(name)
        return self

    def decl(self, name, value):
        self.declarations[name] = value
        return self

    def text(self):
        return "\n    " + ", ".join(self.names) + " {" + \
            "".join("\n        %s: %s;" % (name, self.declarations[name]) for name in sorted(self.declarations.keys())) + \
            "\n    }\n"

class Styles:
    def __init__(self):
        self.rules = []
    def add(self, rule):
        self.rules.append(rule)
        return self
    def _node(self):
        return _SvgNode("style").attr("type", "text/css").text("".join(rule.text() for rule in self.rules) + "  ")

class SvgPrinter(Printer):
    def __init__(self):
        self._width = 1
        self._height = 1
        self._styles = Styles()\
            .add(Rule("text")\
                 .decl("font-family", "sans-serif")\
                 .decl("font-size", "8pt")\
                 .decl("stroke", "none")\
                 .decl("fill", "#333")\
                 .decl("text-anchor", "middle"))\
            .add(Rule("text.object")\
                 .decl("text-decoration", "underline"))\
            .add(Rule("rect")\
                 .decl("stroke", "black")\
                 .decl("stroke-linecap", "butt")\
                 .decl("fill", "#ffa"))\
            .add(Rule(".signal")\
                 .attach(".line")\
                 .decl("stroke", "black")\
                 .decl("stroke-linecap", "butt")\
                 .decl("fill", "none"))\
            .add(Rule(".block")\
                 .decl("stroke", "black")\
                 .decl("stroke-linecap", "butt")\
                 .decl("fill", "black"))\
            .add(Rule(".lifeline")\
                 .attach(".return")\
                 .decl("stroke", "black")\
                 .decl("stroke-dasharray", "5 5"))\
            .add(Rule(".destroy")\
                 .decl("stroke", "black")\
                 .decl("stroke-width", "2")\
                 .decl("stroke-linecap", "butt")\
                 .decl("fill", "none"))

        self._defs = SvgPredefines()
        self._canvas = SvgCanvas(0, 0)
    def defs(self): return self._defs

    def canvas(self, margin, width, height):
        self._width = width + 2 * margin
        self._height = height + 2 * margin
        self._canvas.x = margin
        self._canvas.y = margin
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
            .add(self._styles._node())\
            .add(self._defs._node())\
            .add(self._canvas._node())
        print '<?xml version="1.0" encoding="utf-8" standalone="no"?>'
        svg._print(out, "")
