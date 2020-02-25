# from __future__ import annotations
from typing import List, Dict
from numpy import uint64

from .constants import *


def get_total_weight(validators: List["Validator"]) -> uint64:
    return sum([v.weight for v in validators])


def get_round_beginning_ticks(effective_round_exponents: List[uint64]) -> List[uint64]:
    result = []
    current_tick = 0
    while True:
        result.append(current_tick)
        current_round_exponent = effective_round_exponents[current_tick]
        if current_tick + 2 ** current_round_exponent < len(effective_round_exponents):
            next_tick = current_tick + 2 ** current_round_exponent
        else:
            break
        current_tick = next_tick
    return result


def calculate_q_otf(
    total_weight: uint64, fault_tolerance_threshold: uint64, ack_level: uint64 = 1
) -> uint64:
    """
    total_weight: Total weight of all validators in motes
    fault_tolerance_threshold: An integer value such that its division by
        1 billion gives the fault tolerance threshold as a ratio over unity.
        Example: For 1% FTT, you would give int(0.01*1e9)
    ack_level: Acknowledgement level
    """
    return total_weight // 2 + total_weight * fault_tolerance_threshold * (
        2 ** (ack_level - 1)
    ) // (2 ** ack_level - 1)


# def get_effective_round_exponents(announced_round_exponents: List[uint64])->List[uint64]:
#     result = []
#     current_tick = 0
#     while True:
#         current_round_exponent = announced_round_exponents[current_tick]
#         if current_tick+2**current_round_exponent < len(announced_round_exponents):
#             result.extend([current_round_exponent]*(2**current_round_exponent))
#         else:
#             remaining_n_ticks = len(announced_round_exponents)-current_tick
#             result.extend([current_round_exponent]*remaining_n_ticks)
#             break
#         current_tick += 2**current_round_exponent
#     return result
