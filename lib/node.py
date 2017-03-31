from role import re_rolename

class NodeSyntaxError(Exception): pass
class NodeHandlingError(Exception): pass

class Node(object):

    @staticmethod
    def check_syntax(raw):
        if type(raw) != type({}): return "Node invalid form: %s"%(raw)
        if not raw.has_key("name"): return "Node invalid form - no name: %s"%(raw)
        if type(raw["name"]) != type(""): return "Node invalid form - name not str: %s"%(raw["name"])
        if not raw.has_key("roles"): return "%s Node invalid form - no roles"%(raw["name"])
        if type(raw["roles"]) != type([]): return "%s Node invalid form - roles not array"%(raw["name"])
        for r in raw["roles"]:
            if type(r) != type(""): return "%s Node role invalid - not str: %s"%(raw["name"], r)
            if re_rolename.match(r) is None: return "%s Node role invalid - bad form: %s"%(raw["name"], r)

    def __convert_from_dict(self, raw):
        self._name = raw["name"]
        self._roles = []
        for r in raw["roles"]:
            if r not in self._roles: self._roles.append(r)

    def __init__(self, raw):
        try:
            c = Node.check_syntax(raw)
            if c is not None:
                raise NodeSyntaxError(e)
            self.__convert_from_dict(raw)
        except StandardError, e:
            raise NodeHandlingError(e)

    @property
    def name(self):
        return self._name

    @property
    def roles(self):
        return self._roles

    def has_role(self, rolename):
        return rolename in self._roles
