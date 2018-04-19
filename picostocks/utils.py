# -*- coding: utf-8 -*-

def decimal2string(value, decimal_places=18):
    value = str(float(value))
    prefix, postfix = value.split(".")
    postfix += "0" * (decimal_places - len(postfix))
    return "%s.%s" % (prefix, postfix)
