import re

re_ingress = re.compile("^(?P<context>[\w-]+)::(?P<model>\w+)::(?P<component>\w+)::(?P<service>\w+)$", re.IGNORECASE)
re_egress  = re.compile("^(?P<context>[\w-]+)::(?P<model>\w+)::(?P<component>\w+)::(?P<dep>\w+)::(?P<service>\w+)$", re.IGNORECASE)

class ConnectionSyntaxError(Exception): pass
class ConnectionHandlingError(Exception): pass

class Connection(object):

    @staticmethod
    def check_syntax(raw):
        if type(raw) != type({}): return "Connection invalid form: %s"%(raw)
        if not raw.has_key("ingress") and not raw.has_key("egress"):
            return "Connection invalid form - missing ingress or egress: %s"%(raw)
        if raw.has_key("ingress") and raw.has_key("egress"):
            return "Connection invalid form - has both ingress and egress: %s"%(raw)
        if not raw.has_key("with"): return "Connection invalid form - missing with"%(raw)
        if raw.has_key("ingress"): #ingress
            if type(raw["ingress"]) != type(""): return "Connection invalid form - ingress not str: %s"%(raw["ingress"])
            if re_ingress.match(raw["ingress"]) is None:
                return "Connection invalid form - ingress not correct format: %s"%(raw["ingress"])
            if type(raw["with"]) != type([]): return "Connection invalid form - with not str: %s"%(raw["with"])
            for w in raw["with"]:
                if re_ingress.match(w) is None:
                    return "Connection invalid form - with not correct format: %s"%(w)
        else: #egress
            if type(raw["egress"]) != type(""): return "Connection invalid form - egress not str: %s"%(raw)
            if re_egress.match(raw["egress"]) is None:
                return "Connection invalid form - egress not correct format: %s"%(raw)
            if type(raw["with"]) != type([]): return "Connection invalid form - with not str: %s"%(raw["with"])
            for w in raw["with"]:
                if re_egress.match(w) is None:
                    return "Connection invalid form - with not correct format: %s"%(w)

    def __convert_from_dict(self, raw):
        if raw.has_key("ingress"): #ingress
            self._direction = "ingress"
            self._src       = raw["ingress"]
            self._dst       = raw["with"]
        else: # egress
            self._direction = "egress"
            self._src       = raw["egress"]
            self._dst       = raw["with"]

    def __init__(self, raw):
        try:
            c = Connection.check_syntax(raw)
            if c is not None:
                raise ConnectionSyntaxError(c)
            self.__convert_from_dict(raw)
        except StandardError, e:
            raise ConnectionHandlingError()

    @property
    def direction(self):
        return self._direction

    def is_ingress(self):
        return self._direction == "ingress"

    def is_egress(self):
        return self._direction == "egress"

    @property
    def src(self):
        return self._src

    @property
    def dst(self):
        return self._dst
