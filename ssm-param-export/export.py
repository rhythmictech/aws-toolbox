#!/usr/bin/env python3

import pprint
import boto3
import json
from string import Template

# setup some generic stuff, boto object, pprint
ssm = boto3.client('ssm')
response = ssm.describe_parameters()
pp = pprint.PrettyPrinter(indent=4)

# takes a parameter name and returns the value

def get_value(name):
    value_response = ssm.get_parameter(Name=name)
    value = value_response['Parameter']['Value']
    return value

# builds a Terraform resource for aws_ssm_parameter
# takes name, type and value inputs

def build_parameter(name, type, value):
    tpl_ssm_param = Template("""
    resource "aws_ssm_parameter" "param_$name" {
        name = "$name"
        description = "$name - Automatically Imported"
        type = "$type"
        value = "$value"
    }
    """)
    print(tpl_ssm_param.substitute({'name':name,'type':type,'value':value}))

paginator = ssm.get_paginator('describe_parameters')

for response in paginator.paginate():
    for r in response['Parameters']:
        p_name = r['Name']
        p_type = r['Type']
        p_value = get_value(p_name)
        build_parameter(p_name, p_type, p_value) 