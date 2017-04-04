from component import *

class ModelSyntaxError(Exception): pass
class ModelHandlingError(Exception): pass
class ModelMergeError(Exception): pass

class Model(object):

    @staticmethod
    def check_syntax(raw):
        if type(raw) != type({}): return "Model invalid form: %s"%(raw)
        if not raw.has_key("name"): return "Model invalid form - no name: %s"%(raw)
        if type(raw["name"]) != type(""): return "Model invalid form - name not str: %s"%(raw["name"])
        if not raw.has_key("components"): return "%s invalid form - no components"%(raw["name"])
        if type(raw["components"]) != type([]): return "%s invalid form - components not array: %s"%(raw["name"], raw["components"])
        seen = []
        for comp in raw["components"]:
            c = Component.check_syntax(comp)
            if c is not None: return "%s::%s"%(raw["name"], c)
            if comp["name"] in seen: return "%s::%s duplicate"%(raw["name"], comp["name"])
            seen.append(comp["name"])

    def __convert_from_dict(self, raw):
        self._name = raw["name"]
        self._components = {}
        for comp in raw["components"]:
            self._components[comp["name"]] = Component(comp)

    def __init__(self, raw):
        try:
            c = Model.check_syntax(raw)
            if c is not None:
                raise ModelSyntaxError(c)
            self.__convert_from_dict(raw)
        except StandardError, e:
            raise ModelHandlingError(e)

    @property
    def name(self):
        return self._name

    def list_components(self):
        return self._components.keys()

    def component(self, componentname):
        if not self._components.has_key(componentname): return None
        return self._components[componentname]

    def service(self, servicename):
        (cname, sname) = servicename.split("::", 1)
        c = self.component(cname)
        if c is None: return None
        if not c.ingress(sname): return None
        return self._components[cname].ingress(sname)

    def dependency(self, dependencyname):
        (cname, dname) = dependencyname.split("::", 1)
        c = self.component(cname)
        if c is None: return None
        if c.egress(dname) is None: return None
        return c.egress(dname)

    def merge(self, other):
        raise ModelMergeError("not implemented")
