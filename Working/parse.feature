Feature: Parse Gencode GTF and QuadPraser Output and results from quadPraser into a dictionary

Scenario: Parsing Gencode GTF file and store information of the cDNA
    Given gencode file : "mock_files/gencode.annotation.v17.gtf"
        """
        chr1	ENSEMBL	transcript	11872	14412	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000515242.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-201"; level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
        chr1	ENSEMBL	exon	11872	12227	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000515242.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-201"; exon_number 1;  level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
        chr1	ENSEMBL	exon	12613	12721	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000515242.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-201"; exon_number 2;  level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
        chr1	ENSEMBL	transcript	11874	14409	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000518655.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-202"; level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
        chr1	ENSEMBL	exon	11874	12227	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000518655.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-202"; exon_number 1;  level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
        chr1	ENSEMBL	exon	12595	12721	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000518655.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-202"; exon_number 2;  level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
        chr1	ENSEMBL	exon	13403	13655	.	+	.	gene_id "ENSG00000223972.4"; transcript_id "ENST00000518655.2"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "DDX11L1"; transcript_type "unprocessed_pseudogene"; transcript_status "KNOWN"; transcript_name "DDX11L1-202"; exon_number 3;  level 3; havana_gene "OTTHUMG00000000961.2"; tss_id "TSS1";
    """
    Then this will be stored in a dictionary that like look like this

    """
    { "ENST00000515242.2" : {
        	"chr" : 1, "strand" : "+" ,
        		"exons" : [
        			{ "start" : 11872 , "end" : 12227},
        			{"start" : 12613, "end" : 12721}
        			]

        },

      "ENST00000518655.2" : {
      		"chr" : 1, "strand" : "+",
      			"exons" : [
      			          {"start" : 11874, "end" : 12227},
                          { "start" : 12595, "end" : 12721},
                          {  "start" : 13403, "end" : 13655 }
                          ]
       }
    }
    """


Scenario: Parsing QuadPraser Output
    Given output file : "mock_files/Quad.out"
    """
    ENST00000515242.2 gene=ARF5 CDS=155-695	10	30	ENST00000000233.5 gene=ARF5 CDS=155-695_1008_1045_for	20	+	GGGGCCAGGTTGGGAGGGGGAAGGTGAGGGCTTCGGG
    ENST00000515242.2 gene=ARF5 CDS=155-695	140	160	ENST00000000233.5 gene=ARF5 CDS=155-695_1008_1045_for	20	+	GGGGCCAGGTTGGGAGGGGGAAGGTGAGGGCTTCGGG
    """
    Then this will be stored seperate dictionary that look like this
    """
    { "ENST00000515242.2": {
     	"ENST00000515242.2-1": { "position" : 10, "length"  : 20 },
     	"ENST00000515242.2-2":{	"position" : 140, "length" : 20  }
     	}
    }
   """









