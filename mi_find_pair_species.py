import sqlite3

spe=[]

def findPairSpecies(selection):
    for specie in selection:
        # ���ӵ�SQLite���ݿ�
        conn = sqlite3.connect("chloroplast_species_nc.db")
        cursor = conn.cursor()
        # ִ�в�ѯ��䣬��ȡ"nc"�к�"species"�е�ȫ����
        query = f"SELECT * FROM SpeciesNC WHERE species = '{specie}'"
        cursor.execute(query)
        # ��ȡ��ѯ���
        rows = cursor.fetchall()
        for species in rows:
            cursor.execute(f'SELECT COUNT(*) FROM Species WHERE NCID="{species[1]}"')
            # ��ȡ��ѯ���
            result = cursor.fetchone()
            # �����
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

