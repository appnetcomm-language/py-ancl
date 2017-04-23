import yaml
from model import *
from connection import *
from grouprole import *
from node import *
from role import *
from rendered_node import *
import copy
import os
import ipaddress

class ConnectionAlreadyExistsError(Exception): pass
class NodeAlreadyExistsError(Exception): pass
class GroupAlreadyExistsError(Exception): pass

class EngineRenderError(Exception): pass
class MissingModelRenderError(EngineRenderError): pass
class MissingGroupRoleRenderError(EngineRenderError): pass

class Engine(object):

    def __init__(self):
        self._models = {}
        self._connections = []
        self._groups = {}
        self._nodes  = {}
        self._roles  = {}
        self._rendered_nodes = {}

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
    def num_groups(self):
        return len(self._groups.keys())

    def group(self, groupname):
        if self._groups.has_key(groupname):
            return self._groups[groupname]
        return None

    @property
    def num_nodes(self):
        return len(self._nodes.keys())

    def node(self, nodename):
        if type(nodename) == type(""):
            nodename = ipaddress.ip_network(nodename)
        if self._nodes.has_key(nodename):
            return self._nodes[nodename]
        return None

    @property
    def num_rendered_nodes(self):
        return len(self._rendered_nodes.keys())

    def rendered_node(self, nodename):
        if type(nodename) == type(""):
            nodename = ipaddress.ip_network(nodename)
        if self._rendered_nodes.has_key(nodename):
            return self._rendered_nodes[nodename]
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
                    naip = ipaddress.ip_network(na.name)
                    if self._nodes.has_key(naip):
                        raise NodeAlreadyExistsError(na.name)
                    else:
                        self._nodes[naip] = na
            if d.has_key("groups"):
                for g in d["groups"]:
                    ga = GroupRole(g)
                    if self._groups.has_key(ga.name):
                        raise GroupAlreadyExistsError(ga.name)
                    else:
                        self._groups[ga.name] = ga

    def add_directory(self, dirname):
        for f in os.listdir(dirname):
            fname = "%s/%s"%(dirname,f)
            if f[0] == ".": continue # Catchs this dir, parent dir, dotfiles
            if os.path.isfile(fname):
                if f[-5:] != ".ancl": continue
                self.add_file(fname)
            elif os.path.isdir(fname):
                self.add_directory(fname)
            # else skip it

    def validate(self):
        # ensure that the sum of this environment is valid according to the
        # requires of the spec
        pass

    def _render_roles(self):
        for nn, no in self._nodes.items():
            for r in no.roles:
                m = re_rolename.match(r)
                if m.group("model") != "grouprole":
                    if not self._roles.has_key(r):
                        self._render_role(r)
        for _, go in self._groups.items():
            for r in go.roles:
                if not self._roles.has_key(r):
                    self._render_role(r)

    def _render_role(self, rolename):
        r = Role(rolename)
        m = self.model(r.modelname)
        if m is None: raise MissingModelRenderError(rolename)
        c = m.component(r.componentname)
        if c is None: raise MissingModelRenderError()
        r.associate_component(m,c)
        for iname in c.list_ingress():
            r.add_ingress(c.ingress(iname))
        for ename in c.list_egress():
            r.add_egress(c.egress(ename))
        self._roles[rolename] = r

    def _render_connections(self):
        for c in self._connections:
            self._render_connection(c)

    def _render_connection(self, c):
            if c.direction == "ingress":
                # "ingress" replacement
                # Foreach role, see if that are any egresses which have this connection
                # referenced and hence need to be substituted
                dcontext, dmodel, dcomponent, dservice = c.src.split("::")
                i = "%s::%s::%s"%(dcontext, dmodel, dcomponent)
                to_egresses = []
                for to_egress in c.dst:
                    toe_context, toe_model, toe_component, toe_service = to_egress.split("::")
                    to_egresses.append(["%s::%s::%s"%(toe_context, toe_model, toe_component), toe_service])
                for rn, ro in self._roles.items():
                    if [i,dservice] in ro.egresses:
                        ro.replace_egress([i,dservice],to_egresses)
            else: # egress
                # "egress" replacement
                # very targetted so only need to look at a specific role to update
                dcontext, dmodel, dcomponent, ddepcomponent, ddepservice = c.src.split("::")
                r = "%s::%s::%s"%(dcontext, dmodel, dcomponent)
                i = "%s::%s::%s"%(dcontext, dmodel, ddepcomponent)
                to_egresses = []
                for to_egress in c.dst:
                    toe_context, toe_model, _, toe_component, toe_service = to_egress.split("::")
                    to_egresses.append(["%s::%s::%s"%(toe_context, toe_model, toe_component), toe_service])
                self._roles[r].replace_egress([i, ddepservice], to_egresses)

    def _render_nodes(self):
        for nn, no in self._nodes.items():
            self._render_node(nn, no)

    def _render_node(self, nn, no):
        rn = RenderedNode(no, self)
        self._rendered_nodes[nn] = rn

    def render(self):
        self._render_roles()
        self._render_connections()
        self._render_nodes()

    def role(self, rolename):
        if self._roles.has_key(rolename):
            return self._roles[rolename]
        return None

    def find_flow(self, localip, localport, foreignip, foreignport, protocol):
        "find_flow identifies the egress and ingress relationship based on actual network communication"
        ret = []
        if type(localip) == type(str): localip = ipaddress.ip_network(localip)
        if type(foreignip) == type(str): foreignip = foreignip.ip_network(foreignip)
        lrn = self.rendered_node(localip)
        frn = self.rendered_node(foreignip)
        if lrn is None or frn is None: return None
        # first step is to identify the listener
        if lrn.has_listener(localport,protocol):
            # if listening, then it's an ingress
            possible_ingresses = lrn.find_ingress_by_port(localport,protocol)
            for pi in possible_ingresses:
                for er in frn.roles_with_egress(pi[0],pi[1]):
                    if [er, pi] not in ret: ret.append([er,pi])
        else:
            possible_ingresses = frn.find_ingress_by_port(foreignport,protocol)
            for pi in possible_ingresses:
                for er in lrn.roles_with_egress(pi[0],pi[1]):
                    if [er,pi] not in ret: ret.append([er,pi])
        return ret
