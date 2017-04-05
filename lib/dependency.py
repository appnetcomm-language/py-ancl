import re

re_modeldep = re.compile("^([\w-])+::([\w-])+$", re.IGNORECASE)

class DependencySyntaxError(Exception): pass
class DependencyHandlingError(Exception): pass

class Dependency(object):

    @staticmethod
    def check_syntax(raw):
        if type(raw) != type({}): return "Dependency invalid form: %s"%(raw)
        if not raw.has_key("name"): return "Dependency invalid form - no name: %s"%(raw)
        if type(raw["name"]) != type(""): return "Dependency invalid form - name not str: %s"%(raw["name"])
        if re_modeldep.match(raw["name"]) is None:
            return "%s Dependency invalid form - not COMPONENT::SERVICE"%(raw)

    def __convert_from_dict(self, raw):
        self._name = raw["name"]

    def __init__(self, raw):
        try:
            c = Dependency.check_syntax(raw)
            if c is not None:
                raise DependencySyntaxError(c)
        except StandardError, e:
            raise DependencyHandlingError(e)
        try:
            self.__convert_from_dict(raw)
        except StandardError, e:
            raise DependencyHandlingError(e)

    @property
    def name(self):
        return self._name
