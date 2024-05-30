# 发现并返回保守基因序列
import re
import sqlite3


def conservedSequence(selection,work_fold,database):
    conservedSequence = []
    i=0
    for select in selection:
        if i==0:
            i=i+1
            id=name_to_id(select,database)
            with open(f"{work_fold}/{id}.txt", 'r') as f:
                print(f"{work_fold}/{id}.txt")
                content = f.read()
            # 分割成多个序列
            sequences = content.split('>l')[1:]  # 第一个元素为空，所以从第二个元素开始
            for sequence in sequences:
                if re.search(r'\[gene=(.*?)\]', sequence):
                    found_gene_name = re.search(r'\[gene=(.*?)\]', sequence).group(1)
                else:
                    continue

                if found_gene_name not in conservedSequence:
                    conservedSequence.append(found_gene_name)
        else:
            id = name_to_id(select,database)
            with open(f"{work_fold}/{id}.txt", 'r') as f:
                print(f"{work_fold}/{id}.txt")
                content = f.read()
            # 分割成多个序列
            allSequences =[]
            sequences = content.split('>l')[1:]  # 第一个元素为空，所以从第二个元素开始
            for sequence in sequences:
                if re.search(r'\[gene=(.*?)\]', sequence):
                    found_gene_name = re.search(r'\[gene=(.*?)\]', sequence).group(1)
                else:
                    continue
                if found_gene_name not in allSequences:
                    allSequences.append(found_gene_name)
            conservedSequence=[x for x in conservedSequence if x in allSequences]
    return conservedSequence

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

#print(conservedSequence(['Chlorella vulgaris', 'Geminella minor', 'Triticum aestivum'],'F:/cds_files'))