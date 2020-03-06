#Preliminary study of seigniorage sensitivity
#-----------------------------------------------------------
#Alexander Limonov (alimonov@casperlabs.io)
#-----------------------------------------------------------
#03/06/2020 - file created

#Only using aggregate data, but with validators using "canonical" update rule

#INFRASTRUCTURE
import numpy as np
import uuid
from highway_economic_simulator import *

#CONSTANTS
#Sample size
N = 10
#Number of draws
K = 100
#Tokens per validator
STAKED_TOKENS = 100
#Total supply
INITIAL_SUPPLY = 10000

#HELPERS
def define_honest_validator(stake, exponent):
    v = HonestValidator(stake, str(uuid.uuid1()))
    v.set_constant_round_exponent(exponent)

    return v

#Generate a number of lists containing results from draws and create a list of lists of validators
draws = []
validator_lists = []

for i in range(K):
    draws.append([int(round(x)) for x in np.random.triangular(10, 15, 20, size=N)])

for exponent_list in draws:
    validators = [define_honest_validator(STAKED_TOKENS, exponent) for exponent in exponent_list]
    validator_lists.append(validators)

for lst in validator_lists:
    state = EraState(INITIAL_SUPPLY)
    