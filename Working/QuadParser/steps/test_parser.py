
from __future__ import unicode_literals

from behave import *
import unittest
import sys

import StringIO
import re
import json
from QuadParser import parseGTF, parseQuadOut
from behave import *

__author__ = 'quek'

tc = unittest.TestCase('__init__')
tc.maxDiff = None

@given('gencode file : "{GTFFILE}"')
def step_impl(context, GTFFILE):
    with open(GTFFILE, 'w+') as f:
        f.write(context.text)
    context.gtf = GTFFILE

@then('this will be stored in a dictionary that like look like this')
def step_impl(context):
    mock_results = json.loads(context.text)
    tc.assertDictEqual(mock_results, parseGTF(context.gtf))



@given(u'output file : "{QUADOUT}"')
def step_impl(context, QUADOUT):
    with open(QUADOUT, 'w+') as f:
        f.write(context.text)
    context.quadout = QUADOUT

@then(u'this will be stored seperate dictionary that look like this')
def step_impl(context):
    mock_results = json.loads(context.text)
    tc.assertDictEqual(mock_results, parseQuadOut(context.quadout))


