from Bio import SeqIO, AlignIO, Phylo
from Bio.Align.Applications import ClustalwCommandline
import matplotlib.pyplot as plt
import os

def clustal(time,gene):

    # 序列比对
    clustalw_exe = "clustalw2.exe"
    clustalw_cline = ClustalwCommandline(clustalw_exe, infile=f"{time}/CDS_gene/{gene}.fasta")
    assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
    stdout, stderr = clustalw_cline()

    # 读取比对结果
    alignment = AlignIO.read(f"{time}/CDS_gene/{gene}.fasta".replace(".fasta", ".aln"), "clustal")

    # 将比对结果保存为FASTA格式
    output_fasta_file = f"{time}/CDS_gene/align-{gene}.fasta"
    AlignIO.write(alignment, output_fasta_file, "fasta")

def clustalAll(time):

    # 序列比对
    clustalw_exe = "clustalw2.exe"
    clustalw_cline = ClustalwCommandline(clustalw_exe, infile=f"{time}/CDS_gene/1.fasta")
    assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
    stdout, stderr = clustalw_cline()

    # 读取比对结果
    alignment = AlignIO.read(f"{time}/CDS_gene/1.fasta".replace(".fasta", ".aln"), "clustal")

    # 将比对结果保存为FASTA格式
    output_fasta_file = f"{time}/CDS_gene/align.fasta"
    AlignIO.write(alignment, output_fasta_file, "fasta")

