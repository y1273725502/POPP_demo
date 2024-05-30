import os
import subprocess
import matplotlib.pyplot as plt
from Bio import Phylo

import fas_to_nex
import tre_to_newick


# 使用IQ-TREE生成进化树
def create_tree(input_file):
    cmd = f"mrbayes {input_file}"
    print(cmd)
    process = subprocess.run(cmd, shell=True)
    if process.returncode == 0:
        print("mrbayes run successfully.")
    else:
        print("mrbayes encountered an error.")


# 使用matplotlib和Biopython的Phylo模块展示进化树
def draw_tree(tree_file, time):
    tree = Phylo.read(tree_file, "newick")
    Phylo.draw(tree, do_show=False)
    # 删除原来的png文件
    if os.path.exists(f"{time}/tree.png"):
        os.remove(f"{time}/tree.png")
    plt.savefig(f"{time}/tree.png")


def tree(time,outgroup, ngen, samplefreq, printfreq, nchains):
    # 输入文件和输出文件的路径
    input_file = f"{time}/output.nex"
    output_file = f"{time}/temp.fasta.treefile"
    fas_to_nex.main(time,outgroup, ngen, samplefreq, printfreq, nchains)
    create_tree(input_file)
    tre_to_newick.tre_to_newick(time)
    draw_tree(output_file, time)