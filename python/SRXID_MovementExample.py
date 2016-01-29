#!/usr/bin/env python

from SRXIDTools import *


MoveDeviceTo(10.000, 10.000, 10.000, 10.000, 0.127)
MoveDeviceTo(10.120, 10.120, 10.120, 10.120, None)

AddToTaper(0.04)
AddToTilt(0.02)

SetTaper(0.010)
SetTilt(0.010)

SetTaper(0.000)
SetTilt(0.000)

# Move to specified locations
Moves = [ 
          ['USU',  9.990],
          ['USL',  9.990],
          ['DSU',  9.990],
          ['DSL',  9.990],
          ['USU', 20.000],
          ['USL', 20.000],
          ['DSU', 20.000],
          ['DSL', 20.000]
  ]
MoveDeviceSequence(Moves)



# Move incremental amounts
MovesIncremental = [ 
          ['USU', -0.010],
          ['USL', -0.010],
          ['DSU', -0.010],
          ['DSL', -0.010],
          ['USU',  0.010],
          ['USL',  0.010],
          ['DSU',  0.010],
          ['DSL',  0.010]
  ]
MoveDeviceIncremental(MovesIncremental)

