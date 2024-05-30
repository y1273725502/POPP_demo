import sqlite3

spe=[]

def findPairSpecies(selection):
    for specie in selection:
        # 连接到SQLite数据库
        conn = sqlite3.connect("chloroplast_species_nc.db")
        cursor = conn.cursor()
        # 执行查询语句，获取"nc"列和"species"列的全部行
        query = f"SELECT * FROM SpeciesNC WHERE species = '{specie}'"
        cursor.execute(query)
        # 获取查询结果
        rows = cursor.fetchall()
        for species in rows:
            cursor.execute(f'SELECT COUNT(*) FROM Species WHERE NCID="{species[1]}"')
            # 获取查询结果
            result = cursor.fetchone()
            # 检查结果
            if result[0] > 0:
                print("pass")
                spe.append(species[0])
            else:
                print("no result")
                print(species[0],species[1])

    if len(spe)==0:
        return None
    else:
        return spe

