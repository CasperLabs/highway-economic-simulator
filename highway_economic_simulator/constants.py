# Constants for the simulation

TICKS_PER_ERA = 604800000 # =1000*60*60*24*7
TICKS_PER_YEAR = 31536000000 # =1000*60*60*24*365

# Default values
ERA_SEIGNIORAGE_RATE = 0.000380892 # 380,892 per era ≈ 2% per annum
# ONE_BILLION = 1000000000 # nine zeroes

FAULT_TOLERANCE_THRESHOLD = 0.01 # 1%

# Reward weight parameters
REWARD_WEIGHT_ALPHA = 1 # alpha
REWARD_WEIGHT_BETA = 0.5 # beta
# REWARD_WEIGHT_BETA = 0 # beta
REWARD_WEIGHT_GAMMA = 1 # gamma

EF_REWARD_DELTA = 1 # delta

# Number of infeasible rounds that trigger punishment in the next feasible round
UNDERESTIMATION_TOLERANCE = 3

OTF_RATIO = 0.5 # Ratio of OTF rewards to (OTF + EF) rewards

R_0 = 0.66666
R_1 = 0.83333

# Sizes of CONF and WIT messages on average
AVERAGE_CONF_SIZE = 2000*8 # bits
AVERAGE_WIT_SIZE = 2000*8 # bits
