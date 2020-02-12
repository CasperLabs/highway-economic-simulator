

PROP_MSG = 0
CONF_MSG = 1
WIT_MSG = 2

class Message:
    def __init__(self, sender, size, type_, tick, round_):
        self.sender = sender
        self.size = size
        self.tick = tick
        self.round_ = round_
        self.type_ = type_

        self.received_validators = []
        self.justified_messages = []

        for m in self.round_.messages:
            # print(tick, m.received_validators)
            if sender is not m.sender and sender in m.received_validators:
                self.justified_messages.append(m)

        # print(self.justified_messages)

    def _deliver_to_validator(self, env, validator):
        yield env.timeout(2)
        self.received_validators.append(validator)

    def propagate(self, env):
        for v in self.round_.assigned_validators:
            if v is self.sender:
                continue
            else:
                action = env.process(self._deliver_to_validator(env, v))

    def __repr__(self):
        result = 'Msg('+str(self.sender)+', '
        result += str(self.size)+', '
        if self.type_ is PROP_MSG:
            result += 'PROP'
        elif self.type_ is CONF_MSG:
            result += 'CONF'
        elif self.type_ is WIT_MSG:
            result += 'WIT'
        result += ', '
        result += str(self.tick)
        result += ')'

        return result
