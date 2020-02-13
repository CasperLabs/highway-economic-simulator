# Highway Economic Simulator

This repository implements a Python module for Discrete Event Simulation of
economics of the
[Casperlabs Highway Protocol](https://github.com/casperLabs/highway). It is
possible to simulate various economic aspects of the protocol such as

- Reward distribution (added)
- Transaction fees (upcoming)
- Tendency to form oligopolies (upcoming)
- ... ([send feature requests here](mailto:onur@casperlabs.io))

This repository contains code to serve as a mockup for various economic aspects
of Highway, e.g. reward distribution. As such, it can be used by validators to
project rewards and different scenarios.

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

*What will NOT be implemented:*

- No blockchain/DAG.
- No forking, equivocations or slashing for equivocations.
- No censorship---validators justify and vote for every message that they receive.
- No network topology.

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
