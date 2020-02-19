# Highway Economic Simulator

This repository implements a Python module for Discrete Event Simulation of
economics of the
[Casperlabs Highway Protocol](https://github.com/casperLabs/highway). It is
possible to simulate various economic aspects of the protocol, such as

- [x] Reward distribution (click [here](https://hackmd.io/@onur/highway_reward_distribution) to see the formulation)
- [ ] Transaction fees
- [ ] Tendency to form oligopolies
- [ ] ...
- [ ] Want or need a feature? [Contact me](mailto:onur@casperlabs.io).

The simulator can be used by validators to project rewards and test out different scenarios.

## Assumptions and simplifications

This module does *NOT* aim to be a full-fledged simulator for the Highway
protocol, and as such abstracts away block proposal, voting and consensus to
simple functions.

*Existing features:*

- Proposal, confirmation and witness messages for every round.
- Message propagation and propagation delay.
- Reward distribution.
- Ticks, rounds and round exponents.
- Ability to add different behavior/rules into validators.
- Validators adjust their new round exponent just before the start of their next round.

*What will NOT be implemented:*

- No blockchain/DAG.
- No forking, equivocations or slashing for equivocations.
- No censorship---validators justify and vote for every message that they receive.
- No network topology.

TODO:

- [ ] More detailed and realistic calculation of the sizes of `PROP`, `CONF` and `WIT` messages.
- [ ] Make propagation delay more realistic by basing it on the actual network protocol.
- [x] Implement round exponent adjustment based on finalization.
- [ ] Generate PDF reports of simulations.

## Installing

Install the package in development mode

```
sudo python setup.py develop
```

The Python module `highway_economic_simulator` will be installed. Moreover,
modifications to the source will not require a reinstall, since the module is
installed in development mode.

## Running examples

Examples are found in the `examples/` directory and can be run directly.

```
cd examples/
python three_validators.py
```
