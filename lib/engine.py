import yaml
from model import *
from connection import *
from node import *

class ConnectionAlreadyExistsError(Exception): pass
class NodeAlreadyExistsError(Exception): pass

class Engine(object):

    def __init__(self):
        self._models = {}
        self._connections = []
        self._nodes  = {}

    @property
    def num_models(self):
        return len(self._models.keys())

    def model(self, modelname):
        if self._models.has_key(modelname):
            return self._models[modelname]
        return None

    @property
    def num_connections(self):
        return len(self._connections)

    def connection(self, ingress=None, egress=None):
        if ingress is not None:
            for c in self._connections:
                if c.direction == "ingress" and c.src == ingress:
                    return c
        if egress is not None:
            for c in self._connections:
                if c.direction == "egress" and c.src == egress:
                    return c
        return None

    @property
    def num_nodes(self):
        return len(self._nodes.keys())

    def node(self, nodename):
        if self._nodes.has_key(nodename):
            return self._nodes[nodename]
        return None

    def add_file(self, filename):
        with open(filename) as f:
            d = yaml.load(f)
            if d.has_key("models"):
                for m in d["models"]:
                    ma = Model(m)
                    if self._models.has_key(ma.name):
                        self._models[ma.name].merge(ma)
                    else:
                        self._models[ma.name] = ma
            if d.has_key("connections"):
                for c in d["connections"]:
                    ca = Connection(c)
                    if ca in self._connections:
                        raise ConnectionAlreadyExistsError()
                    else:
                        self._connections.append(ca)
            if d.has_key("nodes"):
                for n in d["nodes"]:
                    na = Node(n)
                    if self._nodes.has_key(na.name):
                        raise NodeAlreadyExistsError()
                    else:
                        self._nodes[na.name] = n
