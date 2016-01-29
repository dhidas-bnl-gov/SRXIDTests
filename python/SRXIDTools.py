#!/usr/bin/env python

from cothread.catools import caget, caput
#from epics import caget, caput

import time

# Device and System name
DEV = 'SR:C5-ID:G1'
SYS = 'IVU21:1'

# Amount of tilt allowed for attempted move
CRAB_LIMIT = 0.050

# Girder Tilt limit internal to pmac controller
PV_GIRDER_TILT_LIMIT = DEV + '{' + SYS + '}GIRDER_TILT_LIMIT'

# Serious tilt error readback
PV_GIRDER_TILT_ERROR = DEV + '{' + SYS + ']GIRDER_TILT_ERROR'

# Gap and position readback PVs
PV_GAP_AVG           = DEV + '{' + SYS + '}REAL_GAP_AVG'
PV_GAP_US            = DEV + '{' + SYS + '}REAL_GAP_US'
PV_GAP_DS            = DEV + '{' + SYS + '}REAL_GAP_DS'
PV_POSITION_US_UPPER = DEV + '{' + SYS + '}REAL_POSITION_US_UPPER'
PV_POSITION_US_LOWER = DEV + '{' + SYS + '}REAL_POSITION_US_LOWER'
PV_POSITION_DS_UPPER = DEV + '{' + SYS + '}REAL_POSITION_DS_UPPER'
PV_POSITION_DS_LOWER = DEV + '{' + SYS + '}REAL_POSITION_DS_LOWER'

# elcoder elevation readings
PV_US_ENCODER = DEV + '{' + SYS +'-LEnc:1}Pos'
PV_DS_ENCODER = DEV + '{' + SYS +'-LEnc:6}Pos'

# Elevation PVs
PV_ELEVATION_US  =  DEV + '{' + SYS + '}REAL_ELEVATION_US'
PV_ELEVATION_DS  =  DEV + '{' + SYS + '}REAL_ELEVATION_DS'
PV_ELEVATION_AVG =  DEV + '{' + SYS + '}REAL_ELEVATION_AVG'

# Position setpoint PVs
PV_SETPOINT_US_UPPER  = DEV + '{' + SYS + '-Mtr:6}Inp:Pos'
PV_SETPOINT_US_LOWER  = DEV + '{' + SYS + '-Mtr:8}Inp:Pos'
PV_SETPOINT_DS_UPPER  = DEV + '{' + SYS + '-Mtr:5}Inp:Pos'
PV_SETPOINT_DS_LOWER  = DEV + '{' + SYS + '-Mtr:7}Inp:Pos'
PV_SETPOINT_ELEVATION = DEV + '{' + SYS + '-Mtr:1}Inp:Pos'

# Go PVs
PV_GO_US_UPPER  = DEV + '{' + SYS + '-Mtr:6}Sw:Go'
PV_GO_US_LOWER  = DEV + '{' + SYS + '-Mtr:8}Sw:Go'
PV_GO_DS_UPPER  = DEV + '{' + SYS + '-Mtr:5}Sw:Go'
PV_GO_DS_LOWER  = DEV + '{' + SYS + '-Mtr:7}Sw:Go'
PV_GO_ELEVATION = DEV + '{' + SYS + '-Mtr:1}Sw:Go'

# Is moving PVs
PV_MOVN_US_UPPER  = DEV + '{' + SYS + '-Mtr:3}Pos.MOVN'
PV_MOVN_US_LOWER  = DEV + '{' + SYS + '-Mtr:8}Pos.MOVN'
PV_MOVN_DS_UPPER  = DEV + '{' + SYS + '-Mtr:2}Pos.MOVN'
PV_MOVN_DS_LOWER  = DEV + '{' + SYS + '-Mtr:4}Pos.MOVN'
PV_MOVN_ELEVATION = DEV + '{' + SYS + '-Mtr:1}Pos.MOVN'

