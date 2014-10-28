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