from DataFormats.FWLite import Handle, Events, Runs
import os
import logging

def readHeader(edm_file_name, tag):
    if "/store/" in edm_file_name[:7]:
        edm_file_name = "/".join(["root://cms-xrd-global.cern.ch/",
            edm_file_name])
    elif not os.path.isfile(edm_file_name):
        raise FileNotFoundException("File %s was not found." % edm_file_name)

    full_header = not tag

    runs = Runs(edm_file_name)
    runInfoHandle = Handle("LHERunInfoProduct")
    lheLabel = getLHEInfoTag(runs, runInfoHandle)
    run = runs.__iter__().next()
    run.getByLabel(lheLabel, runInfoHandle)
    lheStuff = runInfoHandle.product()
    lines = []
    for i, h in enumerate(lheStuff.headers_begin()):
        if i == lheStuff.headers_size():
            break
        hlines = []
        toStore = False
        for line in h.lines():
            hlines.append(line)
            if tag in line or full_header:
                toStore = True
        if toStore:
            lines.extend(hlines)
            if not full_header:
                break
    return ''.join(lines).rstrip("<")

def getLHEInfoTag(holder, handle):
    check = holder.__iter__().next()
    lheLabel = "externalLHEProducer"
    check.getByLabel(lheLabel, handle)
    try:
        lheStuff = handle.product()
        return lheLabel
    except RuntimeError:
        pass
    try:
        lheLabel = "source"
        check.getByLabel(lheLabel, handle)
        lheStuff = handle.product()
        return lheLabel
    except:
        logging.error("Failed to get LHE info from file. " \
            "Are you sure this file contains LHE weights?")
        raise
