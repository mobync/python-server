# Copyright (c) Mobync.
# See LICENSE for details.

"""
mobync: The Library for online-offline synchronization
"""

import sys

from mobync.diff import OperationType, Diff
from mobync.read_filter import ReadFilter, FilterType
from mobync.synchronizer import Synchronizer
from mobync.mobync import Mobync

__version__ = '0.2.0'
__author__ = 'Carlos Matheus'
__contact__ = 'mobync.lib@gmail.com'
__url__ = 'https://github.com/mobync'
__license__ = 'MIT'

if sys.version_info < (3, 5):
    raise Exception(
        "This version of mobync is not compatible with Python 3.4 " "or below."
    )
