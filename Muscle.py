import os
import subprocess

def muscle(time,gene):
    # 输入文件的路径
    input_file = f"{time}/CDS_gene/{gene}.fasta"
    current_path = os.getcwd()


    inputFileName = current_path+"\\" + input_file
    outputFileName = current_path + f"/{time}/CDS_gene/align-{gene}.fasta"
    inputFileName = '''"{}"'''.format(inputFileName)
    outputFileName = '''"{}"'''.format(outputFileName)

    cmd = "muscle5.1.win64.exe --align " + "{} -output {}".format(inputFileName, outputFileName)
    print(cmd)

    # 使用subprocess运行命令
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)


    # 打印比对结果
    print(process.stdout.decode())

    # 如果有错误，打印错误
    if process.returncode != 0:
        print(process.stderr.decode())

def muscleAll(time):
    # 输入文件的路径
    input_file = f"{time}/CDS_gene/1.fasta"
    current_path = os.getcwd()


    inputFileName = current_path+"\\" + input_file
    outputFileName = current_path + f"/{time}/CDS_gene/align.fasta"
    inputFileName = '''"{}"'''.format(inputFileName)
    outputFileName = '''"{}"'''.format(outputFileName)

    cmd = "muscle5.1.win64.exe --align " + "{} -output {}".format(inputFileName, outputFileName)
    print(cmd)

    # 使用subprocess运行命令
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)


    # 打印比对结果
    print(process.stdout.decode())

    # 如果有错误，打印错误
    if process.returncode != 0:
        print(process.stderr.decode())
