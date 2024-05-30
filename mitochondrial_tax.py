import sqlite3
from Bio import Entrez

# 请使用你的邮箱地址，因为NCBI要求使用Entrez的用户提供一个邮箱地址
Entrez.email = ""

def get_tax_info(species,ncid):
    handle = Entrez.efetch(db="nucleotide", id=ncid, retmode="xml")
    records = Entrez.read(handle)
    tax_lineage = records[0]["GBSeq_taxonomy"].split("; ")
    tax_info = {"NCID": ncid}
    tax_info["species"]=species
    for tax in tax_lineage:
        if tax in ["Bacteria", "Archaea", "Eukaryota"]:
            tax_info["kingdom"] = tax
        elif tax.endswith("phyta") or tax.endswith("mycota"):
            tax_info["phylum"] = tax
        elif tax.endswith("opsida") or tax.endswith("mycetes"):
            tax_info["class"] = tax
        elif tax.endswith("ales"):
            tax_info["Orderr"] = tax
        elif tax.endswith("aceae"):
            tax_info["family"] = tax
        elif tax[0].isupper():
            tax_info["genus"] = tax
    if tax_info.get("kingdom")==None:
        tax_info["kingdom"] = "NULL"
    if tax_info.get("phylum")==None:
        tax_info["phylum"] = "NULL"
    if tax_info.get("class")==None:
        tax_info["class"] = "NULL"
    if tax_info.get("Orderr")==None:
        tax_info["Orderr"] = "NULL"
    if tax_info.get("family")==None:
        tax_info["family"] = "NULL"
    if tax_info.get("genus")==None:
        tax_info["genus"] = "NULL"
    return tax_info

def write_to_db(db_name, tax_info):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Species (
            name TEXT,
            NCID TEXT,
            kingdom TEXT,
            phylum TEXT,
            class TEXT,
            Orderr TEXT,
            family TEXT,
            genus TEXT,
            species TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO Species (name, NCID, kingdom, phylum, class, Orderr, family, genus, species)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (tax_info["species"], tax_info["NCID"], tax_info.get("kingdom"), tax_info.get("phylum"),
          tax_info.get("class"), tax_info.get("Orderr"), tax_info.get("family"), tax_info.get("genus"),
          tax_info.get("species")))
    conn.commit()
    conn.close()
    print(tax_info)
def taxInfo(species,ncid):
    tax_info = get_tax_info(species,ncid)
    write_to_db("mitochondrion_species_nc.db", tax_info)
