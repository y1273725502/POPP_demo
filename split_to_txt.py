#将第一个基因写入文件（带>）
import re
def split_to_txt(time,gene):
    with open(f"{time}/CDS_gene/temp-{gene}.txt", 'r') as f:
        print(f"{time}/CDS_gene/temp-{gene}.txt")
        content = f.read()

    # 分割成多个序列
    sequences = content.split('>l')[1:]  # 第一个元素为空，所以从第二个元素开始

    # 创建一个列表，存储含有特定基因的序列
    selected_sequences = []
    for sequence in sequences:
        # 使用正则表达式找到基因名
        if re.search(r'\[gene=(.*?)\]',sequence):
            found_gene_name = re.search(r'\[gene=(.*?)\]', sequence).group(1)
        # 如果找到的基因名和你想查找的基因名相同，那么将这个序列添加到列表中
        else:
            continue

        if found_gene_name == gene_name:
            selected_sequences.append(">" + Spec)
            lines = sequence.split('\n')
            lines_after_second = lines[1:]
            result = '\n'.join(lines_after_second)
            selected_sequences.append(result)


    # 将含有特定基因的序列写入新的txt文件
    with open(f'{time}/1.fasta', 'a') as f:
        f.write('\n'.join(selected_sequences))

# split_to_txt("rps120","F:\cds_files","Acer miaotaiense")