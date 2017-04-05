import re

re_rolename = re.compile("^(?P<context>[\w-]+)::(?P<model>[\w-]+)::(?P<component>[\w-]+)$", re.IGNORECASE)

class InvalidRoleNameError(Exception): pass
class InvalidRoleReplaceError(Exception): pass

class Role(object):

    def __init__(self, rolename):
        m = re_rolename.match(rolename)
        if m is None: raise InvalidRoleNameError()
        self._name          = rolename
        self._contextname   = m.group("context")
        self._modelname     = m.group("model")
        self._model         = None
        self._componentname = m.group("component")
        self._component     = None

        self._ingress = {}
        self._egress  = []

    def __str__(self):
        return str({
            "name":      self._name,
            "context":   self._contextname,
            "model":     self._modelname,
            "component": self._componentname,
            "ingress":   self._ingress,
            "egress":    self._egress,
        })

    def associate_component(self, model, component):
        self._model     = model
        self._component = component

    def add_ingress(self, ingress):
        self._ingress[ingress.name] = {
            "ports": []
        }
        for pn in ingress.ports:
            self._ingress[ingress.name]["ports"].append(ingress.port(pn))

    def add_egress(self, egress):
        depcomp, depserv = egress.name.split("::")
        self._egress.append([
            "%s::%s::%s"%(self._contextname, self._modelname, depcomp),
            depserv,
        ])

    def replace_egress(self, from_egress, to_egresses):
        self._egress.remove(from_egress)
        self._egress += to_egresses

    @property
    def name(self):
        return self._name

    @property
    def contextname(self):
        return self._contextname

    @property
    def modelname(self):
        return self._modelname

    @property
    def componentname(self):
        return self._componentname

    @property
    def ingresses(self):
        return self._ingress

    def list_ingress(self):
        return self._ingress.keys()

    def ingress(self, ingressname):
        if not self._ingress.has_key(ingressname): return None
        return self._ingress[ingressname]

    @property
    def egresses(self):
        return self._egress

    def list_egress(self):
        return self._egress.keys()

    def egress(self, egressname):
        if not self._egress.has_key(egressname): return None
        return self._egress[egressname]
