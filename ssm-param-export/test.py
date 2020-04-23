#!/usr/bin/env python3

import argparse

# argparse setup
parser = argparse.ArgumentParser()
parser.add_argument("--region", help="specify region in which to run, otherwise \
    defaulting to whatever is specified by Okta")
args = parser.parse_args()
if args.region:
    print("region specified")
else:
    print("default region")