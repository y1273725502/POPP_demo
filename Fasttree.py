import os
import subprocess
import matplotlib.pyplot as plt
from Bio import Phylo


# 使用IQ-TREE生成进化树
def create_tree(input_file,output_file,mod):
    cmd = f"FastTree {mod} {input_file} > {output_file}"
    process = subprocess.run(cmd, shell=True)
    if process.returncode == 0:
        print("FastTree run successfully.")
    else:
        print("FastTree encountered an error.")


# 使用matplotlib和Biopython的Phylo模块展示进化树
def draw_tree(tree_file, time):
    tree = Phylo.read(tree_file, "newick")
    Phylo.draw(tree, do_show=False)
    # 删除原来的png文件
    if os.path.exists(f"{time}/tree.png"):
        os.remove(f"{time}/tree.png")
    plt.savefig(f"{time}/tree.png")


def tree(time,mod):
    # 输入文件和输出文件的路径
    input_file = f"{time}/temp.fasta"
    output_file = f"{time}/temp.fasta.treefile"
    create_tree(input_file,output_file,mod)
    draw_tree(output_file, time)
