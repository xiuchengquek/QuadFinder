from __future__ import unicode_literals

from behave import *
import unittest
import sys

import StringIO
import re
import json
from QuadParser import exons_loop, convertGenomicLoc

from behave import *
__author__ = 'quek'

### Scenario for a list of exon, join them up ###
@given('a list that looks like this')
def step_impl(context):
    exons = context.table
    context.exons = exons

@then('return the following dictionary with transcript info')
def step_impl(context):
    tc = unittest.TestCase('__init__')
    tc.maxDiff = None
    result = exons_loop(context.exons)
    for index, rows in enumerate(context.table):
        mock_info = {k : int(rows[k]) for k in context.table.headings}
        tc.assertDictEqual(mock_info, result[index])


### Scenario : Positive Strand ###
@given('A genome annotation file')
def step_impl(context):
    genome_annotation = json.loads(context.text)
    context.genome_annotation = genome_annotation

@then('the genomic feature at transcript level will be')
def step_impl(context):
    tc = unittest.TestCase('__init__')
    tc.maxDiff = None
    mock_results = json.loads(context.text)
    results = convertGenomicLoc(context.genome_annotation)
    tc.assertDictEqual(mock_results, results)