# List of temperature PVs
PV_TEMPERATURES = [
  DEV + '{' + SYS + '-Pt:1}T',
  DEV + '{' + SYS + '-Pt:2}T',
  DEV + '{' + SYS + '-Pt:3}T',
  DEV + '{' + SYS + '-Pt:4}T',
  DEV + '{' + SYS + '-Pt:5}T',
  DEV + '{' + SYS + '-Pt:6}T',
  DEV + '{' + SYS + '-Pt:7}T',
  DEV + '{' + SYS + '-Pt:8}T',
  DEV + '{' + SYS + '-Pt:9}T',
  DEV + '{' + SYS + '-Pt:10}T',
  DEV + '{' + SYS + '-Pt:11}T',
  DEV + '{' + SYS + '-Pt:12}T',
  DEV + '{' + SYS + '-Pt:13}T',
  DEV + '{' + SYS + '-Pt:14}T',
  DEV + '{' + SYS + '-Pt:15}T',
  DEV + '{' + SYS + '-Pt:16}T'
]









def MoveDeviceTo (USU, USL, DSU, DSL, ELE):
  """Move the device to the specified location for all points.
     We will crab our way there if needed minding the PV_GIRDER_TILT_LIMIT and CRAB_LIMIT.
     I use USE and not DSE because it is just along for the ride (no feedback)"""

  # Grab current positions.  Variables to be used in calculation.
  This_USU = caget(PV_POSITION_US_UPPER)
  This_USL = caget(PV_POSITION_US_LOWER)
  This_DSU = caget(PV_POSITION_DS_UPPER)
  This_DSL = caget(PV_POSITION_DS_LOWER)
  This_USE = caget(PV_ELEVATION_US)

  # Did we finish the crab walk calculation for each axis?
  Finished = [0, 0, 0, 0]

  # Calculate the moves using a max crab
  while sum(Finished) != 4:
    if not Finished[0]:
      if abs(This_DSU - This_USU) < CRAB_LIMIT:
        This_USU = USU
        Finished[0] = 1
      else:
        if USU > Starting_USU:
          This_USU = This_DSU + CRAB_LIMIT
        else:
          This_USU = This_DSU - CRAB_LIMIT
      Moves.append(['USU', This_USU])

    if not Finished[1]:
      if abs(This_DSU - This_USU) < CRAB_LIMIT:
        This_DSU = DSU
        Finished[1] = 1
      else:
        if DSU > Starting_DSU:
          This_DSU = This_USU + CRAB_LIMIT
        else:
          This_DSU = This_USU - CRAB_LIMIT
      Moves.append(['DSU', This_DSU])

    if not Finished[2]:
      if abs(This_DSL - This_USL) < CRAB_LIMIT:
        This_USL = USL
        Finished[2] = 1
      else:
        if USL > Starting_USL:
          This_USL = This_DSL + CRAB_LIMIT
        else:
          This_USL = This_DSL - CRAB_LIMIT
      Moves.append(['USL', This_USL])

    if not Finished[3]:
      if abs(This_DSL - This_USL) < CRAB_LIMIT:
        This_DSL = DSL
        Finished[3] = 1
      else:
        if DSL > Starting_DSL:
          This_DSL = This_USL + CRAB_LIMIT
        else:
          This_DSL = This_USL - CRAB_LIMIT
      Moves.append(['DSL', This_DSL])


      if Finished[0] == 0 and Finished[1] == 1:
        Moves.append(['USU', USU])
        Finished[0] = 1
      if Finished[0] == 1 and Finished[1] == 0:
        Moves.append(['DSU', DSU])
        Finished[1] = 1
      if Finished[2] == 0 and Finished[3] == 1:
        Moves.append(['USL', USL])
        Finished[2] = 1
      if Finished[2] == 1 and Finished[3] == 0:
        Moves.append(['DSL', DSL])
        Finished[3] = 1

  # Don't forget about elevation
  if abs(ELE - ThisUSE) > 0.010:
    Moves.append(['ELE', ELE])
  print Moves


  return








