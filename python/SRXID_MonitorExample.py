#!/usr/bin/env python

from SRXIDTools import *




# Values to caget and write to data file
PV_ValuesToRecord = [
                      PV_GAP_AVG,
                      PV_GAP_US,
                      PV_GAP_DS,
                      PV_POSITION_US_UPPER,
                      PV_POSITION_US_LOWER,
                      PV_POSITION_DS_UPPER,
                      PV_POSITION_DS_LOWER,
                      PV_POSITION_ELEVATION
                    ]


# Forever get your variables
while True:
  print GetVars(PV_ValuesToRecord)
  print GetVars(PV_TEMPERATURES)
  time.sleep(1)
