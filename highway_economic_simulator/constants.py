from decimal import Decimal

# TICKS_PER_ERA = 604800000 # =1000*60*60*24*7
TICKS_PER_ERA = 10000000
# TICKS_PER_ERA = 100000

# Default values
ERA_SEIGNIORAGE_RATE = Decimal('0.000380892') # 380,892 per era ≈ 2% per annum
# ONE_BILLION = 1000000000 # nine zeroes

FAULT_TOLERANCE_THRESHOLD = Decimal('0.01') # 1%

# Reward weight parameters
REWARD_WEIGHT_ALPHA = Decimal('1') # alpha
REWARD_WEIGHT_BETA = Decimal('0.5') # beta
# REWARD_WEIGHT_BETA = 0 # beta
REWARD_WEIGHT_GAMMA = 1 # gamma

EF_REWARD_DELTA = 1 # delta

UNDERESTIMATION_TOLERANCE = 3 #

OTF_RATIO = Decimal('0.5') # Ratio of OTF rewards to (OTF + EF) rewards

R_0 = Decimal('0.66666')
R_1 = Decimal('0.83333')
