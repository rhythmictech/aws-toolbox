#!/usr/bin/env python3

import pprint
import boto3
from string import Template

# setup some generic stuff, boto object, pprint
cf = boto3.resource("cloudformation")
pp = pprint.PrettyPrinter(indent=4)

# takes a parameter name and returns the value

for stack in cf.stacks.all():
    print(stack)
