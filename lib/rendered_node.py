from role import re_rolename
from connection import re_ingress
from connection import re_egress

class RenderedNode(object):

    def __init__(self, anclnode, engine):
        self._node = anclnode
        self._name = anclnode.name
        self._engine = engine
        self._roles = set()
        for r in anclnode.roles:
            m = re_rolename.match(r)
            if m.group("model") == "grouprole":
                for grm in self._engine.group(r).roles:
                    self._roles.add(grm)
            else:
                self._roles.add(r)
        self._listeners = []

    def add_listener(self, port, protocol):
        if [port,protocol] not in self._listeners:
            self._listeners.append([port,protocol])

    @property
    def name(self):
        "String representation of this node's name"
        return self._name

    @property
    def roles(self):
        """Returns a list of strings for the roles for this rendered node
        - includes roles expanded from grouproles
        - excludes grouproles themselves"""
        return list(self._roles)

    def has_role(self,rolename):
        """Checks to see if the string argument 'role' is in the list of roles
        - includes roles expanded from grouproles
        - excludes grouproles themelves"""
        return rolename in self._roles

    def role(self, rolename):
        """Returns the Role object for this rolename if it exists on this
        RenderedNode. Otherwise, returns None"""
        if self.has_role(rolename): return self._engine.role(rolename)
        return None

    def has_listener(self, port, protocol):
        """Returns T/F whether port/protocol is in the list of known listeners"""
        return [port,protocol] in self._listeners

    def has_ingress(self, rolename, service):
        if not self.has_role(rolename): return False
        r = self.role(rolename)
        return r.ingress(service) is not None

    def find_ingress_by_port(self, port, protocol):
        ingress = []
        for r in self._roles:
            if self._engine.role(r) is None: continue
            i = self._engine.role(r).find_ingress_by_port(port,protocol)
            if i is not None and i not in ingress:
                ingress.append(i)
        ret = []
        for i in ingress:
            m = re_ingress.match(i)
            ret.append(["%s::%s::%s"%(m.group("context"),m.group("model"),m.group("component")),m.group("service")])
        return ret

    @property
    def egresses(self):
        ret = []
        for r in self._roles:
            for e in self._engine.role(r).egresses:
                if e not in ret: ret.append(e)
        return ret

    def has_egress(self, rolename, service):
        if re_ingress.match("%s::%s"%(rolename,service)) is None: return False
        for r in self._roles:
            if self._engine.role(r).has_egress("%s::%s"%(rolename, service)): return True
        return False

    def roles_with_egress(self, rolename, service):
        if re_ingress.match("%s::%s"%(rolename,service)) is None: return False
        ret = []
        for r in self._roles:
            if self._engine.role(r).has_egress("%s::%s"%(rolename, service)) and r not in ret:
                ret.append(r)
        return ret
