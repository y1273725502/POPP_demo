import pandas as pd

# 读取Excel文件
df = pd.read_excel('genomes.xlsx')

# 提取genbank_id列
genbank_ids = df['Assembly']

# 将genbank_id列写入txt文件
with open('../genbank_ids.txt', 'w') as f:
    for id in genbank_ids:
        f.write(str(id) + '\n')
