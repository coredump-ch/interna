#!/usr/bin/env python
import os
import sys
import pytest


PYTHONPATH_DIRS = ['.']


if __name__ == '__main__':

    for pathdir in PYTHONPATH_DIRS:
        fullpath = os.path.join(os.path.dirname(__file__), pathdir)
        sys.path.insert(0, fullpath)

    pytest.main()
