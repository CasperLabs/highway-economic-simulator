# from __future__ import annotations
from typing import List, Dict
from numpy import uint8, uint16, uint32, uint64
from collections import OrderedDict

from .helper import get_total_weight, calculate_q_otf, get_round_beginning_ticks
from .round import Round
from .constants import *

class EraState:
    validators: List['ValidatorBase']
    latest_tick: uint64
    initial_supply: uint64
    rounds_dict: Dict[uint64, Round]

    def __init__(
            self,
            env,
            initial_supply: uint64,
            seigniorage_rate=ERA_SEIGNIORAGE_RATE,
            fault_tolerance_threshold=FAULT_TOLERANCE_THRESHOLD,
            reward_weight_alpha=REWARD_WEIGHT_ALPHA,
            reward_weight_beta=REWARD_WEIGHT_BETA,
            reward_weight_gamma=REWARD_WEIGHT_GAMMA,
            ef_reward_delta=EF_REWARD_DELTA,
            underestimation_tolerance=UNDERESTIMATION_TOLERANCE,
            otf_ratio=OTF_RATIO,
    ):
        self.env = env
        self.validators = []
        self.rounds_dict = OrderedDict()
        self.initial_supply = initial_supply

        self.fault_tolerance_threshold = FAULT_TOLERANCE_THRESHOLD
        self.seigniorage_rate = ERA_SEIGNIORAGE_RATE
        self.reward_weight_alpha=REWARD_WEIGHT_ALPHA
        self.reward_weight_beta=REWARD_WEIGHT_BETA
        self.reward_weight_gamma=REWARD_WEIGHT_GAMMA
        self.ef_reward_delta=EF_REWARD_DELTA
        self.underestimation_tolerance=UNDERESTIMATION_TOLERANCE
        self.otf_ratio=OTF_RATIO

        self.latest_tick = 0

    def add_validator(self, validator: 'ValidatorBase'):
        self.validators.append(validator)

    def add_validators(self, validators: List['ValidatorBase']):
        for v in validators:
            self.add_validator(v)

    def calculate_reward_weights(self, q_OTF: uint64):
        # Calculate reward weight for each block/round
        for tick, round_ in self.rounds_dict.items():
            assigned_weight = round_.get_assigned_weight()
            if assigned_weight >= q_OTF:
                reward_weight = (
                    self.reward_weight_alpha*assigned_weight
                    + (1 - self.reward_weight_alpha)*self.reward_weight_beta
                    - self.reward_weight_beta*q_OTF
                )**self.reward_weight_gamma
            else:
                round_.set_insufficient_weight(True)
                reward_weight = 0

            round_.set_reward_weight(reward_weight)

    def determine_underestimated_rounds(self):
        for v in self.validators:
            counter = 0
            punishment = False

            for tick, round_ in self.rounds_dict.items():
                if v not in round_.assigned_validators:
                    continue

                if punishment and not round_.insufficient_weight:
                    round_.punished_validators.append(v)
                    punishment = False
                    counter = 0

                if round_.insufficient_weight:
                    counter += 1

                if counter >= self.underestimation_tolerance:
                    punishment = True

    def distribute_rewards(self):
        # Calculate relevant quantities
        total_weight = get_total_weight(self.validators)
        q_OTF = calculate_q_otf(total_weight, self.fault_tolerance_threshold)

        self.calculate_reward_weights(q_OTF)
        self.determine_underestimated_rounds()

        # Calculate OTF and EF statuses
        for tick, round_ in self.rounds_dict.items():
            # Get the list of validators contributing to OTF

            validators_contributing_to_otf = \
                round_.get_level_1_committee(only_in_round_messages=True)

            # validators_contributing_to_ef = round_.get_level_1_committee(only_in_round_messages=False)
            validators_contributing_to_ef = \
                set(self.validators)

            # If a validator contributes to OTF, then it also contributes to EF
            for v in validators_contributing_to_otf:
                validators_contributing_to_ef.add(v)

            if get_total_weight(validators_contributing_to_otf) >= q_OTF:
                round_.set_otf_status(True)
            else:
                round_.set_otf_status(False)

            round_.set_ef_status(get_total_weight(validators_contributing_to_ef))

        total_reward = self.get_total_era_reward()

        total_reward_weight = sum([
            r.reward_weight
            for r in self.rounds_dict.values()
        ])

        # Calculate and distribute rewards
        for tick, round_ in self.rounds_dict.items():
            # If OTF not successful, set rewards to 0
            round_reward = total_reward*round_.reward_weight//total_reward_weight
            if not round_.otf_status:
                otf_reward = 0
                ef_reward = 0
            else:
                otf_reward = round_reward*self.otf_ratio
                allocated_ef_reward = round_reward - otf_reward
                f_ef = (round_.eventual_contributing_weight - q_OTF)**self.ef_reward_delta \
                    //(total_weight - q_OTF)**self.ef_reward_delta
                ef_reward = allocated_ef_reward*f_ef

            round_.set_final_rewards(otf_reward, ef_reward)

            # Distribute OTF rewards
            assigned_weight = round_.get_assigned_weight()
            for v in round_.assigned_validators:
                if v not in round_.punished_validators:
                    v.balance += round_.otf_reward*v.weight//assigned_weight

            # Distribute EF rewards
            for v in self.validators:
                if v not in round_.punished_validators:
                    v.balance += round_.ef_reward*v.weight//total_weight

        # # Tests
        # print('Total balance of validators:', sum([v.balance for v in self.validators]))
        # print('Total minted reward:', total_reward)
        # print('Difference:', total_reward - sum([v.balance for v in self.validators]))

    def init_round_if_not_already(self, tick):
        if tick not in self.rounds_dict.keys():
            tick = self.env.now

            assigned_validators = [v for v in self.validators if tick in v.assigned_ticks]

            self.rounds_dict[tick] = Round(tick, assigned_validators)

    def get_total_era_reward(self) -> uint64:
        return self.initial_supply*self.seigniorage_rate

    def output_result(self):
        result = ''
        for i, v in enumerate(self.validators):
            result += 'Validator %d has earned %d tokens\n'%(i, v.balance)
        return result

    def initialize_simulation(self):
        for v in self.validators:
            v.set_shared_state(self, self.env)


