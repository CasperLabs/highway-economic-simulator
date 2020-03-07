#Preliminary study of seigniorage sensitivity
#-----------------------------------------------------------
#Alexander Limonov (alimonov@casperlabs.io)
#-----------------------------------------------------------
#03/06/2020 - file created, implemented basic data generation for era-level datasets

#INFRASTRUCTURE
import numpy as np
import pandas as pd
import uuid
from highway_economic_simulator import *

#Let's make sure printing data actually shows us the data
pd.set_option('display.expand_frame_repr', False)

#CONSTANTS
#Sample size
N = 10
#Number of draws
K = 100
#Tokens per validator
STAKED_TOKENS = 100
#Total supply
INITIAL_SUPPLY = 10000
#Duration in "ticks"
DURATION = 1000 * 60 * 60 * 24

#HELPERS
def define_honest_validator(stake, exponent):
    v = HonestValidator(stake, str(uuid.uuid1()))
    v.set_constant_round_exponent(exponent)

    return v

def average_absolute_deviation(lst):
    avg = np.average(lst)
    
    return sum([abs(x - avg)/len(lst) for x in lst])

#Generate a number of lists containing results from draws and create a list of lists of validators
draws = []
validator_lists = []

#Collection of random draws from the exponent distribution
for i in range(K):
    draws.append([int(round(x)) for x in np.random.triangular(10, 15, 20, size=N)])

#A list of lists of validators instantiated from the randomly drawn exponents
for exponent_list in draws:
    validators = [define_honest_validator(STAKED_TOKENS, exponent) for exponent in exponent_list]
    validator_lists.append(validators)

#Creating an era-level dataset
columns = ['number_of_rounds', 'initial_supply', 'average_round_length', 'average_round_exponent', 'total_minted_reward', 'total_distributed_reward', 'annual_seigniorage_rate_after_burning', 'exponent_variance', 'exponent_absolute_deviation']
data = []

for lst in validator_lists:
    exps = [v.constant_round_exponent for v in lst]
    variance = np.var(exps)
    mean_deviation = average_absolute_deviation(exps)

    state = EraState(INITIAL_SUPPLY)
    state.add_validators(lst)
    state.run_simulation(DURATION, show_progressbar = False)
    
    number_of_rounds = len(state.rounds_dict)
    initial_supply = INITIAL_SUPPLY
    average_round_length = state.duration / 1000 / len(state.rounds_dict)
    average_round_exponent = log(state.duration / len(state.rounds_dict), 2)
    total_distributed_reward = sum([v.reward_balance for v in state.validators])
    annual_seigniorage_rate_after_burning = (
            (state.initial_supply + total_distributed_reward) / state.initial_supply
        ) ** (TICKS_PER_YEAR / state.duration) - 1

    new_data = [number_of_rounds, initial_supply, average_round_length, average_round_exponent, state.total_minted_reward, total_distributed_reward, annual_seigniorage_rate_after_burning, variance, mean_deviation]

    data.append(new_data)

era_df = pd.DataFrame(data, None, columns)
    
 