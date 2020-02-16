# from __future__ import annotations
from typing import List, Dict
from numpy import uint8, uint16, uint32, uint64
from collections import OrderedDict

from .constants import *
from .validator_base import ValidatorBase

ACCELERATION_PARAMETER = 10


class SimpleValidator(ValidatorBase):
    constant_round_exponent: uint64

    def set_constant_round_exponent(self, re: uint64):
        self.constant_round_exponent = re

    def calculate_new_round_exponent(self):
        return self.constant_round_exponent

    def get_prop_msg_size(self):
        return 15000 * 8  # bits
