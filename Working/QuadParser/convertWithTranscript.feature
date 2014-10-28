Feature: Convert Transcript features to Genomic Features with exon

Scenario:  Convert Transcript features coordinates to Genomic level coordiantes - Positive Strand only
    Given Transcript feature
    | transcript_name  | transcript_feature | length | position |
    | TestA            | TestA-1            |   15   |    0     |
    | TestB            | TestB-1            |   15   |    0     |
    """
        {"TestA":
            {"TestA-1": {
                "position" : 0,
                "length"   : 15
                }
            }
            }
    """

    When the genome feature is
    | transcript_name  | chr | exons | genomic_start | genomic_end | strand |transcript_start| transcript_end |
    | TestA            | 1   | 1     |  11           | 20          | +      |1               | 10             |
    | TestA            | 1   | 2     |  31           | 40          | +      |11              | 20             |
    """
     {
           "TestA"  : {"chr" : 1,
                       "strand" : "+",
                       "exons" : [
            {"g_start": 11 ,"g_end": 20, "t_start" : 1, "t_end" : 10},
            {"g_start": 31 ,"g_end": 40, "t_start" : 11, "t_end" : 20}

           ]
           }

    }

    """
    Then the genomic feature for the transcript should be
    | name         | chr | start | end |  strand |
    | TestA-1-1    | 1   | 11    | 20  |  +      |
    | TestA-1-2    | 1   | 31    | 35  |  +      |

    """
    {
           "TestA-1-1"  :
                { "chr" : 1, "start" : 11, "end" : 20, "strand" : "+"},
            "TestA-1-2"  :
                { "chr" : 1, "start" : 31, "end" : 35, "strand" : "+"}
        }
    """





Scenario:  Convert Transcript features coordinates to Genomic level coordiantes - both Strand
    Given Transcript feature
    | transcript_name  | transcript_feature | length | position |
    | TestA            | TestA-1            |   15   |    0     |
    | TestB            | TestB-1            |   15   |    0     |
    """
        {"TestA":
            {"TestA-1": {
                "position" : 0,
                "length"   : 15
                }
            },

          "TestB" :
             {"TestB-1":  {
                "position" : 0,
                "length"   : 15
                }
            }
        }
    """

    When the genome feature is
    | transcript_name  | chr | exons  | genomic_start | genomic_end | strand |transcript_start| transcript_end |
    | TestA            | 1   | 1      |  11           | 20          | +      |1               | 10             |
    | TestA            | 1   | 2      |  31           | 40          | +      |11              | 20             |
    | TestB            | 1   | 1      |  11           | 20          | -      |11              | 20             |
    | TestB            | 1   | 2      |  31           | 40          | -      |1               | 10             |

    """
     {
           "TestA"  : {"chr" : 1,
                       "strand" : "+",
                       "exons" : [
            {"g_start": 11 ,"g_end": 20, "t_start" : 1, "t_end" : 10},
            {"g_start": 31 ,"g_end": 40, "t_start" : 11, "t_end" : 20}

           ]
           },

           "TestB"  : {"chr" : 1,
               "strand" : "-",
               "exons" : [
               {"g_start": 11 ,"g_end": 20, "t_start" : 11, "t_end" : 20},
               {"g_start": 31 ,"g_end": 40, "t_start" : 1, "t_end" : 10}

               ]
    		}

    }

    """
    Then the genomic feature for the transcript should be
    | name         | chr | start | end |  strand |
    | TestA-1-1    | 1   | 11    | 20  |  +      |
    | TestA-1-2    | 1   | 31    | 35  |  +      |
    | TestB-1-2    | 1   | 16    | 20  |  -      |
    | TestB-1-1    | 1   | 31    | 40  |  -      |

    """
    {
           "TestA-1-1"  :
                { "chr" : 1, "start" : 11, "end" : 20, "strand" : "+"},
            "TestA-1-2"  :
                { "chr" : 1, "start" : 31, "end" : 35, "strand" : "+"},
            "TestB-1-2" :
                { "chr" : 1, "start" : 16, "end" : 20, "strand" : "-"},
            "TestB-1-1" :
                { "chr" : 1, "start" : 31, "end" : 40, "strand" : "-"}
        }
    """

