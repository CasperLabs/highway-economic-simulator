# from __future__ import annotations
from typing import List, Dict
from numpy import uint8, uint16, uint32, uint64
from collections import OrderedDict
from sortedcontainers import SortedSet

from .constants import *
from .message import *


class ValidatorBase:
    def __init__(self, weight: uint64, name: str):
        self.weight = weight  # number of staked tokens
        self.reward_balance = 0  # remaining owned tokens
        self.round_exponents = OrderedDict()
        self.name = name
        self.assigned_ticks = SortedSet([0])

        self.era_state = None
        self.env = None

    def send_reward(self, amount):
        self.reward_balance += amount

    def determine_new_round_exponent(self):
        raise Exception("Method not defined")

    def get_prop_msg_size(self):
        raise Exception("Method not defined")

    def _update_round_exponent(self, tick):
        # Called before the start of every new round
        new_round_exponent = self.determine_new_round_exponent()
        self.round_exponents[tick] = new_round_exponent
        return new_round_exponent

    def send_prop_msg(self, round_, tick):
        size = self.get_prop_msg_size()
        msg = Message(self, size, PROP_MSG, tick, round_)
        round_.messages.append(msg)
        msg.propagate(self.env)

    def send_conf_msg(self, round_, tick):
        msg = Message(self, AVERAGE_CONF_SIZE, CONF_MSG, tick, round_)
        round_.messages.append(msg)
        msg.propagate(self.env)

    def send_wit_msg(self, round_, tick):
        msg = Message(self, AVERAGE_WIT_SIZE, WIT_MSG, tick, round_)
        round_.messages.append(msg)
        msg.propagate(self.env)

    def set_shared_state(self, era_state, env):
        self.era_state = era_state
        self.env = env
        self.action = env.process(self.run())

    def execute_round(self):
        # Initialize and get the round instance
        self.era_state.init_round_if_not_already(self.env.now)
        round_ = self.era_state.rounds_dict[self.env.now]

        # Round length for the given validator
        round_length = 2 ** self.round_exponents[round_.beginning_tick]

        conf_delay = round(round_length * R_0)
        wit_delay = round(round_length * (R_1 - R_0))

        if self is round_.leader:
            # print('Round %d\'s assigned_vld = %s, leader = %s'%(round_.beginning_tick, round_.assigned_validators, round_.leader))
            # print('Sending prop at', self.env.now)
            self.send_prop_msg(round_, self.env.now)
            yield self.env.timeout(conf_delay + wit_delay)
        else:
            yield self.env.timeout(conf_delay)
            # print('Sending conf at', self.env.now)
            self.send_conf_msg(round_, self.env.now)
            yield self.env.timeout(wit_delay)

        self.send_wit_msg(round_, self.env.now)

    def run(self):
        round_counter = 0

        # Announce the first round exponent
        current_round_exponent = self._update_round_exponent(0)

        while True:
            # print("For vld", self.name, "time is", self.env.now)
            # Calculate the new round exponent
            current_tick = self.env.now
            new_round_length = 2 ** current_round_exponent

            # Add the next tick in advance
            # This is necessary to find out assigned validators when creating
            # the next round instance
            self.assigned_ticks.add(current_tick + new_round_length)

            round_action = self.env.process(self.execute_round())

            yield self.env.timeout(new_round_length - 1)

            current_round_exponent = self._update_round_exponent(
                current_tick + new_round_length
            )

            yield self.env.timeout(1)
            round_counter += 1

    def __repr__(self):
        return self.name
