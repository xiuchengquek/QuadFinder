from __future__ import unicode_literals

from behave import *
import unittest
import sys

import StringIO
import re
import json

from behave import *
__author__ = 'quek'


def exons_loop(exons, strandness=None):
    """
    :param exons: list of dictioanry. each dictionary will contain 2 keys "start", "end", value should be integer,
     if not function will convert.

    :return: list of dictioanry, each dictionary now contains 4 keys "g_start, g_end, t_start, t_end" all value are
    integer
    """
    return_list = []
    if strandness == "-":
        exons = reversed(exons)

    previous_end = 0
    for x in exons:
        exon_length = int(x['end']) - int(x['start'])
        t_start = previous_end + 1
        t_end = t_start + exon_length
        previous_end = t_end
        return_list.append({
            "g_start" : int(x['start']) , "g_end" : int(x['end']) ,
            "t_start" : t_start ,  "t_end" : t_end })

    if strandness == "-":
        return [x for x in reversed(return_list)]
    return return_list



def convertGenomicLoc(genomic_annotation):
    """

    :param genomic_annotation: a dictionary with the transcript name as the main key.
            each key will then have the following structure:
                chr, strand and a list of exons.
                each exons will contain the genomic start and end

    :return: this will convert the genomic start and end into the transcript start and end 't_start, t_end'
    """
    for keys, value in genomic_annotation.iteritems():
        genomic_annotation[keys]["exons"] = exons_loop(value['exons'], value['strand'])
    return genomic_annotation



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






