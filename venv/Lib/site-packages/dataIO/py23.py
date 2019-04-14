#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A portable version of ``six``, provide basic python2/3 compatible utilities.
"""

import sys

if sys.version_info[0] == 3:
    str_type = str
    int_type = (int,)
    pk_protocol = 3
    is_py2 = False
    is_py3 = True
else:
    str_type = basestring
    int_type = (int, long)
    pk_protocol = 2
    is_py2 = True
    is_py3 = False


#--- Unittest ---
if __name__ == "__main__":
    def test():
        s = "text" # unicode string
        b = s.encode("utf-8") # bytes
        i = 32 # integer
        i_long = 1000000000000 # long integer
        f = 3.14 # float

        assert isinstance(s, str_type)
        assert isinstance(b, bytes)
        assert isinstance(i, int_type)
        assert isinstance(i_long, int_type)
        assert isinstance(f, float)
            
    test()