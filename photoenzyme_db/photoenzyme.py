import pandas as pd
import sqlite3
import cirpy
import re

def read_data():
    photo_df = pd.read_csv("photo_data.csv")
    enzyme_df = photo_df[["protein_sequence", "enzyme_classification", "uniprot_id", "pdb_id", "alphafold_id"]]
    print(photo_df.columns)
    reaction_df = photo_df[["substrate", "product", "yield", "quantum_yield", "er", "ee", "wavelength_nm",
                            "ph_condition", "temp_celsius", "substrate_concentration", "solvent", "enzyme_loading",
                            "reaction_time", "citation"]]
    return photo_df, enzyme_df, reaction_df

def iupac_to_smiles(reaction_df):
    clean_df = reaction_df[reaction_df["ee"].notna()]
    product_iupac_names = clean_df["product"]
    product_smile_list = []

    for name in product_iupac_names:
        split_name = re.split(r', (?=\S|$)', name)
        for individual_product in split_name:
            smile = cirpy.resolve(individual_product, 'smiles')
            product_smile_list.append(smile)
            print(individual_product, smile)


def create_db(photo_df, enzyme_df, reaction_df):

    photo_db = "photo_enzyme.db"
    conn = sqlite3.connect(photo_db)
    cursor = conn.cursor()

    enzyme_df.to_sql("enzyme_table", conn, if_exists = "replace", index = True)
    reaction_df.to_sql("reactions_table", conn, if_exists = "replace", index = True)

    conn.close()

    return photo_db

def verify_db(photo_db):
    conn_verify = sqlite3.connect(photo_db)
    cursor_verify = conn_verify.cursor()
    cursor_verify.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor_verify.fetchall()
    print("Tables in", photo_db, ":", tables)

    df_from_enzyme_table = pd.read_sql_query("SELECT * FROM enzyme_table", conn_verify)
    print("Data table from enzyme table")
    print(df_from_enzyme_table.columns)

    df_from_reactions_table = pd.read_sql_query("SELECT * FROM reactions_table", conn_verify)
    print("Data table from reactions table")
    print(df_from_reactions_table.columns)

    conn_verify.close()
    print("Verification connection to", photo_db, "is closed")


def main():
    photo_df, enzyme_df, reaction_df = read_data()
    updated_reaction_df = iupac_to_smiles(reaction_df)
    photo_db = create_db(photo_df, enzyme_df, reaction_df)
    verify_db(photo_db)

main()