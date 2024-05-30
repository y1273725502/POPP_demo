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


def geneForEachSpec(spec, work_fold,database):
    dictionary = {}

    for select in spec:
        genes = []
        id = name_to_id(select,database)
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
            if found_gene_name not in genes:
                genes.append(found_gene_name)
        dictionary.update({select: genes})
    return dictionary
