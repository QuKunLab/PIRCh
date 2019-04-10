# Scripts for data analysis in PIRCh-seq
## 1.Mapping
The raw fastq files were aligned by tophat v2.1.0. Output bam files were transformed to BedGraph files & BigWig files through bedtools v2.25.0.
## 2.Basic analysis
We used 'pirch_rpkm.py' and 'pirch_rpkm_raw.py' scripts to calculate the RPKM and raw reads counts from the relevant BedGraph files. 'position_mean_bedGraph.py' was then used to get the average read coverage around introns. 'reads_count_in_diff.py' was used to count the mapped reads distribution in different annotation region, such as exon, intron, TSS, 5'UTR et al. To calculate the ChIP signal over PIRCh-enriched ncRNA TSS region, we used the 'PIRCH_average_TSS.py' script. 
## 3.Enrichment analysis
For gene set enrichment analysis(GSEA), we used the BROAD Institute softward 'GSEA' V2.0.  R package 'limma'  v3.38.3  was used for enrichment analysis, and the p-value cut-off was set to 0.05. Detail of limma analysis was in 'limma.R' script. 
## 4.Data analysis
We used python 2.7 for further analysis in jupyter notebook. The main package we used are 'Pandas', 'Numpy', 'Scipy' and 'Sklearn'. Figure were drawed by 'matplotlib.pyplot' and 'seaborn'. The scirpt 'Data analysis.ipynb' consist of 4 parts: 1)Nascent transcript analysis(correlation with ChIP read count). 2) K-mean cluster and T-SNE. 3) Overlap with GRID/ChIRP/CHART/RAP result (measured by spearman corrleation). 4) Nearby coding gene expression calculation.
## 5.Allelic SNP analysis
The allele genome fasta file was made by GATK toolkit FastaAlternateReferenceMaker and SelectVariants V 3.6. SNPs at each gene were selected by 'refine_allele.py' and relevant read counts at each SNP position were calculated by 'pirch_SNP_expression.py'. RNA structure prediction was performed by the web server 'RNAfold'.
## 6.Peak calling
Peak calling was performed by 'eCLIPgoing.py' script. The relevant scripts were involved in the same folder.
## 7.Other data integration
1) icSHAPE score was downloaded from previous publication, and overlap of icSHAPE result with PIRCh result was performed by 'icSHAPE_PIRCh.py'. 
2) ChIRP binding sites were calculated by scripts provided by the original paper. Calculation of histone modification around ChIRP binding sites was performed by 'ChIRP_expand_unlog.py'. 
3) To overlap the binding sites of GRID/ChIRP/CHART/RAP result with ChIP result, we used 'mpi_chirp_overlap.py' script.
