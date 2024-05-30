#用于将ncbi下载的基因信息去重，并加入到数据库中
import sqlite3
from collections import defaultdict
import re
def filter_chloroplast(folder):
    species_nc_dict = defaultdict(list)

    # 读取文件，将所有nc号存储起来
    with open(folder, 'r') as f:
        lines = f.readlines()
        for i in range(0, len(lines), 4):  # 每3行是一个物种的信息
            species_line = lines[i+1]
            nc_line = lines[i + 3]

            # 从species_line中提取物种名
            match = re.search(r'\d+\.\s+(.*?)\s+chloroplast', species_line)
            if match is None:
                print(f"Failed to extract species name from line: {i} {species_line}")
                continue
            species = match.group(1)

            # 从nc_line中提取nc号
            nc = nc_line.strip().split()[0]

            species_nc_dict[species].append(nc)

    # 进行过滤
    filtered_species_nc_dict = {}
    for species, ncs in species_nc_dict.items():
        if len(ncs) > 1:  # 如果有多个nc号
            for nc in ncs:
                if nc.startswith('NC'):  # 保留NC开头的nc号
                    filtered_species_nc_dict[species] = nc
                    break
        else:  # 如果只有一个nc号
            filtered_species_nc_dict[species] = ncs[0]

    # # 如果你需要将结果写入到新的文件中，可以使用以下代码
    # with open('filtered_file.txt', 'w') as f:
    #     for species, nc in filtered_species_nc_dict.items():
    #         f.write(f'{species}\n{nc}\n')

    # 创建一个数据库连接
    conn = sqlite3.connect('chloroplast_species_nc.db')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 创建一个表格
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SpeciesNC (
            species TEXT,
            nc TEXT
        )
    ''')

    # 创建一个游标对象
    cursor = conn.cursor()

    # 将过滤后的物种和nc号信息写入数据库
    for species, nc in filtered_species_nc_dict.items():
        cursor.execute(f'SELECT COUNT(*) FROM SpeciesNC WHERE nc="{nc}"')
        # 获取查询结果
        result = cursor.fetchone()
        # 检查结果
        if result[0] > 0:
            print("字符串在数据库中存在，跳过。")
        else:
            print("字符串在数据库中不存在。")
            cursor.execute('''
                INSERT INTO SpeciesNC (species, nc)
                VALUES (?, ?)
            ''', (species, nc))

    # 提交更改并关闭连接
    conn.commit()
    conn.close()