Scenario:  C Convert Transcript features coordinates to Genomic level coordiantes - cross 3 exons for negative
    Given Transcript feature
    | transcript_name  | transcript_feature | length | position |
    | TestA            | TestA-1            |   15   |    0     |
    | TestB            | TestB-1            |   15   |    0     |
    """
        {"TestA":
            {"TestA-1": {
                "position" : 0,
                "length"   : 15
                }
            },

          "TestB" :
             {"TestB-1":  {
                "position" : 0,
                "length"   : 15
                }
            }
        }
    """

    When the genome feature is
    | transcript_name  | chr | exons | genomic_start | genomic_end | strand |transcript_start| transcript_end |
    | TestA            | 1   | 1     |  11           | 20          | +      |1               | 10             |
    | TestA            | 1   | 2     |  31           | 40          | +      |11              | 20             |
    | TestB            | 1   | 1     |  11           | 20          | -      |11              | 20             |
    | TestB            | 1   | 2     |  31           | 35          | -      |6               | 10             |
    | TestB            | 1   | 3     |  41           | 45          | -      |1               | 5              |

    """
     {
           "TestA"  : {"chr" : 1,
                       "strand" : "+",
                       "exons" : [
            {"g_start": 11 ,"g_end": 20, "t_start" : 1, "t_end" : 10},
            {"g_start": 31 ,"g_end": 40, "t_start" : 11, "t_end" : 20}

           ]
           },

           "TestB"  : {"chr" : 1,
               "strand" : "-",
               "exons" : [
               {"g_start": 11 ,"g_end": 20, "t_start" : 11, "t_end" : 20},
               {"g_start": 31 ,"g_end": 35, "t_start" : 6, "t_end" : 10},
               {"g_start": 41 ,"g_end": 45, "t_start" : 1, "t_end" : 5}


               ]
    		}

    }

    """
    Then the genomic feature for the transcript should be
    | name         | chr | start | end |  strand |
    | TestA-1-1    | 1   | 11    | 20  |  +      |
    | TestA-1-2    | 1   | 31    | 35  |  +      |
    | TestB-1-3    | 1   | 16    | 20  |  -      |
    | TestB-1-2    | 1   | 31    | 35  |  -      |
    | TestB-1-1    | 1   | 41    | 45  |  -      |

    """
    {
           "TestA-1-1"  :
                { "chr" : 1, "start" : 11, "end" : 20, "strand" : "+"},
            "TestA-1-2"  :
                { "chr" : 1, "start" : 31, "end" : 35, "strand" : "+"},
            "TestB-1-3" :
                           { "chr" : 1, "start" : 16, "end" : 20, "strand" : "-"},

            "TestB-1-2" :
                { "chr" : 1, "start" : 31, "end" : 35, "strand" : "-"},
            "TestB-1-1" :
                { "chr" : 1, "start" : 41, "end" : 45, "strand" : "-"}
        }
    """

Scenario:  Convert Transcript features coordinates to Genomic level coordiantes - cross 3 exons for negative, multiple features
    Given Transcript feature
    | transcript_name  | transcript_feature | length | position |
    | TestA            | TestA-1            |   15   |    0     |
    | TestB            | TestB-1            |   15   |    0     |
    | TestB            | TestB-2            |   18   |    0     |

    """
        {"TestA":
            {"TestA-1": {
                "position" : 0,
                "length"   : 15
                }
            },

          "TestB" :
             {"TestB-1":  {
                "position" : 0,
                "length"   : 15
                },
			"TestB-2":  {
				"position" : 0,
				"length"   : 18
				}
            }
        }
    """

    When the genome feature is
    | transcript_name  | chr | exons | genomic_start | genomic_end | strand |transcript_start| transcript_end |
    | TestA            | 1   | 1    |  11           | 20          | +      |1               | 10             |
    | TestA            | 1   | 2    |  31           | 40          | +      |11              | 20             |
    | TestB            | 1   | 1    |  11           | 20          | -      |11              | 20             |
    | TestB            | 1   | 2    |  31           | 35          | -      |6               | 10             |
    | TestB            | 1   | 3    |  41           | 45          | -      |1               | 5              |

    """
     {
           "TestA"  : {"chr" : 1,
                       "strand" : "+",
                       "exons" : [
            {"g_start": 11 ,"g_end": 20, "t_start" : 1, "t_end" : 10},
            {"g_start": 31 ,"g_end": 40, "t_start" : 11, "t_end" : 20}

           ]
           },

           "TestB"  : {"chr" : 1,
               "strand" : "-",
               "exons" : [
               {"g_start": 11 ,"g_end": 20, "t_start" : 11, "t_end" : 20},
               {"g_start": 31 ,"g_end": 35, "t_start" : 6, "t_end" : 10},
               {"g_start": 41 ,"g_end": 45, "t_start" : 1, "t_end" : 5}


               ]
    		}

    }

    """
    Then the genomic feature for the transcript should be
    | name         | chr | start | end |  strand |
    | TestA-1-1    | 1   | 11    | 20  |  +      |
    | TestA-1-2    | 1   | 31    | 35  |  +      |
    | TestB-1-3    | 1   | 16    | 20  |  -      |
    | TestB-1-2    | 1   | 31    | 35  |  -      |
    | TestB-1-1    | 1   | 41    | 45  |  -      |
    | TestB-2-3    | 1   | 13    | 20  |  -      |
    | TestB-2-2    | 1   | 31    | 35  |  -      |
    | TestB-2-1    | 1   | 41    | 45  |  -      |
    """
    {
           "TestA-1-1"  :
                { "chr" : 1, "start" : 11, "end" : 20, "strand" : "+"},
            "TestA-1-2"  :
                { "chr" : 1, "start" : 31, "end" : 35, "strand" : "+"},
            "TestB-1-3" :
                           { "chr" : 1, "start" : 16, "end" : 20, "strand" : "-"},
            "TestB-1-2" :
                { "chr" : 1, "start" : 31, "end" : 35, "strand" : "-"},
            "TestB-1-1" :
                { "chr" : 1, "start" : 41, "end" : 45, "strand" : "-"},

			"TestB-2-3" :
				{ "chr" : 1, "start" : 13, "end" : 20, "strand" : "-"},
			"TestB-2-2" :
				{ "chr" : 1, "start" : 31, "end" : 35, "strand" : "-"},
			"TestB-2-1" :
				{ "chr" : 1, "start" : 41, "end" : 45, "strand" : "-"}

        }
    """
    And the bedformat out but unordered
    """
    chr1	10	20	TestA-1-1	0	+
    chr1	30	35	TestA-1-2	0	+
    chr1	15	20	TestB-1-3	0	-
    chr1	30	35	TestB-1-2	0	-
    chr1	40	45	TestB-1-1	0	-
    chr1	12	20	TestB-2-3	0	-
    chr1	30	35	TestB-2-2	0	-
    chr1	40	45	TestB-2-1	0	-
    """
