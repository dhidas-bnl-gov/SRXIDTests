#!/usr/bin/env python

from cothread.catools import caget, caput
#from epics import caget, caput

import time

# Device and System name
DEV = 'SR:C5-ID:G1'
SYS = 'IVU21:1'

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





def MoveDeviceTo (Moves):
  """Move any axes to specific locations in a specific order."""

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
  """Move any axis a specified distance."""

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
    MoveDeviceTo( [axis, Position] )

  return









def GetVars (Vars):
  Vals = []
  for pv in Vars:
    Vals.append(caget(pv))
  return Vals





