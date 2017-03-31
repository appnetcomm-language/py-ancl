import re

re_rolename = re.compile("^(?P<context>\w+)::(?P<model>\w+)::(?P<component>\w+)$", re.IGNORECASE)
