
from __future__ import unicode_literals

from behave import *
import unittest
import sys

import StringIO
import re
import json

from behave import *

from QuadParser import remap





@given('Genomic location of transcript')
def step_impl(context):
    genome_info  = context.table
    context.genome_info = genome_info

@when('the transcript feature is 0 based')
def step_impl(context):
    transcript_info = context.table
    context.transcript_info = transcript_info

@then('Transcript will have a genomic start and end of')
def step_impl(context):
    tc = unittest.TestCase('__init__')
    tc.maxDiff = None

    for index, rows in enumerate(context.table):
        mock_info = { 'start' : int(rows['start']),
                      'end'   : int(rows['end'])
        }
        feature_info = remap(context.genome_info[index],
                             context.transcript_info[0])

        tc.assertDictEqual(mock_info, feature_info)
