from .constants import *
from .validator_base import ValidatorBase

ACCEL_PARAM = 1000
BREAK_PARAM_C0 = 10
BREAK_PARAM_C1 = 40


class HonestValidator(ValidatorBase):
    def set_initial_round_exponent(self, re):
        # To be called before the simulation starts
        if self.env:
            assert self.env.now == 0

        self.round_exponent = re

        self.next_break_target = 0 + BREAK_PARAM_C1 * 2 ** re

    def check_break(self):

        current_tick = self.env.now

        ticks = self.assigned_ticks[-(BREAK_PARAM_C1 + 1) : -1]

        # Round exponents for new rounds are announced on the tick that is
        # right before the new round's beginning: (beginning_tick - 1)
        assert self.assigned_ticks[-1] == current_tick + 1

        relevant_ticks = ticks[-BREAK_PARAM_C1:]
        relevant_rounds = [
            self.era_state.rounds_dict[tick] for tick in reversed(relevant_ticks)
        ]

        fail_counter = 0
        increase_round_exponent = False

        for r in relevant_rounds:
            if current_tick + 1 >= r.get_last_tick():
                store_result = True
            else:
                store_result = False

            if not r.is_otf_successful(self.era_state.q_OTF, store_result=store_result):
                fail_counter += 1
            if fail_counter >= BREAK_PARAM_C0:
                increase_round_exponent = True
                break

        return increase_round_exponent

    def check_accelerate(self):
        next_tick = self.env.now + 1

        return next_tick // 2 ** self.round_exponent % ACCEL_PARAM == 0

    def determine_new_round_exponent(self):
        changed = False
        current_tick = self.env.now
        next_tick = current_tick + 1

        # print(next_tick, self.next_break_target)

        if next_tick >= self.next_break_target:
            increase = self.check_break()
            decrease = self.check_accelerate()

            if increase:
                self.round_exponent += 1
                changed = True

            elif not increase and decrease:
                self.round_exponent -= 1

                changed = True

        if changed:
            new_break_target = next_tick + BREAK_PARAM_C1 * 2 ** self.round_exponent
            self.next_break_target = max(new_break_target, self.next_break_target)
        else:
            new_break_target = next_tick + 2 ** self.round_exponent
            self.next_break_target = max(new_break_target, self.next_break_target)

        return self.round_exponent

    def get_prop_msg_size(self):
        return AVERAGE_PROP_SIZE
