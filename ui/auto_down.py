from Bio import Entrez, SeqIO
import pandas as pd

# 请使用你自己的电子邮件地址
Entrez.email = "1273725502@qq.com"


def get_protein_ids(genbank_id):
    handle = Entrez.efetch(db="nucleotide", id=genbank_id, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    protein_ids = [f.qualifiers['protein_id'][0] for f in record.features if f.type == 'CDS']
    return protein_ids


def download_cds(protein_id):
    handle = Entrez.efetch(db="protein", id=protein_id, rettype="fasta", retmode="text")
    return handle.read()


# 读取Excel文件
df = pd.read_excel('genomes.xlsx', dtype={'GenBank ID': str})  # 替换这里的'your_file.xlsx'为你的Excel文件名

# 创建一个新的DataFrame来存储结果
result = pd.DataFrame(columns=['GenBank ID', 'CDS file'])

for index, row in df.iterrows():
    genbank_id = row['Assembly']  # 替换这里的'GenBank ID'为你的Excel文件中的列名
    if isinstance(genbank_id, str):  # 检查genbank_id是否是一个字符串
        protein_ids = get_protein_ids(genbank_id)

        for protein_id in protein_ids:
            cds = download_cds(protein_id)

            # 将CDS序列保存到文件中
            cds_file_path = f'F:/cds_files/{protein_id}.fasta'
            with open(cds_file_path, 'w') as file:
                file.write(str(cds))

            # 将结果添加到DataFrame中
            new_row = pd.DataFrame({'GenBank ID': [genbank_id], 'CDS file': [cds_file_path]})
            result = pd.concat([result, new_row], ignore_index=True)

# 保存结果到新的Excel文件中
result.to_excel('output.xlsx', index=False)
