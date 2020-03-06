#Decorator functionality for output code injection
#-----------------------------------------------------------
#Alexander Limonov (alimonov@casperlabs.io)
#-----------------------------------------------------------
#03/05/2020 - file created

#ENVIRONMENT SETUP
#Types
import highway_economic_simulator as hec
#Data manipulation and output
import pandas as pd

#Basic proof of concept - run simulation, then print out round data
def basic_decorator(self: hec.EraState, DURATION):
    self.run_simulation(DURATION, show_progressbar=False)
    for r in self.rounds_dict:
        print(self.rounds_dict[r].beginning_tick)