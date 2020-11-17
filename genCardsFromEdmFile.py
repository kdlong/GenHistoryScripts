#!/usr/bin/env python3
from InputTools import UserInput 
import re
import tarfile
import logging
import os
import subprocess

logging.basicConfig(level=logging.INFO)

def getMembers(tar, name, isfile):
    members = []
    for member in tar.getmembers():
        if member.name.startswith(name) and not isfile or member.name == name:
            members.append(member)
    return memberstT

# This works for madgraph if you have lzma support in tarfile, not in CMSSW_10_6
def extractTarPython(gridpack, toRead, outfolder, isfile=True):
    tar = tarfile.open(gridpack, "r:*")
    try:
        tar.extractall(outfolder, getMembers(tar, toRead, isfile))
    except KeyError as e:
        logging.error("Failed to extract the cards from gridpack. Either the " \
            "gridpack is not well formed, or it is not the generator you specified")
    return 0

def extractTarSubprocess(gridpack, toRead, outfolder):
    return subprocess.call(["tar", "xf", gridpack, toRead], cwd=outfolder)

parser = UserInput.commonParser()
parser.add_argument("--powheg", action='store_true', help="Is a POWHEG sample")
parser.add_argument("-o", "--outfolder", type=str, default=".", help="Folder to store output (default cwd)")
args = parser.parse_args()

edmFile = args.edmfile if args.edmfile else UserInput.firstFileFromDAS(args.das)
prov = UserInput.edmProv(edmFile, "ExternalLHEProducer")

gridpack = re.findall("'(/cvmfs.*\.t\\S+)'", str(prov))
if len(gridpack) < 1:
    logging.error("Failed to find gridpack in providence. Either this is malformed, " \
        "or it isn't an EDM file produced from a gridpack")
    exit(1)
gridpack = gridpack[0].rstrip('\\')

logging.info("Extracting cards from gridpack %s" % gridpack)

if not os.path.isdir(args.outfolder):
    os.makedirs(args.outfolder)

members = "powheg.input" if args.powheg else "InputCards"
func = extractTarPython if args.powheg else extractTarSubprocess

val = func(gridpack, members, args.outfolder)

if val == 0:
    logging.info("Extracted input cards to folder %s" % args.outfolder)
