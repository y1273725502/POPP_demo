from Bio import Phylo
from matplotlib import pyplot as plt

def tre_to_newick(time):
    # 读取 Nexus 格式的树文件
    nexus_file_path = time+"/output.con.tre"
    trees = Phylo.parse(nexus_file_path, "nexus")

    # 写入每棵树到文件
    output_file_path = time+"/temp.fasta.treefile"
    with open(output_file_path, "w") as output_file:
        i=0
        for idx, tree in enumerate(trees):
            if i==0:
                # 将每棵树以 Newick 格式写入文件
                Phylo.write(tree, format='newick', file=output_file)
                i+=1
            else:
                pass
