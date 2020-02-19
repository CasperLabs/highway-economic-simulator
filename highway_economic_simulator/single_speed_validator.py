from .validator_base import ValidatorBase


class SingleSpeedValidator(ValidatorBase):
    def set_constant_round_exponent(self, re):
        # To be called before the simulation starts
        if self.env:
            assert self.env.now == 0

        self.constant_round_exponent = re

    def determine_new_round_exponent(self):
        return self.constant_round_exponent

    def get_prop_msg_size(self):
        return 15000 * 8  # bits
