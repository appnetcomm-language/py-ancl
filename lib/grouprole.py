from role import *

class GroupRole(object):

    @staticmethod
    def check_syntax(raw):
        if type(raw) != type({}): return "Invalid GroupRole form %s"%(raw)
        if not raw.has_key("name"): return "Invalid GroupRole form - no name: %s"%(raw)
        if type(raw["name"]) != type(""): return "Invalid GroupRole form - name not str: %s"%(raw["name"])
        re = re_rolename.match(raw["name"])
        if re is None: return "Invalid GroupRole form - name not valid: %s"%(raw["name"])
        if re.group("model") != "grouprole": return "Invalid GroupRole - model is not literal grouprole: %s"%(raw["name"])
        if not raw.has_key("roles"): return "%s Invalid GroupRole form - no roles"%(raw["name"])
        if type(raw["roles"]) != type ([]): return "%s Invalid GroupRole form - roles not array"%(raw["name"])
        for r in raw["roles"]:
            if type(r) != type(""): return "%s GroupRole role invalid - not str: %s"%(raw["name"], r)
            if re_rolename.match(r) is None: return "%s GroupRole role invalid - invalid form: %s"%(raw["name"], r)

    def __convert_from_dict(self, raw):
        self._name = raw["name"]
        self._roles = []
        for r in raw["roles"]:
            if r not in self._roles: self._roles.append(r)

    def __init__(self, raw):
        try:
            c = GroupRole.check_syntax(raw)
            if c is not None:
                raise GroupRoleSyntaxError(c)
            self.__convert_from_dict(raw)
        except StandardError, e:
            raise GroupRoleHandlingError(e)

    @property
    def name(self):
        return self._name

    @property
    def roles(self):
        return self._roles
