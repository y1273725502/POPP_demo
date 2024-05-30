from Bio import Entrez, SeqIO


def download(name):
    Entrez.email = "1273725502@qq.com"

    search_query = name
    handle = Entrez.esearch(db="nucleotide", term=search_query)
    record = Entrez.read(handle)
    handle.close()

    # 获取线粒体基因组的记录
    if int(record["Count"]) > 0:
        id_list = record["IdList"]
        first_id = id_list[0]  # 取第一个记录的ID
        handle = Entrez.efetch(db="nucleotide", id=first_id, rettype="fasta", retmode="text")
        newname=name+'.fasta'
        new=newname.replace(' ','_')
        # 保存FASTA文件
        with open(new, "w") as output_file:
            output_file.write(handle.read())

        handle.close()
        print("基因组FASTA文件已下载成功。")
    else:
        print("未找到相关记录。")
