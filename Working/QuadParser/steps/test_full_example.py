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

@given('a Gencode file  "{mock_gtf}" which has 1 based coordinates')
def step_impl(context, mock_gtf):
    with open(mock_gtf, 'w+') as f:
        f.write(context.text)
    context.mock_gtf = mock_gtf

@given('a QuadParser file "{mock_quad}" which has 0 based coordaintes')
def step_impl(context, mock_quad):
    with open(mock_quad, 'w+') as f:
        f.write(context.text)
    context.mock_quad = mock_quad

@then('the output of will be a bed file that is 0 base')
def step_impl(context):
    gtf_dict = parseGTF(context.mock_gtf)
    print >> sys.stdout, gtf_dict

    gtf_dict = convertGenomicLoc(gtf_dict)
    transcript_dict = parseQuadOut(context.mock_quad)
    mapped_reads = compareTranscriptGenome(gtf_dict, transcript_dict)
    bed_out = writeBedFormat(mapped_reads)
    mock_results = context.text.split('\n')
    mock_results = [x.strip() for x in mock_results]
    tc.assertItemsEqual(mock_results, bed_out)


@given('The same Gencode file  "{mock_gtf}" which has 1 based coordinates')
def step_impl(context, mock_gtf):
    with open(mock_gtf, 'w+') as f:
        f.write(context.text)
    context.mock_gtf = mock_gtf

@given('a Different QuadParser file "{mock_quad}" which has 0 based coordaintes')
def step_impl(context, mock_quad):
    with open(mock_quad, 'w+') as f:
        f.write(context.text)

    context.mock_quad = mock_quad

@then('there will no results')
def step_impl(context):
    gtf_dict = parseGTF(context.mock_gtf)
    gtf_dict = convertGenomicLoc(gtf_dict)
    transcript_dict = parseQuadOut(context.mock_quad)
    mapped_reads = compareTranscriptGenome(gtf_dict, transcript_dict)
    bed_out = writeBedFormat(mapped_reads)
    tc.assertTrue(len(bed_out)== 0)




