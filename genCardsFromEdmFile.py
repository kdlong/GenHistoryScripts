from InputTools import UserInput 
import re
import tarfile
import logging
import os

logging.basicConfig(level=logging.INFO)

def getMembers(tar, name, isdir):
    members = []
    for member in tar.getmembers():
        if member.name.startswith(name) and isdir or member.name == name:
            members.append(member)
    return members


parser = UserInput.commonParser()
parser.add_argument("--powheg", action='store_true', help="Is a POWHEG sample")
parser.add_argument("-o", "--outfolder", type=str, default=".", help="Folder to store output (default cwd)")
args = parser.parse_args()

edmFile = args.edmfile if args.edmfile else UserInput.firstFileFromDAS(args.das)
prov = UserInput.edmProv(edmFile, "ExternalLHEProducer")

gridpack = re.findall("'(/cvmfs.*\.t\\S+)'", prov)
if len(gridpack) < 1:
    logging.error("Failed to find gridpack in providence. Either this is malformed, " \
        "or it isn't an EDM file produced from a gridpack")
    exit(1)
gridpack = gridpack[0]

logging.info("Extracting cards from gridpack %s" % gridpack)
tar = tarfile.open(gridpack)

members = "InputCards" if not args.powheg else "powheg.input"

if not os.path.isdir(args.outfolder):
    os.makedirs(args.outfolder)

try:
    tar.extractall(args.outfolder, getMembers(tar, members, args.powheg))
except KeyError as e:
    logging.error("Failed to extract the cards from gridpack. Either the " \
        "gridpack is not well formed, or it is not the generator you specified")

logging.info("Extracted input cards to folder %s" % args.outfolder)

