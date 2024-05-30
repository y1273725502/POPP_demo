import os
import subprocess
import matplotlib.pyplot as plt
from Bio import Phylo

# 使用IQ-TREE生成进化树
def create_tree(input_file,b,bb,o,outgroup):
    cmd = f"iqtree -s {input_file} {b} {bb} {o} {outgroup}"
    print(cmd)
    process = subprocess.run(cmd, shell=True)
    if process.returncode == 0:
        print("IQ-TREE run successfully.")
    else:
        print("IQ-TREE encountered an error.")

# 使用matplotlib和Biopython的Phylo模块展示进化树
def draw_tree(tree_file,time):
    tree = Phylo.read(tree_file, "newick")
    # fig, ax = plt.subplots(figsize=(20, 20))
    #Phylo.draw(tree,do_show=False,axes=ax)
    Phylo.draw(tree, do_show=False)
    # 删除原来的png文件
    if os.path.exists(f"{time}/tree.png"):
        os.remove(f"{time}/tree.png")
    plt.savefig(f"{time}/tree.png")

def tree(time,b,bb,o,outgroup):
    # 输入文件和输出文件的路径
    input_file = f"{time}/temp.fasta"
    output_file = f"{time}/temp.fasta.treefile"
    create_tree(input_file,b,bb,o,outgroup)
    draw_tree(output_file,time)

#tree("2024-02-13-21-29-30")
    
    # if os.path.exists("align.fasta"):
    #     os.remove("align.fasta")
    # if os.path.exists("align.fasta.bionj"):
    #     os.remove("align.fasta.bionj")
    # if os.path.exists("align.fasta.ckp.gz"):
    #     os.remove("align.fasta.ckp.gz")
    # if os.path.exists("align.fasta.iqtree"):
    #     os.remove("align.fasta.iqtree")
    # if os.path.exists("align.fasta.log"):
    #     os.remove("align.fasta.log")
    # if os.path.exists("align.fasta.mldist"):
    #     os.remove("align.fasta.mldist")
    # if os.path.exists("align.fasta.model.gz"):
    #     os.remove("align.fasta.model.gz")
    # # if os.path.exists("align.fasta.treefile"):
    # #     os.remove("align.fasta.treefile")
    # if os.path.exists("1.fasta"):
    #     os.remove("1.fasta")
