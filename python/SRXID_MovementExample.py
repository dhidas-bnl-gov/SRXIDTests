#!/usr/bin/env python

from SRXIDTools import *



# Move to specified location
Moves = [ 
          ['USU', 19.990],
          ['USL', 19.990],
          ['DSU', 19.990],
          ['DSL', 19.990],
          ['USU', 20.000],
          ['USL', 20.000],
          ['DSU', 20.000],
          ['DSL', 20.000]
  ]
MoveDeviceTo(Moves)



# Move incremental amount
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

