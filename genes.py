import re


def genes(self, Name,folder):
    # 初始化一个空列表，用于存储所有的gene=后面的内容
    genes = []

    # 打开并读取.txt文件
    with open(folder+'/'+Name+'.txt', 'r') as f:
        for line in f:
            # 使用正则表达式查找gene=后面的内容
            match = re.search(r'gene=([^ \[]+?)\]', line)
            # 如果找到了匹配的内容，就将它添加到列表中
            if match:
                genes.append(match.group(1))


    # 打印genes列表
    print(genes)
    return genes