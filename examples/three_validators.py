import numpy as np

from highway_economic_simulator import *

np.random.seed(42)

INITIAL_SUPPLY = 1000000000000
# DURATION = TICKS_PER_ERA
DURATION = 1000 * 60 * 60 * 24 * 3
INITIAL_ROUND_EXPONENT = 15

# A simple setup of 2 fast 1 slow validators with equal weight

v1 = HonestValidator(100000000000, "A")
v1.set_initial_round_exponent(INITIAL_ROUND_EXPONENT)

v2 = HonestValidator(100000000000, "B")
v2.set_initial_round_exponent(INITIAL_ROUND_EXPONENT)

v3 = HonestValidator(100000000000, "C")
v3.set_initial_round_exponent(INITIAL_ROUND_EXPONENT)

state = EraState(INITIAL_SUPPLY)

state.add_validators([v1, v2, v3])

state.run_simulation(DURATION, show_progressbar=True)

# for tick, round_ in state.rounds_dict.items():
#     pct = get_total_weight(round_.get_level_1_committee()) \
#         / get_total_weight(round_.assigned_validators)

#     print(tick, pct)

print(state.output_result())
