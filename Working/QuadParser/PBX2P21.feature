Feature: Get Genomeic Coordiantes of Transcript Feature


  Scenario: ENST00000560287, is a single exon transcript and is on the positive strand
  Given Feature of Transcript ENST00000293443 on a gtf file
  """
  chr3	HAVANA	transcript	142895127	142897305	.	+	.	gene_id "ENSG00000244171.3"; transcript_id "ENST00000560287.1"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "PBX2P1"; transcript_type "processed_transcript"; transcript_status "KNOWN"; transcript_name "PBX2P1-002"; level 2; tag "basic"; havana_gene "OTTHUMG00000159350.2"; havana_transcript "OTTHUMT00000417717.1";
  chr3	HAVANA	exon	142895127	142897305	.	+	.	gene_id "ENSG00000244171.3"; transcript_id "ENST00000560287.1"; gene_type "pseudogene"; gene_status "KNOWN"; gene_name "PBX2P1"; transcript_type "processed_transcript"; transcript_status "KNOWN"; transcript_name "PBX2P1-002"; exon_number 1;  exon_id "ENSE00002557317.1";  level 2; tag "basic"; havana_gene "OTTHUMG00000159350.2"; havana_transcript "OTTHUMT00000417717.1";
  """
  And the Transcript Features are
  """
  ENST00000560287.1 gene=PBX2P1	0	28	ENST00000560287.1 gene=PBX2P1_0_28_for	28	+	GGGGCTGAGCAGGGAGGGGGCCTCAGGG
  ENST00000560287.1 gene=PBX2P1	77	98	ENST00000560287.1 gene=PBX2P1_77_98_for	21	+	GGGGCCCGGGGGGGGCCTGGG
  ENST00000560287.1 gene=PBX2P1	156	189	ENST00000560287.1 gene=PBX2P1_156_189_for	33	+	GGGGGTAGCGGGGGGTTCCCGGGAGGCCGAGGG
  """
  Then the resulting bed file should be
  """
  chr3	142895126	142895154	ENST00000560287.1-1-1	0	+
  chr3	142895203	142895224	ENST00000560287.1-2-1	0	+
  chr3	142895282	142895315	ENST00000560287.1-3-1	0	+
  """

