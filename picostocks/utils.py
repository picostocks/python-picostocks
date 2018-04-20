# -*- coding: utf-8 -*-
import decimal


def float2string(number, precision=18):
    return '{0:.{prec}f}'.format(
        decimal.Context(prec=100).create_decimal(str(number)),
        prec=precision,
    )
