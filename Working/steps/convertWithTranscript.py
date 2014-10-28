
from __future__ import unicode_literals

from behave import *
import unittest
import sys

import StringIO
import re
import json

from behave import *




tc = unittest.TestCase('__init__')
tc.maxDiff = None

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
    Function that maps transcript coordinates to its genomic coordinates.
    :param genomic_info: a dictionary that contains position and the strand, ie
                    { 'position' : xxx,
                      'strand'  : + or 1 }
    :param transcript: a dictinoary that contains a transcript feature and its length and its starting postion
    :return: return a dictioanry containing transcript features mapped with its corresponding genomic coordinates
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


def compareTranscriptGenome(genomic, transcript):
    """
    Loop thru the feautres and feed them into function remap
    :param genomic: Genomic coordinates and its exons for a given gene
    :param transcript: Transcript features with coordiantes relative to transcript start site
    :return: Genomic coordiantes for given transcript start site.
    """
    return_dict = {}
    for transcript_name, feature in transcript.iteritems():
        try:
            genomic_info = genomic[transcript_name]
        except KeyError,e:
            print >> sys.stdout, e
            continue
        return_dict.update(remap(genomic_info, feature))


    return return_dict


def writeBedFormat(genomic_features):
    """
    Convert genomic features dictioanry from remap and compare transcript genome into bed foramt
    :param genomic_features:
    :return: bedformat of genomic features
    """
    return_list = []
    for feature_name, feature_info in genomic_features.iteritems():
        return_list.append(

            "\t".join(map(str, ['chr%s' % feature_info['chr'],
             feature_info['start'] - 1,
             feature_info['end'],
             feature_name,
             0,
             feature_info['strand']
            ]))

        )

    return return_list


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






















