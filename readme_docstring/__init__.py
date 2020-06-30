__all__ = ['getdoc', 'getspec', 'getmodules',
           'getmembers', 'getclasses', 'getfunctions', 'Table', 'Classes', 'Functions']


import inspect
import markdown_table
import os
import pydoc
import readme_docstring
import setupcfg


def getdoc(obj):
    """return first line of an object docstring"""
    doc = inspect.getdoc(obj) if obj.__doc__ else ""
    return doc.split("\n")[0].strip()


def getspec(routine):
    """return a string with Python routine specification"""
    doc = pydoc.plain(pydoc.render_doc(routine))
    return doc.splitlines()[2]


def getmodules():
    """return a list of modules"""
    if not os.path.exists("setup.cfg"):
        raise OSError("setup.cfg NOT EXISTS")
    return setupcfg.getmodules()


def getmembers():
    """return all the members defined in `__all__` in a list of (name, value) pairs """
    objects = []
    for module in readme_docstring.getmodules():
        __all__ = getattr(module, "__all__", [])
        members = inspect.getmembers(module)
        objects += list(map(lambda m: m,
                            filter(lambda m: m[0] in __all__, members)))
    return list(objects)


def getclasses():
    """return a list of classes defined in `__all__`"""
    classes = []
    for name, member in getmembers():
        if inspect.isclass(member):
            classes.append(member)
    return classes


def getfunctions():
    """return a list of functions defined in `__all__`"""
    functions = []
    for name, member in getmembers():
        if inspect.isroutine(member):
            functions.append(member)
    return functions


class Table(markdown_table.Table):
    """abstract table class. attrs: `headers`, `objects`"""
    columns = ["name", "`__doc__`"]
    objects = []

    def __init__(self, objects):
        self.objects = list(objects)

    def getleftcell(self, obj):
        name = obj.__module__ + '.' + obj.__name__
        if inspect.isroutine(obj):
            value = readme_docstring.getspec(obj)
            value = value.replace("self, ", "").replace("(self)", "()")
            name = obj.__module__ + '.' + value
        return "`%s`" % name

    def getrightcell(self, obj):
        return readme_docstring.getdoc(obj)

    def getmatrix(self):
        data = []
        for obj in self.objects:
            left = self.getleftcell(obj)
            right = self.getrightcell(obj)
            data.append([left, right])
        return data


class Classes(Table):
    """`classes` table class. attrs: `classes`"""
    columns = ["class", "`__doc__`"]

    def __init__(self, classes=None):
        if not classes:
            classes = getclasses()
        self.objects = list(classes)


class Functions(Table):
    """`functions` table class. attrs: `functions`"""
    columns = ["function", "`__doc__`"]

    def __init__(self, functions=None):
        if not functions:
            functions = getfunctions()
        self.objects = list(functions)
