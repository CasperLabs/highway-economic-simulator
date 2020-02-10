# from __future__ import annotations
from typing import List, Dict
from numpy import uint8, uint16, uint32, uint64
from collections import OrderedDict

class ValidatorBase:
    weight: uint64
    balance: uint64
    announced_round_exponents: List[uint64]

    def __init__(self, weight: uint64, balance:uint64=0):
        self.weight = weight # number of staked tokens
        self.balance = balance # remaining owned tokens
        self.announced_round_exponents = []

    def calculate_new_round_exponent(self, era_state: 'EraState'):
        raise Exception('Method not defined')

    def announce_round_exponent(self, era_state: 'EraState'):
        new_round_exponent = self.calculate_new_round_exponent(era_state)
        self.announced_round_exponents.append(new_round_exponent)

    def probability_of_contributing_to_otf(self, round_exponent: uint64):
        raise Exception('Method not defined')

    def probability_of_contributing_to_ef(self):
        raise Exception('Method not defined')

