import pandas as pd 


def data_frame(file_path, sheet_name):
    # Carregar os dados do arquivo Excel
    df = pd.read_excel(file_path, sheet_name,  skiprows=9, header=[1, 2])
    return df


def new_dataframe(df1, df2):
    pass



