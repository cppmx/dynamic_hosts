# -*- coding: utf-8 -*-
"""
Filename: console
Created on: 08/02/2019
Project name: dynamic_hosts
Author: Carlos Colon
Description: 
Changes:
    06/02/2019     CECR     Initial version
"""

import sys
import io
from contextlib import contextmanager


@contextmanager
def read_console(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, io.StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out
