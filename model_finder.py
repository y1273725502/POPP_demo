import os
import subprocess
import matplotlib.pyplot as plt
from Bio import Phylo


# 使用IQ-TREE生成进化树
def create_tree(input_file, o, outgroup):
    cmd = f"iqtree -s {input_file} -m MFP {o} {outgroup}"
    print(cmd)
    process = subprocess.run(cmd, shell=True)
    if process.returncode == 0:
        print("IQ-TREE run successfully.")
    else:
        print("IQ-TREE encountered an error.")



def tree(time, o, outgroup):
    # 输入文件和输出文件的路径
    input_file = f"{time}/temp.fasta"
    output_file = f"{time}/temp.fasta.treefile"
    create_tree(input_file, o, outgroup)