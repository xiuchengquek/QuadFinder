

Feature: Calculate start and end of a transcript feature that is 0-based to
         a given genomic location that is 1 based without considering exonic
         information. This will allow us to determine if the calculation wil be correct
          based on strand and feature length

Scenario: Positive Strand
	Given Genomic location of transcript
	| position | strand |
	| 5000	   | +      |
	| 1000     | -      |
	When the transcript feature is 0 based
	| position | length |
	| 10       | 20     |
	Then Transcript will have a genomic start and end of
	| start | end  | strand  |
	| 5010  | 5029 |   +     |
	|  971  |  990 |   -     |


