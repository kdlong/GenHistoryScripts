#/usr/bin/env python3
import DataFormats.FWLite as fwlite
from InputTools import UserInput
import argparse

parser = UserInput.commonParser()
args = parser.parse_args()

edmFile = args.edmfile if args.edmfile else UserInput.firstFileFromDAS(args.das)

if "/store" in edmFile[:6]:
    edmFile = "root://cms-xrd-global.cern.ch/"+edmFile

lumis = fwlite.Lumis(edmFile)
handle = fwlite.Handle("GenLumiInfoHeader")
lumis.getByLabel("generator", handle)
genlumi = handle.product()
weightNames = genlumi.weightNames()
print("Length of weight names is", len(weightNames))
for w in weightNames:
    print(w)
