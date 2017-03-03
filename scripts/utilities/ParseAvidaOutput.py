#!/usr/bin/python2
import re

def ParseDetailFile(detail_fpath):
    """
    Given file pointer to detail file, extract information into form below:
    return [{"detail":value, "detail":value, ...}, ...]
    """
    with open(detail_fpath, "r") as detail_fp:
        ######################
        # Step 1) Build Legend
        ###
        # Travel to the legend.
        for line in detail_fp:
            if line == "# Legend:\n": break
        # Consume the legend.
        details = []
        for line in detail_fp:
            if line == "\n": break
            details.append(line.split(":")[-1].strip())
        ######################
        # Step 2) Consume Organisms
        ###
        orgs = []
        for line in detail_fp:
            org_dets = line.strip().split(" ")
            org = {details[i].lower():org_dets[i] for i in range(0, len(org_dets))}
            orgs.append(org)
        return orgs
