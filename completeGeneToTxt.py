import os


def completeGeneToTxt(folder,ncID,time):
    with open(folder + "/" + ncID + '_complete.txt') as file1:
        data_file1 = file1.read()
    if not os.path.exists(f"{time}/CDS_gene"):
        os.mkdir(f"{time}/CDS_gene")
    with open(f'{time}/CDS_gene/1.fasta', 'a') as file2:
        # 将第一个文件的内容写入第二个文件的末尾
        file2.write(data_file1)