
from __future__ import unicode_literals

from behave import *
import unittest
import sys

import StringIO
import re
import json

from behave import *

from QuadParser import findBetween, compareTranscriptGenome,writeBedFormat




tc = unittest.TestCase('__init__')
tc.maxDiff = None







@given('Transcript feature')
def step_impl(context):
    transcript_feature = json.loads(context.text)
    context.transcript_feature = transcript_feature

@when('the genome feature is')
def step_impl(context):
    genomic_feature = json.loads(context.text)
    context.genomic_feature = genomic_feature

@then("the genomic feature for the transcript should be")
def step_impl(context):

    results_info =  json.loads(context.text)
    results_dict = compareTranscriptGenome(context.genomic_feature, context.transcript_feature )
    tc.assertDictEqual(results_info, results_dict)
    context.results = results_dict

@then("the bedformat out but unordered")
def step_impl(context):
    mock_results = context.text
    genomic_features = context.results
    bed_out = writeBedFormat(genomic_features)
    mock_results = mock_results.split('\n')
    tc.assertItemsEqual(bed_out, mock_results)






















