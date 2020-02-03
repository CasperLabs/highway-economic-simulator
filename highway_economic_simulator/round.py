# from __future__ import annotations
from typing import List, Dict
from numpy import uint8, uint16, uint32, uint64
from collections import OrderedDict

from .helper import get_total_weight

class Round:
    assigned_validators: List['ValidatorBase']
    punished_validators: List['ValidatorBase'] # punished for underestimation
    round_exponents_dict: Dict['Validator', uint64]
    beginning_tick: uint64
    reward_weight: uint64
    insufficient_weight: bool

    def __init__(
            self,
            beginning_tick: uint64,
            assigned_validators: List['ValidatorBase'],
            round_exponents_dict: Dict['Validator', uint64]
    ):
        self.beginning_tick = beginning_tick
        self.assigned_validators = assigned_validators
        self.punished_validators = []
        self.reward_weight = None
        self.round_exponents_dict = round_exponents_dict
        self.insufficient_weight = False

    def get_assigned_weight(self) -> uint64:
        return get_total_weight(self.assigned_validators)

    def set_reward_weight(self, reward_weight: uint64):
        self.reward_weight = reward_weight

    def get_round_exponent(self, validator: 'Validator') -> uint64:
        if validator in self.assigned_validators:
            return self.round_exponents_dict[validator]
        else:
            raise Exception('Validator not assigned to round')

    def set_otf_status(self, otf_status: bool):
        self.otf_status = otf_status

    def set_ef_status(self, eventual_contributing_weight: uint64):
        self.eventual_contributing_weight = eventual_contributing_weight

    def set_final_rewards(self, otf_reward: uint64, ef_reward: uint64):
        self.otf_reward = otf_reward
        self.ef_reward = ef_reward

    def set_insufficient_weight(self, status: bool):
        self.insufficient_weight = status
