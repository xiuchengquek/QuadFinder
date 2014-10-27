
Feature: join exons from genome to give transcript location



Scenario: for a given list of exon join them up
	Given a list that looks like this
	| start | end |
	| 11	| 20  |
	| 31    | 40  |
	Then return the following dictionary with transcript info
	| g_start | g_end | t_start | t_end |
	| 11      | 20    | 1       | 10    |
	| 31      | 40    | 11      | 20    |


Scenario: Positive strand
    Given A genome annotation file
    | transcript_name  | chr |     exon | start | end | strand |
    | TestA            | 1   |     1    |  11   | 20  | +      |
    | TestA            | 1   |     2    |  31   | 40  | +      |
    | TestB            | 1   |     1    |  11   | 20  | -      |
    | TestB            | 1   |     2    |  31   | 40  | -      |
    """
        {
         "TestA" : { "chr" :  1, "strand" : "+" ,
               "exons" : [
                        { "start" : 11, "end" : 20 },
                        { "start" : 31, "end" : 40 }]
             },
         "TestB" : { "chr" :  1, "strand" : "-" , "exons" : [
                                           { "start" : 11, "end" : 20 },
                                           { "start" : 31, "end" : 40 }]
                                       }
       }
    """
    Then the genomic feature at transcript level will be
    | transcript_name  | chr | exon | genomic_start | genomic_end | strand |transcript_start| transcript_end |
    | TestA            | 1   | 1    |  11           | 20          | +      |1               | 10             |
    | TestA            | 1   | 2    |  31           | 40          | +      |11              | 20             |
    | TestB            | 1   | 1    |  11           | 20          | -      |11              | 20             |
    | TestB            | 1   | 2    |  31           | 40          | -      |1               | 10             |
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