def MoveDeviceTo (Moves):
  """Move any axes to specific locations in a specific order.
     The input is a list of pairs which are 'moves'.  Each pair is a list containing
     the axis and the absolute position to move to.  The axis labels are as follows:
       USU - Upstream Upper
       USL - Upstream Lower
       DSU - Downstream Upper
       DSL - Downstream Lower
       ELE - Elevation

     The list is processed in order.  Be aware that there is a girder tilt limit.  It is
     unchecked here.  Please do not hit the limit.
     """


  # Loop over each move command
  for move in Moves:

    # Which axis and position
    axis     = move[0]
    position = move[1]


    # Select which axis and put position and go variables.  There is extra sleep due to vendor misuse
    # of motor records.  Sorry about that.
    if axis == 'USU':
      caput(PV_SETPOINT_US_UPPER, position, wait=True)
      caput(PV_GO_US_UPPER, 1, timeout=100, wait=True)
      time.sleep(2)

      while (caget(PV_MOVN_US_UPPER) == 1):
        time.sleep(1)
      time.sleep(5)

    elif axis == 'USL':
      caput(PV_SETPOINT_US_LOWER, position, wait=True)
      caput(PV_GO_US_LOWER, 1, timeout=100, wait=True)
      time.sleep(2)

      while (caget(PV_MOVN_US_LOWER) == 1):
        time.sleep(1)
      time.sleep(5)

    elif axis == 'DSU':
      caput(PV_SETPOINT_DS_UPPER, position, wait=True)
      caput(PV_GO_DS_UPPER, 1, timeout=100, wait=True)
      time.sleep(2)

      while (caget(PV_MOVN_DS_UPPER) == 1):
        time.sleep(1)
      time.sleep(5)

    elif axis == 'DSL':
      caput(PV_SETPOINT_DS_LOWER, position, wait=True)
      caput(PV_GO_DS_LOWER, 1, timeout=100, wait=True)
      time.sleep(2)

      while (caget(PV_MOVN_DS_LOWER) == 1):
        time.sleep(1)
      time.sleep(5)

    elif axis == 'ELE':
      caput(PV_SETPOINT_ELEVATION, position, wait=True)
      caput(PV_GO_ELEVATION, 1, timeout=100, wait=True)
      time.sleep(2)

      while (caget(PV_MOVN_ELEVATION) == 1):
        time.sleep(1)
      time.sleep(5)

    else:
      print 'ERROR: I do not understand this move command:', move

  return








def MoveDeviceIncremental (Moves):
  """Move any axes a specified distance in a specific order.
     The input is a list of pairs which are 'moves'.  Each pair is a list containing
     the axis and the relative distance to move.  The axis labels are as follows:
       USU - Upstream Upper
       USL - Upstream Lower
       DSU - Downstream Upper
       DSL - Downstream Lower
       ELE - Elevation

     The list is processed in order.  Be aware that there is a girder tilt limit.  It is
     unchecked here.  Please do not hit the limit.
     """

  for move in Moves:
    axis     = move[0]
    distance = move[1]

    Position = 0

    # Get the correct position for the given axis
    if axis == 'USU':
      Position = caget(PV_POSITION_US_UPPER)
      Position += distance

    elif axis == 'USL':
      Position = caget(PV_POSITION_US_LOWER)
      Position += distance

    elif axis == 'DSU':
      Position = caget(PV_POSITION_DS_UPPER)
      Position += distance

    elif axis == 'DSL':
      Position = caget(PV_POSITION_DS_LOWER)
      Position += distance

    elif axis == 'ELE':
      Position = caget(PV_POSITION_ELEVATION)
      Position += distance

    else:
      print 'ERROR: I do not understand this move command:', move
      return


    # Do the move with the newly computed position
    MoveDeviceTo( [[axis, Position]] )

  return









def GetVars (Vars):
  """caget a list of cariables and return a list of results"""

  Vals = []
  for pv in Vars:
    Vals.append(caget(pv))
  return Vals





