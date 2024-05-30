from Bio import SeqIO, AlignIO, Phylo
from Bio.Align.Applications import ClustalwCommandline
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
import matplotlib.pyplot as plt
import os

def tree_constructor():

    # 序列比对
    clustalw_exe = "C:\Program Files (x86)\ClustalW2\clustalw2.exe"
    clustalw_cline = ClustalwCommandline(clustalw_exe, infile="combined.fasta")
    assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
    stdout, stderr = clustalw_cline()

    # 读取比对结果
    alignment = AlignIO.read("combined.fasta".replace(".fasta", ".aln"), "clustal")

    # 计算距离矩阵
    calculator = DistanceCalculator("identity")
    dm = calculator.get_distance(alignment)

    # 构建进化树
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(dm)

    # 绘制进化树
    Phylo.draw(tree)
    plt.show()

    if os.path.exists("combined.fasta"):
        os.remove("combined.fasta")
    if os.path.exists("combined.aln"):
        os.remove("combined.aln")
    if os.path.exists("combined.dnd"):
        os.remove("combined.dnd")
    if os.path.exists("1.fasta"):
        os.remove("1.fasta")
