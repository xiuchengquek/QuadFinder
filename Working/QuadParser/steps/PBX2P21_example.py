from __future__ import unicode_literals

from behave import *
import unittest
import sys

import StringIO
import re
import json
from QuadParser import parseGTF, parseQuadOut, compareTranscriptGenome, writeBedFormat, convertGenomicLoc
from behave import *
__author__ = 'quek'

tc = unittest.TestCase('__init__')
tc.maxDiff = None

@given(u'Feature of Transcript ENST00000293443 on a gtf file')
def step_impl(context):
    with open('mock_files/mock_example.gtf', 'w+') as f:
        f.write(context.text)
    context.mock_gtf = "mock_files/mock_example.gtf"


@given(u'the Transcript Features are')
def step_impl(context):
    with open('mock_files/mock_quad.txt', 'w+') as f:
        f.write(context.text)
    context.mock_quad ='mock_files/mock_quad.txt'

@then(u'the resulting bed file should be')
def step_impl(context):
    gtf_dict = parseGTF(context.mock_gtf)
    gtf_dict = convertGenomicLoc(gtf_dict)
    transcript_dict = parseQuadOut(context.mock_quad)
    mapped_reads = compareTranscriptGenome(gtf_dict, transcript_dict)
    bed_out = writeBedFormat(mapped_reads)
    mock_results = context.text.split('\n')
    mock_results = [x.strip() for x in mock_results]
    tc.assertItemsEqual(mock_results, bed_out)


