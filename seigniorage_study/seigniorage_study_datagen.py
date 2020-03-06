#Preliminary study of seigniorage sensitivity
#-----------------------------------------------------------
#Alexander Limonov (alimonov@casperlabs.io)
#-----------------------------------------------------------
#03/05/2020 - file created

from seigniorage_study.datagen_decorators import *

import numpy as np

from highway_economic_simulator import *

np.random.seed(42)

INITIAL_SUPPLY = 10000
# DURATION = TICKS_PER_ERA
DURATION = 1000 * 60 * 60 * 24

# A simple setup of 2 fast 1 slow validators with equal weight

v1 = HonestValidator(100, "A")
v1.set_constant_round_exponent(15)

v2 = HonestValidator(100, "B")
v2.set_constant_round_exponent(14)

v3 = HonestValidator(100, "C")
v3.set_constant_round_exponent(14)

state = EraState(INITIAL_SUPPLY)

state.add_validators([v1, v2, v3])

state.run_simulation(DURATION, show_progressbar=False)

# for tick, round_ in state.rounds_dict.items():
#     pct = get_total_weight(round_.get_level_1_committee()) \
#         / get_total_weight(round_.assigned_validators)

#     print(tick, pct)

print(state.output_result())
