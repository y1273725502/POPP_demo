from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def fasta_to_nexus(time,input_fasta, output_nexus, outgroup, ngen, samplefreq, printfreq, nchains, data_type='dna',
                   missing='?', gap='-'):
    # 读取FASTA文件
    records = list(SeqIO.parse(input_fasta, "fasta"))

    # 将每个序列转换为SeqRecord对象
    seq_records = [SeqRecord(record.seq, id=record.id) for record in records]

    # 将SeqRecord对象写入NEXUS文件
    with open(output_nexus, "w") as nexus_file:
        nexus_file.write("#NEXUS\n")
        nexus_file.write("begin data;\n")
        nexus_file.write("  dimensions ntax={} nchar={};\n".format(len(seq_records), len(seq_records[0].seq)))
        nexus_file.write("  format datatype={} missing={} gap={};\n".format(data_type, missing, gap))
        nexus_file.write("  matrix\n")

        for seq_record in seq_records:
            nexus_file.write("    {}  {}\n".format(seq_record.id, seq_record.seq))

        nexus_file.write("  ;\n")
        nexus_file.write("end;\n\n")

        # 添加MrBayes建树所需的指令和参数
        nexus_file.write("begin mrbayes;\n")
        nexus_file.write("  set autoclose=yes nowarn=yes;\n")
        for out in outgroup:
            nexus_file.write(f"  outgroup {out};\n")
        nexus_file.write("  log start filename = log.txt;\n")
        nexus_file.write(
            f"  mcmcp ngen={ngen} samplefreq={samplefreq} printfreq={printfreq} nchains={nchains} savebrlens=yes filename={time}/output;\n")
        nexus_file.write("  mcmc;\n")
        nexus_file.write("  sumt conformat=Simple contype=Allcompat relburnin=yes burninfrac=0.25;\n")
        nexus_file.write("  sump relburnin=yes burninfrac=0.25;\n")
        nexus_file.write("end;\n")


def main(time, outgroup, ngen, samplefreq, printfreq, nchains):
    # 指定输入的FASTA文件和输出的NEXUS文件
    input_fasta_file = time + "/temp.fasta"
    output_nexus_file = time + "/output.nex"

    # 调用函数进行转换
    fasta_to_nexus(time,input_fasta_file, output_nexus_file, outgroup, ngen, samplefreq, printfreq, nchains)


# main("2024-02-28-15-27-30", ["Malus_x_domestica",'Pyrus_betulifolia'], 10000,1000,1000, 4)
