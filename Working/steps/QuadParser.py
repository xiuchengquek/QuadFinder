

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
        genomic_end = int(genomic['position']) -int(transcript['position'])
        genomic_start = (genomic_end  - int(transcript['length'])) + 1
    return {'start' : genomic_start, 'end' : genomic_end}


def parseGTF(file):
    getTranscriptID = re.compile('transcript_id "(.*)"; gene_type')
    exon_info = {}
    with open(file, 'r') as f:
        for line in f:
            fields = line.split('\t')
            if fields[2].startswith('exon'):
                transcript_id = getTranscriptID.search(fields[8]).group(1)

                if transcript_id in exon_info:
                    exon_no = "exon-%s" % (len(exon_info[transcript_id]) + 1)  ## get current exon number
                else:
                    exon_info[transcript_id] = {}
                    exon_no = 'exon-1'
                exon_info[transcript_id][exon_no] = {
                    'chrom' :  fields[0],
                    'start' :  int(fields[3]),
                    'end'   :  int(fields[4]),
                    'strand' : fields[6]
                }

    return exon_info


def parseQuadOut(file):
    re_transcript = re.compile('^([\w.]+)')

    feature_info = {}
    with open(file, 'r') as f:
        for index, line in enumerate(f):
            fields = line.split('\t')
            feature_number = "Feature %s" % index
            feature_info[feature_number] = {
                "TranscriptID" : re_transcript.match(fields[0]).group(0),
                "start" : int(fields[1]),
                "end"   : int(fields[2]),
                "strand" : fields[5],
                "length" : int(fields[4])
            }
    return feature_info