import sqlite3

spe=[]

def findPairSpecies(selection):
    for specie in selection:

        conn = sqlite3.connect("mitochondrion_species_nc.db")
        cursor = conn.cursor()

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
                print("字符串在数据库中存在，跳过。")
                spe.append(species[0])
            else:
                print("字符串在数据库中不存在。")
                print(species[0],species[1])

    if len(spe)==0:
        return None
    else:
        return spe

