from __future__ import unicode_literals

import unittest
import sys

import StringIO
import re
import json

import argparse

__author__ = 'quek'



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

def parseGTF(file):
    getTranscriptID = re.compile('transcript_id "(.*)"; gene_type')
    exon_info = {}
    with open(file, 'r') as f:

        for line in f:
            if not line.startswith('#'):
                fields = line.split('\t')
                if fields[2].startswith('exon'):
                    transcript_id = getTranscriptID.search(fields[8]).group(1)
                    if transcript_id not in exon_info:
                        if 'chr' in fields[0]:
                            fields[0] = fields[0].replace("chr", "")
                        exon_info[transcript_id] = {'chr': fields[0],
                                                    'strand': fields[6],
                                                    'exons': []}

                    exon_info[transcript_id]['exons'].append({
                        'start': int(fields[3]),
                        'end': int(fields[4])
                    })

    return exon_info

def findBetween(transcript_pos, genomic_exon):
    """
    Given a transcript position and a list of exons. find which exon the transcrtip fails in
    :param transcript_pos:
    :param genomic_exon:
    :return:
    """
    for index, value in enumerate(genomic_exon):
        if int(value['t_start']) <=  int(transcript_pos)  and int(value['t_end']) >= int(transcript_pos):
            relative_start = transcript_pos - value['t_start']
            return {'index' : index, 'relative_start' : relative_start }

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
        genome_coordinates = rebuild_coordinates(subset_exons, first_exon,  last_exon, features_name, genomic_info)
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



def rebuild_coordinates(exons, start_exon,  last_exon, feature_name, genomic_info):
    """
    Build output for bed file
    :param exons: list of subsetted exons
    :param start_exon :  information of the start exon, namly the index ( which is the exon number)
    :param last_exon : infromation of the last exon
    :param feature_name: name of feature (transcript)
    :param genomic_info: genomic_info , dictionary carrying all genomic feature
    :return:
    """
    exon_counts = len(exons)
    return_dict = {}
    print >> sys.stdout, exons, last_exon, start_exon
    ## determien if start and end are the same if same them take their cooridinates between their relative_start
    start_exon_no = start_exon['index']
    last_exon_no = last_exon['index']
    for index, x in enumerate(exons):
        name = "%s-%s" % (feature_name, index + 1)


        if genomic_info['strand'] == '+':
            genomic_start = x['g_start']
            genomic_end = x['g_end']
            if index == start_exon_no:
                genomic_start = start_exon['relative_start'] + x['g_start']
            if index == last_exon_no:
                genomic_end =  last_exon['relative_start'] + x['g_start']
        else:
            genomic_start = x['g_start']
            genomic_end = x['g_end']

            if index == start_exon_no:
                genomic_end =  x['g_end'] - start_exon['relative_start']
            if index == last_exon_no:
                genomic_start = x['g_end'] -  last_exon['relative_start']



        return_dict[name] = {
            'start'  : genomic_start,
            'end' :  genomic_end,
            'strand' : genomic_info['strand'],
            'chr' : genomic_info['chr']
        }
    return return_dict



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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert Trascript Feature from QuadPraser to Genomic Feature')
    parser.add_argument('-i','--input', help='QuadParserOut', required=True)
    parser.add_argument('-g','--gtf', help='GTF File', required=True)
    parser.add_argument('-o','--out', help='output', required=True)

    args = vars(parser.parse_args())

    gtf_dict = parseGTF(args['gtf'])
    gtf_dict = convertGenomicLoc(gtf_dict)
    transcript_dict = parseQuadOut(args['input'])
    mapped_reads = compareTranscriptGenome(gtf_dict, transcript_dict)
    results = writeBedFormat(mapped_reads)
    with open(args['out'], 'w') as f :
        for line in results:
            f.write("%s\n" % line)

