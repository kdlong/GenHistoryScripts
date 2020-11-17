#/usr/bin/env python3
from InputTools import lheTools,UserInput

parser = UserInput.commonParser()
args = parser.parse_args()

edmFile = args.edmfile if args.edmfile else UserInput.firstFileFromDAS(args.das)
if "NANOAOD" in args.edmFile:
    logging.error("LHE header is not stored in NanoAOD files. Exiting")
    exit(1)

header = lheTools.readHeader(edmFile, "")

print(header)
