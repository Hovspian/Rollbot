#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


def prt(message, enable_verbose):
    """A print function wrapper.
    
    :param enable_verbose: boolean value
    """
    if enable_verbose:
        print(message)
