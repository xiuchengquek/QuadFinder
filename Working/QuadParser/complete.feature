Feature: Given and gtf file and a QuadParser output which contains
         information about features of a transcript with position
         relative to the start of the transcript.
         Convert the postition into genomic co-ordinate


Scenario: A single transcript with a single feature on the positive strand
 	Given a Gencode file  "mock_files/gencode.annotation.v17.gtf" which has 1 based coordinates
      """
      #zz
      chr1	ENSEMBL	transcript	11	50	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000515242.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-201"; level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
      chr1	ENSEMBL	exon	11	20	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000515242.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-201"; exon_number 1;  level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
      chr1	ENSEMBL	exon	31	40	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000515242.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-201"; exon_number 2;  level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
      """
    And a QuadParser file "mock_files/Quad.out" which has 0 based coordaintes
      """
      ENST00000515242.2 gene=ARF5 CDS=155-695	0	15	ENST00000515242.2 gene=ARF5 CDS=155-695_1008_1045_for	15	+	GGGGCCAGGTTGGGAGGGGGAAGGTGAGGGCTTCGGG
      """
      Then the output of will be a bed file that is 0 base
      """
      chr1	10	20	ENST00000515242.2-1-1	0	+
      chr1	30	35	ENST00000515242.2-1-2	0	+
      """


Scenario: If matching transcript is not found
 	Given The same Gencode file  "mock_files/gencode.annotation.v17.gtf" which has 1 based coordinates
      """
      chr1	ENSEMBL	transcript	11	50	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000515242.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-201"; level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
      chr1	ENSEMBL	exon	11	20	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000515242.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-201"; exon_number 1;  level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
      chr1	ENSEMBL	exon	31	40	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000515242.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-201"; exon_number 2;  level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
      """
    And a Different QuadParser file "mock_files/Quad.out" which has 0 based coordaintes
      """
      ENST000005152422222.2 gene=ARF5 CDS=155-695	0	15	ENST00000515242.2 gene=ARF5 CDS=155-695_1008_1045_for	15	+	GGGGCCAGGTTGGGAGGGGGAAGGTGAGGGCTTCGGG
      """
	Then there will no results




