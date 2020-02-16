# from __future__ import annotations
import simpy
import progressbar

from typing import List, Dict
from numpy import uint8, uint16, uint32, uint64
from collections import OrderedDict
from math import ceil
from .helper import get_total_weight, calculate_q_otf, get_round_beginning_ticks
from .round import Round
from .constants import *


class EraState:
    validators: List["ValidatorBase"]
    latest_tick: uint64
    initial_supply: uint64
    rounds_dict: Dict[uint64, Round]

    def __init__(
        self,
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
        self.env = simpy.Environment()
        self.validators = []
        self.rounds_dict = OrderedDict()
        self.initial_supply = initial_supply

        self.fault_tolerance_threshold = FAULT_TOLERANCE_THRESHOLD
        self.seigniorage_rate = ERA_SEIGNIORAGE_RATE
        self.reward_weight_alpha = REWARD_WEIGHT_ALPHA
        self.reward_weight_beta = REWARD_WEIGHT_BETA
        self.reward_weight_gamma = REWARD_WEIGHT_GAMMA
        self.ef_reward_delta = EF_REWARD_DELTA
        self.underestimation_tolerance = UNDERESTIMATION_TOLERANCE
        self.otf_ratio = OTF_RATIO

        self.latest_tick = 0

        self.total_minted_reward = 0

    def add_validator(self, validator: "ValidatorBase"):
        self.validators.append(validator)

    def add_validators(self, validators: List["ValidatorBase"]):
        for v in validators:
            self.add_validator(v)

    def calculate_reward_weights(self, q_OTF: uint64):
        # Calculate reward weight for each block/round
        for tick, round_ in self.rounds_dict.items():
            assigned_weight = round_.get_assigned_weight()
            if assigned_weight >= q_OTF:
                reward_weight = (
                    self.reward_weight_alpha * assigned_weight
                    + (1 - self.reward_weight_alpha) * self.reward_weight_beta
                    - self.reward_weight_beta * q_OTF
                ) ** self.reward_weight_gamma
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

        finished_rounds = OrderedDict()
        for tick, round_ in self.rounds_dict.items():
            if round_.get_last_tick() < self.duration:
                finished_rounds[tick] = round_

        # Calculate OTF and EF statuses
        for tick, round_ in finished_rounds.items():
            # Get the list of validators contributing to OTF

            validators_contributing_to_otf = round_.get_level_1_committee(
                only_in_round_messages=True
            )

            # validators_contributing_to_ef = round_.get_level_1_committee(only_in_round_messages=False)
            validators_contributing_to_ef = set(self.validators)

            # If a validator contributes to OTF, then it also contributes to EF
            for v in validators_contributing_to_otf:
                validators_contributing_to_ef.add(v)

            if get_total_weight(validators_contributing_to_otf) >= q_OTF:
                round_.set_otf_status(True)
            else:
                round_.set_otf_status(False)

            round_.set_ef_status(get_total_weight(validators_contributing_to_ef))

        total_reward = self.get_total_era_reward()
        self.total_minted_reward += total_reward

        total_reward_weight = sum([r.reward_weight for r in finished_rounds.values()])

        # Calculate and distribute rewards
        for tick, round_ in finished_rounds.items():
            # If OTF not successful, set rewards to 0
            round_reward = total_reward * round_.reward_weight / total_reward_weight
            if not round_.otf_status:
                otf_reward = 0
                ef_reward = 0
            else:
                otf_reward = round_reward * self.otf_ratio
                allocated_ef_reward = round_reward - otf_reward
                f_ef = (
                    (round_.eventual_contributing_weight - q_OTF)
                    ** self.ef_reward_delta
                    / (total_weight - q_OTF) ** self.ef_reward_delta
                )
                ef_reward = allocated_ef_reward * f_ef

            round_.set_final_rewards(otf_reward, ef_reward)

            # Distribute OTF rewards
            assigned_weight = round_.get_assigned_weight()
            for v in round_.assigned_validators:
                if v not in round_.punished_validators:
                    v.send_reward(round_.otf_reward * v.weight / assigned_weight)

            # Distribute EF rewards
            for v in self.validators:
                if v not in round_.punished_validators:
                    v.send_reward(round_.ef_reward * v.weight / total_weight)

    def init_round_if_not_already(self, tick):
        if tick not in self.rounds_dict.keys():
            tick = self.env.now

            assigned_validators = [
                v for v in self.validators if tick in v.assigned_ticks
            ]

            self.rounds_dict[tick] = Round(tick, assigned_validators)

    def get_total_era_reward(self) -> uint64:
        return self.initial_supply * (
            (1 + self.seigniorage_rate) ** (self.duration / TICKS_PER_ERA) - 1
        )

    def output_result(self):
        total_distributed_reward = sum([v.reward_balance for v in self.validators])
        # annual_seigniorage_rate = (1+self.seigniorage_rate)**(TICKS_PER_YEAR/TICKS_PER_ERA)-1
        annual_seigniorage_rate = (
            (self.initial_supply + self.total_minted_reward) / self.initial_supply
        ) ** (TICKS_PER_YEAR / self.duration) - 1
        annual_seigniorage_rate_after_burning = (
            (self.initial_supply + total_distributed_reward) / self.initial_supply
        ) ** (TICKS_PER_YEAR / self.duration) - 1

        result = ""
        result += "Number of validators: %d\n" % (len(self.validators))
        result += "Simulated time: %.3g hours\n" % (self.duration / (1000 * 60 * 60))
        result += "Number of rounds: %d\n" % (len(self.rounds_dict))
        result += "Average round length: %.3g seconds\n" % (
            self.duration / 1000 / len(self.rounds_dict)
        )
        result += "Initial token supply: %d\n" % (self.initial_supply)
        result += "Total minted reward: %d\n" % (self.total_minted_reward)
        result += "Total distributed reward: %d\n" % (total_distributed_reward)
        result += "Total burned reward: %d\n" % (
            self.total_minted_reward - total_distributed_reward
        )
        result += "Projected annual seigniorage rate: %.2g%%\n" % (
            annual_seigniorage_rate * 100
        )
        result += "Net pr. a. seigniorage rate considering burning: %.2g%%\n" % (
            annual_seigniorage_rate_after_burning * 100
        )

        for i, v in enumerate(self.validators):
            result += "%s has earned %d tokens" % (v.name, v.reward_balance)
            if i < len(self.validators) - 1:
                result += "\n"

        return result

    def run_simulation(self, duration, show_progressbar=False):
        if duration > TICKS_PER_ERA:
            raise Exception(
                "Simulating for durations longer than one era is not supported yet"
            )

        for v in self.validators:
            v.set_shared_state(self, self.env)

        self.duration = duration

        if show_progressbar:
            self.bar = progressbar.ProgressBar(max_value=duration)
            self.update_frequency = int(duration / 1000)

            action = self.env.process(self.update_progressbar())

        # Start running the simulation
        self.env.run(until=duration)

        # At the end, distribute the rewards
        self.distribute_rewards()

    def update_progressbar(self):
        while True:
            if self.duration - self.env.now <= self.update_frequency:
                self.bar.finish()
                break

            yield self.env.timeout(self.update_frequency)
            self.bar.update(self.env.now)
