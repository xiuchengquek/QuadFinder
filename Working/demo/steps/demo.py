__author__ = 'quek'
from __future__ import unicode_literals

from behave import *
import unittest
import sys

import StringIO
import re
import json

from behave import *


def remap(genomic, transcript):
    """
    :param genomic: a dictionary that contains position and the strand, ie
                    { 'position' : xxx,
                      'strand'  : + or 1 }
    :param transcript: a dictinoary that contains a transcript feature and its length
    :return:
    """
    if genomic['strand'] == "+":
        genomic_start = int(genomic['position']) + int(transcript['position'])
        genomic_end = genomic_start + int(transcript['length']) - 1
    elif genomic['strand'] == "-":
        genomic_end = int(genomic['position']) - int(transcript['position'])
        genomic_start = (genomic_end - int(transcript['length'])) + 1
    return {'start': genomic_start, 'end': genomic_end}



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
