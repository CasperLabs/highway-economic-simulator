# from __future__ import annotations
from typing import List, Dict
from numpy import uint8, uint16, uint32, uint64
from collections import OrderedDict

from .constants import *
from .validator_base import ValidatorBase

class SimpleValidator(ValidatorBase):
    constant_round_exponent: uint64

    def set_constant_round_exponent(self, re: uint64):
        self.constant_round_exponent = re

    def calculate_new_round_exponent(self):
        return self.constant_round_exponent

    def probability_of_contributing_to_otf(self, round_exponent: uint64):
        return 1

    def probability_of_contributing_to_ef(self):
        return 1

