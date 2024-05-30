import datetime
import os
import re
import sqlite3


def name_to_id(item,database):
    # 连接到SQLite数据库
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # 执行查询语句，获取"nc"列和"species"列的全部行
    query = f"SELECT * FROM Species WHERE name = '{item}'"
    cursor.execute(query)
    # 获取查询结果
    rows = cursor.fetchall()
    # 关闭连接
    conn.close()
    return rows[0][1]

def geneToFolder(allGene,spec,work_fold,time,database):


    for species in spec:
        Spec = species.replace(' ', '_')
        id = name_to_id(species,database)
        with open(f"{work_fold}/{id}.txt", 'r') as f:
            print(f"{work_fold}/{id}.txt")
            content = f.read()
        # 分割成多个序列
        sequences = content.split('>l')[1:]  # 第一个元素为空，所以从第二个元素开始
        found_gene=[]
        for sequence in sequences:
            for gene in allGene:
                if re.search(r'\[gene=(.*?)\]', sequence):
                    found_gene_name = re.search(r'\[gene=(.*?)\]', sequence).group(1)
                else:
                    continue
                if gene==found_gene_name:

                    if found_gene_name not in found_gene:
                        found_gene.append(gene)
                        selected_sequences = []
                        selected_sequences.append(">" + Spec)
                        lines = sequence.split('\n')
                        lines_after_second = lines[1:]
                        result = '\n'.join(lines_after_second)
                        selected_sequences.append(result)

                        # 检查文件夹是否已存在，如果没有则创建新文件夹
                        if not os.path.exists(f"{time}/CDS_gene"):
                            os.mkdir(f"{time}/CDS_gene")
                        with open(f'{time}/CDS_gene/{gene}.fasta', 'a') as f:
                            f.write('\n'.join(selected_sequences))

#geneToFolder(['psbA'],['Geminella minor'],'F:/cds_files','2024-02-13-19-44-42')
