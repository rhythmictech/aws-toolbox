#!/usr/bin/env python3

import boto3
import json

client = boto3.client('config')

# Before deleting the rule, ensure to delete remediation action associated with the rule. 
# Deleting the rule removes the rule and its evaluation results. The deletion might take several minutes.

page = client.get_paginator('describe_config_rules')
for response in page.paginate():
    for r in response['ConfigRules']:
        arn = r['ConfigRuleArn'] # may need this one later
        try:
            createdBy = r['CreatedBy']
            pass
        except:
            print(r['ConfigRuleName'])
            # now lets fetch remediation_configurations
            CRN = [r['ConfigRuleName']]
            remediations = client.describe_remediation_configurations(ConfigRuleNames=CRN)
            print(remediations)
