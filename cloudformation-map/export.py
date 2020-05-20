#!/usr/bin/env python3

import pprint
import boto3
import argparse
from string import Template

# argparse stuff
parser = argparse.ArgumentParser()
parser.add_argument("--region", help="specify an aws region")
args = parser.parse_args()

if args.region:
    # use a different region
    cf = boto3.resource('cloudformation', region_name=args.region)
else:
    # falling back to default region 
    cf = boto3.resource('cloudformation')

# setup some generic stuff, boto object, pprint

pp = pprint.PrettyPrinter(indent=4)

# takes a parameter name and returns the value

for stack in cf.stacks.all():
        print(stack.name)
