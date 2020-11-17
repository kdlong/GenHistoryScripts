#!/usr/bin/env python3
from InputTools import UserInput 

parser = UserInput.commonParser()
parser.add_argument("--powheg", action='store_true', help="Is a POWHEG sample")
parser.add_argument("-o", "--outfolder", type=str, default=".", help="Folder to store output (default cwd)")
args = parser.parse_args()

edmFile = args.edmfile if args.edmfile else UserInput.firstFileFromDAS(args.das)
prov = UserInput.edmProv(edmFile, "Pythia8HadronizerFilter")

foundGenerator = False
for line in prov.split("\n"):
    if "Pythia8HadronizerFilter" in line:
        foundGenerator = True
    if foundGenerator:
        print line.strip()

