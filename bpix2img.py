#! /usr/bin/env python

import pycrates as cr
import numpy as np
import sys

if len(sys.argv) != 3:
    print("Usage: bpix2img.py infile outfile\n")
    sys.exit(1)

infile=sys.argv[1]
outfile=sys.argv[2]

#
# Load Data
#
bpix = cr.read_file(infile)
xx =  cr.copy_colvals( bpix, "chipx")
yy =  cr.copy_colvals( bpix, "chipy")
stt = cr.copy_colvals( bpix, "status")
#tt  = cr.copy_colvals( bpix, "time_stop")

#
# Turn array of status bytes into long integer
#


twos = 2**np.arange(32)[::-1]
gg = [ np.sum(twos*ii) for ii in stt ]


#gg=[ (ii[0]*256l*256*256)+(ii[1]*256l*256)+(ii[2]*256)+ii[3] for ii in stt ]
#gg=tt

#
# chip coords go 1:1024 so add extra row/column so don't have to -1
# everywhere.
#
msk = np.zeros((1025,1025), np.int32)
for ii in range( len(xx) ):
    for x in range( xx[ii][0], xx[ii][1]+1 ):
        for y in range( yy[ii][0], yy[ii][1]+1):
            msk[y,x]=gg[ii]

#
# remove extra row/column and correct orientation, add extra bogus dim
#
#msk=msk[1:,1:]
#msk=msk.reshape(1,1024,1024)

#msk=msk[1:,:]
foo=msk[1:,1:]
msk=foo

#
# Write out, always clobbers
#
cd = cr.CrateData()
cd.values =msk
icrt = cr.IMAGECrate()
cr.add_piximg( icrt, cd )


cr.write_file( icrt, outfile, clobber=True )
