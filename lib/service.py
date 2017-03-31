import re

re_port = re.compile("^(?P<startport>\d+)(-(?P<endport>\d+))?/(?P<protocol>tcp|udp)$", re.IGNORECASE)
re_protocol = re.compile("^tcp|udp$", re.IGNORECASE)

class ServiceSyntaxError(Exception): pass
class ServiceHandlingError(Exception): pass

class Service(object):

    @staticmethod
    def check_syntax(raw):
        if not raw.has_key("name"): return "Service missing name: %s"%(raw)
        if raw.has_key("ports"):
            if type(raw["ports"]) != type([]): return "%s ports invalid - not an array"%(raw["name"])
            for rp in raw["ports"]:
                if type(rp) != type(""): return "%s ports invalid - value '%s' not a str"%(raw["name"], rp)
                m = re_port.match(rp)
                if m is None: return "%s ports %s invalid format"%(raw["name"],rp)
                if re_protocol.match(m.group("protocol")) is None:
                    return "%s ports '%s' invalid protocol %s"%(raw["name"], rp, m.group("protocol"))
                if m.group("endport") is not None:
                    if int(m.group("startport")) > int(m.group("endport")):
                        return "%s ports '%s' invalid - startport > endport"%(raw["name"],rp)

    def __convert_from_dict(self, raw):
        self._raw  = raw
        self._name = raw["name"]
        self._ports = {}
        if raw.has_key("ports"):
            for r in raw["ports"]:
                m = re_port.match(r)
                if m.group("endport"):
                    self._ports[r] = {
                        "start": int(m.group("startport")),
                        "end":   int(m.group("endport")),
                        "protocol": m.group("protocol")
                    }
                else:
                    self._ports[r] = {
                        "start": int(m.group("startport")),
                        "end":   int(m.group("startport")),
                        "protocol": m.group("protocol")
                    }

    def __init__(self, raw):
        try:
            c = Service.check_syntax(raw)
            if c is not None:
                raise ServiceSyntaxError(c)
        except StandardError, e:
            raise ServiceHandlingError(e)
        try:
            self.__convert_from_dict(raw)
        except StandardError, e:
            raise ServiceHandlingError(e)

    @property
    def name(self):
        return self._name

    @property
    def abstract(self):
        return len(self._ports.keys()) == 0

    @property
    def ports(self):
        return self._ports.keys()

    def port(self,portid):
        if not self._ports.has_key(portid): return None
        return [ self._ports[portid]["start"], self._ports[portid]["end"], self._ports[portid]["protocol"] ]
