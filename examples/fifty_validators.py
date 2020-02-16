import numpy as np

from highway_economic_simulator import *

np.random.seed(42)

INITIAL_SUPPLY = 1000000000000
# DURATION = TICKS_PER_ERA
DURATION = 1000 * 60 * 60

N_VALIDATORS = 50
ROUND_EXPONENT = 15
# A simple setup of 2 fast 1 slow validators with equal weight

validators = []

for i in range(N_VALIDATORS):
    v = SimpleValidator(100000000000, "V%d" % i)
    v.set_constant_round_exponent(ROUND_EXPONENT)
    validators.append(v)

state = EraState(INITIAL_SUPPLY)

state.add_validators(validators)

state.run_simulation(DURATION, show_progressbar=True)

# for tick, round_ in state.rounds_dict.items():
#     pct = get_total_weight(round_.get_level_1_committee()) \
#         / get_total_weight(round_.assigned_validators)

#     print(tick, pct)

print(state.output_result())
