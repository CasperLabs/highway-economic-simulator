from decimal import Decimal

# TICKS_PER_ERA = 604800000 # =1000*60*60*24*7
TICKS_PER_ERA = 1000000
# TICKS_PER_ERA = 10000

ERA_SEIGNIORAGE_RATE = Decimal('0.000380892') # 380,892 per era ≈ 2% per annum
# ONE_BILLION = 1000000000 # nine zeroes

FAULT_TOLERANCE_THRESHOLD = Decimal('0.01') # 1%

REWARD_WEIGHT_PARAM_1 = Decimal('1') # alpha
REWARD_WEIGHT_PARAM_2 = Decimal('0.5') # beta
# REWARD_WEIGHT_PARAM_2 = 0 # beta
REWARD_WEIGHT_PARAM_3 = 1 # gamma

EF_REWARD_PARAM = 1 # delta

UNDERESTIMATE_PARAM = 3 #

EPSILON = Decimal('0.5') # Ratio of OTF rewards to (OTF + EF) rewards
