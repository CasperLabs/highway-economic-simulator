# from __future__ import annotations
from typing import List, Dict
import numpy as np
from numpy import uint8, uint16, uint32, uint64
from numpy.random import choice
from collections import OrderedDict

from .helper import get_total_weight
from .message import *

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
    ):
        self.beginning_tick = beginning_tick
        self.assigned_validators = assigned_validators
        self.punished_validators = []
        self.reward_weight = None
        self.insufficient_weight = False

        # Assign a leader randomly, based on weight
        self.leader = choice(assigned_validators, 1, [v.weight for v in assigned_validators])[0]

        self.messages = []

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

    def get_level_1_committee(self, only_in_round_messages=True):

        if only_in_round_messages:
            messages = []
            for m in self.messages:
                end_tick = self.beginning_tick + 2**m.sender.round_exponents[self.beginning_tick]
                if m.tick < end_tick:
                    messages.append(m)
        else:
            messages = self.messages

        n_validators = len(self.assigned_validators)
        vld_idx = {}
        for i, v in enumerate(self.assigned_validators):
            vld_idx[v] = i

        relation_matrix = np.zeros((n_validators, n_validators), dtype=bool)

        prop_messages = [m for m in messages if m.type_ is PROP_MSG]

        # If no PROP message is found, the committee is automatically an empty set
        if len(prop_messages) == 0:
            return []
        elif len(prop_messages) == 1:
            prop_msg = prop_messages[0]
        else:
            raise Exception('Each round can only have 1 PROP message')

        conf_messages = [m for m in messages if m.type_ is CONF_MSG]
        wit_messages = [m for m in messages if m.type_ is WIT_MSG]

        c0 = set([self.leader])
        for m in conf_messages:
            if prop_msg in m.justified_messages:
                relation_matrix[vld_idx[m.sender], vld_idx[prop_msg.sender]] = True
                c0.add(m.sender)

        for m_w in wit_messages:
            for m_c in m_w.justified_messages:
                if m_c in conf_messages:
                    relation_matrix[vld_idx[m_w.sender], vld_idx[m_c.sender]] = True

        c1 = set()
        for i in range(n_validators):
            for j in range(i+1, n_validators):
                if relation_matrix[i, j] and relation_matrix[j, i]:
                    c1.add(self.assigned_validators[i])
                    c1.add(self.assigned_validators[j])

        # for m in messages:
        #     print(m, m.justified_messages)

        # print(relation_matrix)
        # print(c1)

        return c1





