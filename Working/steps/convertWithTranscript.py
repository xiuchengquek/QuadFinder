
from __future__ import unicode_literals

from behave import *
import unittest
import sys

import StringIO
import re
import json

from behave import *

def findBetween(transcript_pos, genomic_exon):
    """
    Given a transcript position and a list of exons. find which exon the transcrtip fails in 
    :param transcript_pos:
    :param genomic_exon:
    :return:
    """
    for index, value in enumerate(genomic_exon):
        if value['t_start'] <=  transcript_pos  and value['t_end'] >= transcript_pos:
            relative_end = transcript_pos - value['t_start']
            return {'index' : index, 'relative_end' : relative_end }


def rebuild_coordinates(exons, relative_end, feature_name, genomic_info):
    """
    Build output for bed file
    :param exons: list of subsetted exons
    :param relative_end: end point to the start of exon (transcript)
    :param feature_name: name of feature (transcript)
    :param genomic_info: genomic_info , dictionary carrying all genomic feature
    :return:
    """
    exon_counts = len(exons)
    return_dict = {}
    for index, x in enumerate(exons):
        current_exon = index + 1
        name = "%s-%s" % (feature_name, current_exon)
        if current_exon == exon_counts :
            if genomic_info['strand'] == '+' :
                genomic_start = x['g_start']
                genomic_end = x['g_start'] + relative_end
            else:
                genomic_start = x['g_end'] - relative_end
                genomic_end = x['g_end']
            return_dict[name] = {
                    'start'  : genomic_start,
                    'end' : genomic_end,
                    'strand' : genomic_info['strand'],
                    'chr' : genomic_info['chr']
                }
        else:
            return_dict[name] = {
                'start'  : x['g_start'],
                'end' :  x['g_end'],
                'strand' : genomic_info['strand'],
                'chr' : genomic_info['chr']
            }
    return return_dict

def remap(genomic_info, transcript_feature):
    """
    :param genomic_info: a dictionary that contains position and the strand, ie
                    { 'position' : xxx,
                      'strand'  : + or 1 }
    :param transcript: a dictinoary that contains a transcript feature and its length and its starting postion
    :return:
    """


    return_dict = {}
    exons  = genomic_info['exons']
    if genomic_info['strand'] == '-':
        exons = [x for x in reversed(exons)]

    for features_name, features_info in transcript_feature.iteritems():
        transcript_start = int(features_info['position'] + 1)
        transcript_end = int(features_info['position']) + int(features_info['length'])
        first_exon = findBetween(transcript_start, exons)
        last_exon = findBetween(transcript_end, exons)
        subset_exons = exons[first_exon['index']:last_exon['index']+1]
        genome_coordinates = rebuild_coordinates(subset_exons, last_exon['relative_end'], features_name, genomic_info)
        return_dict.update(genome_coordinates)
    return return_dict


def compareTranscriptGenoem(genomic, transcript):
    return_dict = {}
    for transcript_name, feature in transcript.iteritems():
        genomic_info = genomic[transcript_name]
        return_dict.update(remap(genomic_info, feature))

    return return_dict

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
    tc = unittest.TestCase('__init__')
    tc.maxDiff = None
    results_info =  json.loads(context.text)
    results_dict = compareTranscriptGenoem(context.genomic_feature, context.transcript_feature )
    tc.assertDictEqual(results_info, results_dict)























