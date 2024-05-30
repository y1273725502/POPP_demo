import re


def split_to_fasta(time, spec, genes):
    for each in spec:
        # 创建一个列表，存储含有特定基因的序列
        selected_sequences = []
        i = 0
        each = each.replace(' ', '_')

        for gene in genes:

            with open(f"{time}/temp-{gene}.fasta", 'r') as f:
                print(f"{time}/temp-{gene}.fasta")
                content = f.read()

            # 分割成多个序列
            sequences = content.split('>')[1:]  # 第一个元素为空，所以从第二个元素开始

            for sequence in sequences:

                if each+" " in sequence:
                    if i == 0:
                        selected_sequences.append(">" + each)
                        lines = sequence.split('\n')
                        lines_after_second = lines[1:]
                        result = '\n'.join(lines_after_second)
                        selected_sequences.append(result)
                        i += 1
                    else:
                        lines = sequence.split('\n')
                        lines_after_second = lines[1:]
                        result = '\n'.join(lines_after_second)
                        selected_sequences.append(result)

        # 将含有特定基因的序列写入新的txt文件
        with open(f'{time}/temp.fasta', 'a') as f:
            f.write('\n'.join(selected_sequences))

#split_to_fasta("2024-02-13-19-44-42",['Chlorella vulgaris', 'Geminella minor', 'Triticum aestivum'],['psbA'])