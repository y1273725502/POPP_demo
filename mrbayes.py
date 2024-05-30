import os
import subprocess
import matplotlib.pyplot as plt
from Bio import Phylo

import fas_to_nex
import tre_to_newick


# ʹ��IQ-TREE���ɽ�����
def create_tree(input_file):
    cmd = f"mrbayes {input_file}"
    print(cmd)
    process = subprocess.run(cmd, shell=True)
    if process.returncode == 0:
        print("mrbayes run successfully.")
    else:
        print("mrbayes encountered an error.")


# ʹ��matplotlib��Biopython��Phyloģ��չʾ������
def draw_tree(tree_file, time):
    tree = Phylo.read(tree_file, "newick")
    Phylo.draw(tree, do_show=False)
    # ɾ��ԭ����png�ļ�
    if os.path.exists(f"{time}/tree.png"):
        os.remove(f"{time}/tree.png")
    plt.savefig(f"{time}/tree.png")


def tree(time,outgroup, ngen, samplefreq, printfreq, nchains):
    # �����ļ�������ļ���·��
    input_file = f"{time}/output.nex"
    output_file = f"{time}/temp.fasta.treefile"
    fas_to_nex.main(time,outgroup, ngen, samplefreq, printfreq, nchains)
    create_tree(input_file)
    tre_to_newick.tre_to_newick(time)
    draw_tree(output_file, time)