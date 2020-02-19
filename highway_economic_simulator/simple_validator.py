# from __future__ import annotations
from typing import List, Dict
from numpy import uint8, uint16, uint32, uint64
from collections import OrderedDict

from .constants import *
from .validator_base import ValidatorBase

ACCEL_PARAM = 100
BREAK_PARAM_C0 = 10
BREAK_PARAM_C1 = 40

TEST = 0


class SimpleValidator(ValidatorBase):
    def set_constant_round_exponent(self, re):
        # To be called before the simulation starts
        if self.env:
            assert(self.env.now == 0)

        self.constant_round_exponent = re

        self.next_adjustment_target = 0 + BREAK_PARAM_C1 * 2**re

    def check_break(self):

        current_tick = self.env.now

        ticks = list(self.era_state.rounds_dict.keys())
        assert(ticks == sorted(ticks))

        relevant_rounds = []
        counter = 0

        for r in reversed(self.era_state.rounds_dict.values()):
            if counter >= BREAK_PARAM_C1:
                break

            # Round exponents for new rounds are announced on the tick that is
            # right before the new round's beginning: (beginning_tick - 1)
            if current_tick <= r.get_last_tick()-1:
                continue
            else:
                relevant_rounds.append(r)
                counter += 1

        relevant_rounds.reverse()

        fail_counter = 0
        increase_round_exponent = False

        for r in relevant_rounds:
            if not r.is_otf_successful(self.era_state.q_OTF):
                fail_counter += 1
            if fail_counter >= BREAK_PARAM_C0:
                increase_round_exponent = True
                break

        # print("N_FAILS", fail_counter)
        # for r in relevant_rounds: print(r.beginning_tick, len(r.assigned_validators),r.is_otf_successful(self.era_state.q_OTF))

        return increase_round_exponent


    def calculate_new_round_exponent(self):
        global TEST

        current_tick = self.env.now
        if current_tick >= self.next_adjustment_target - 1:
            increase = self.check_break()
            if increase:
                self.constant_round_exponent += 1

            self.next_adjustment_target += BREAK_PARAM_C1 * 2**self.constant_round_exponent

        # print(self.constant_round_exponent)

        return self.constant_round_exponent

    def get_prop_msg_size(self):
        return 15000 * 8  # bits
