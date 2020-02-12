import simpy
import progressbar
import numpy as np

from highway_economic_simulator import *

np.random.seed(42)

INITIAL_SUPPLY = 1000000000000

env = simpy.Environment()

# A simple setup of 2 fast 1 slow validators with equal weight

v1 = SimpleValidator(100000000000, "A")
v1.set_constant_round_exponent(15)

v2 = SimpleValidator(100000000000, "B")
v2.set_constant_round_exponent(14)

v3 = SimpleValidator(100000000000, "C")
v3.set_constant_round_exponent(14)


state = EraState(env, INITIAL_SUPPLY)

state.add_validators([v1, v2, v3])
state.initialize_simulation()

env.run(until=TICKS_PER_ERA)

# bar = progressbar.ProgressBar(max_value=TICKS_PER_ERA)
# for tick in range(TICKS_PER_ERA):
#     state.next_tick()
#     bar.update(tick)

# state.distribute_rewards()
# print(state.output_result())

# state.rounds_dict[0].get_level_1_committee()
for tick, round_ in state.rounds_dict.items():
    pct = get_total_weight(round_.get_level_1_committee()) \
        / get_total_weight(round_.assigned_validators)
    print(tick, pct)

# import ipdb; ipdb.set_trace()
