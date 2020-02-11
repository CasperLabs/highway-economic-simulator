# from __future__ import annotations
from typing import List, Dict
from numpy import uint8, uint16, uint32, uint64
from collections import OrderedDict

class ValidatorBase:
    weight: uint64
    balance: uint64
    announced_round_exponents: List[uint64]

    def __init__(self, weight: uint64, name: str, balance:uint64=0):
        self.env = None
        self.weight = weight # number of staked tokens
        self.balance = balance # remaining owned tokens
        self.announced_round_exponents = []
        self.name = name

    def calculate_new_round_exponent(self, era_state: 'EraState'):
        raise Exception('Method not defined')

    def announce_round_exponent(self, era_state: 'EraState'):
        new_round_exponent = self.calculate_new_round_exponent(era_state)
        self.announced_round_exponents.append(new_round_exponent)

    def send_lambda_msg(self):
        pass

    def send_lambda_response_msg(self):
        pass

    def send_omega_msg(self):
        pass


    def probability_of_contributing_to_otf(self, round_exponent: uint64):
        raise Exception('Method not defined')

    def probability_of_contributing_to_ef(self):
        raise Exception('Method not defined')


    def round_counter(self, round_exponent):
        yield self.env.timeout(2**round_exponent)
        print("For vld", self.name, "round ended at", self.env.now)
        # self.action.interrupt()
        # yield self.env.timeout(self.env.now+2**round_exponent)
        # self.env.schedule(self.env.process(self.run()), delay=2**round_exponent)
        # pass

    def set_shared_state(self, era_state, env):
        self.era_state = era_state
        self.env = env
        self.action = env.process(self.run())

    def watch_round(self):
         # yield self.env.process(self.round_counter(14))
         action = self.env.process(self.execute_round(14))

    def execute_round(self):
        if self.env.now not in self.era_state.rounds_dict.keys():
            self.era_state.init_round()

        # import ipdb; ipdb.set_trace()
        # yield self.env.timeout(2**round_exponent)
        yield self.env.timeout(5)
        print(self.env.now)


    def run(self):
        round_counter = 0
        while True:
            print("For vld", self.name, "time is", self.env.now)
            # self.round_counter(14)

            round_action = self.env.process(self.execute_round())

            yield self.env.timeout(2**14)
            round_counter += 1

        # yield self.env.schedule(self.env.process(self.round_counter(14)))
    def __repr__(self):
        return self.name
