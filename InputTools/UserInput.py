import subprocess
import argparse

def commonParser():
    parser = argparse.ArgumentParser()
    inp = parser.add_mutually_exclusive_group(required=True)
    inp.add_argument("-d", "--das", type=str, help="DAS path of sample")
    inp.add_argument("-f", "--edmfile", type=str, help="EDM file")
    return parser

def firstFileFromDAS(path):
    return subprocess.check_output(["/cvmfs/cms.cern.ch/common/dasgoclient", "-query=file dataset=%s" % path, "-limit=1"]).strip()

def edmProv(edmfile, module=None):
    args = ["-e"]
    if module:
        args.extend(["-f", module])
    return subprocess.check_output(["edmProvDump"]+args+[edmfile])
