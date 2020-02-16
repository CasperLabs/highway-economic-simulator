import numpy as np

from highway_economic_simulator import *

np.random.seed(42)

INITIAL_SUPPLY = 1000000000000
# DURATION = TICKS_PER_ERA
DURATION = 1000 * 60 * 60 * 24

v1 = SimpleValidator(100000000000, "A")
v1.set_constant_round_exponent(13)

v2 = SimpleValidator(100000000000, "B")
v2.set_constant_round_exponent(15)

v3 = SimpleValidator(100000000000, "C")
v3.set_constant_round_exponent(15)

state = EraState(INITIAL_SUPPLY)

state.add_validators([v1, v2, v3])

state.run_simulation(DURATION, show_progressbar=True)

print(state.output_result())
