from service import *
from dependency import *

class ComponentSyntaxError(Exception): pass
class ComponentHandlingError(Exception): pass

class Component(object):

    @staticmethod
    def check_syntax(raw):
        if type(raw) != type({}): return "Component invalid form: %s"%(raw)
        if not raw.has_key("name"): return "Component invalid form - no name: %s"%(raw)
        if type(raw["name"]) != type(""): return "Component invalid form - name not str: %s"%(raw["name"])
        if not raw.has_key("ingress"): return "%s invalid form - no ingress"%(raw["name"])
        if type(raw["ingress"]) != type([]): return "%s invalid form - ingress not array: %s"%(raw["name"], raw["ingress"])
        seen = []
        for i in raw["ingress"]:
            c = Service.check_syntax(i)
            if c is not None: return "%s::%s"%(raw["name"], c)
            if i["name"] in seen: return "%s::%s duplicate"%(raw["name"], i["name"])
            seen.append(i["name"])
        if not raw.has_key("egress"): return "%s invalid form - no egress"%(raw["name"])
        if type(raw["egress"]) != type([]): return "%s invalid form - egress not array: %s"%(raw["name"], raw["egress"])
        seen = []
        for e in raw["egress"]:
            c = Dependency.check_syntax(e)
            if c is not None: return "%s::%s"%(raw["name"], c)
            if e["name"] in seen: return "%s::%s duplicate"%(raw["name"], e["name"])
            seen.append(e["name"])

    def __convert_from_dict(self, raw):
        self._name = raw["name"]
        self._ingress = {}
        for i in raw["ingress"]:
            self._ingress[i["name"]] = Service(i)
        self._egress = {}
        for e in raw["egress"]:
            self._egress[e["name"]] = Dependency(e)

    def __init__(self, raw):
        try:
            c = Component.check_syntax(raw)
            if c is not None:
                raise ComponentSyntaxError(c)
        except StandardError, e:
            raise ComponentHandlingError(e)
        try:
            self.__convert_from_dict(raw)
        except StandardError, e:
            raise ComponentHandlingError(e)

    @property
    def name(self):
        return self._name

    def list_ingress(self):
        return self._ingress.keys()

    def ingress(self, ingressname):
        if not self._ingress.has_key(ingressname): return None
        return self._ingress[ingressname]

    def list_egress(self):
        return self._egress.keys()

    def egress(self, egressname):
        if not self._egress.has_key(egressname): return None
        return self._egress[egressname]
