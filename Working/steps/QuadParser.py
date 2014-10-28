from __future__ import unicode_literals

from behave import *
import unittest
import sys

import StringIO
import re
import json

__author__ = 'quek'


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


def parseGTF(file):
    getTranscriptID = re.compile('transcript_id "(.*)"; gene_type')
    exon_info = {}
    with open(file, 'r') as f:
        for line in f:
            fields = line.split('\t')
            if fields[2].startswith('exon'):
                transcript_id = getTranscriptID.search(fields[8]).group(1)
                if transcript_id not in exon_info:
                    if 'chr' in fields[0]:
                        fields[0] = fields[0].replace('chr', '')
                    exon_info[transcript_id] = {'chr': int(fields[0]),
                                                'strand': fields[6],
                                                'exons': []}

                exon_info[transcript_id]['exons'].append({
                    'start': int(fields[3]),
                    'end': int(fields[4])
                })

    return exon_info


def parseQuadOut(file):
    re_transcript = re.compile('^([\w.]+)')

    feature_info = {}
    with open(file, 'r') as f:
        for index, line in enumerate(f):
            fields = line.split('\t')
            transcript_id = re_transcript.match(fields[0]).group(0)
            if transcript_id in feature_info:
                feature_number = len(feature_info[transcript_id]) + 1
            else:
                feature_number = 1
                feature_info[transcript_id] = {}

            feature_name = "%s-%s" % (transcript_id, feature_number)
            feature_info[transcript_id][feature_name] = {'position': int(fields[1]),
                                                         'length': int(fields[4])}

    return feature_info


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
            "g_start": int(x['start']), "g_end": int(x['end']),
            "t_start": t_start, "t_end": t_end})

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


