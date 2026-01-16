import pandas as pd
import re

def carregar_planilha(path):
    df = pd.read_excel(path, skiprows=9, header=[1, 2])
    df = df.dropna(how='all')

    # Achatar os dois níveis, removendo "Unnamed"
    colunas = []
    for nivel1, nivel2 in df.columns:
        if "Unnamed" in str(nivel2):
            colunas.append(str(nivel1).strip())
        else:
            colunas.append(f"{nivel1} {nivel2}".strip())

    df.columns = colunas

    return df

def limpar_colunas(df):
    novas_colunas = []
    for col in df.columns:

        # remove quebras de linha
        col = col.replace('\n', ' ')

        # remove números sequenciais antes de M / F / AC
        col = re.sub(r'\s\d+(?=\s[MFA][C]?$)', '', col)

        # remove números standalone no meio
        col = re.sub(r'\s\d+\s', ' ', col)

        # tira espaços duplos
        col = re.sub(r'\s+', ' ', col).strip()

        novas_colunas.append(col)

    df.columns = novas_colunas
    return df


def new_dataframe(dataframe):
    # Identificar as disciplinas disponíveis no DataFrame
    available_columns = dataframe.columns.tolist()
        
    # Identificar e manter apenas as colunas relevantes ('Nome', 'Sit', 'M', 'F', 'AC', 'Total')
    colunas_relevantes = []
    
    for col in available_columns:
        if col[1] in ['Nome', 'Sit', 'M', 'F', 'AC', 'TF', 'Fre(%)', 'FT An.', 'Fre.An(%)']:
            colunas_relevantes.append(col)            
     
    # Selecionar as colunas específicas para o novo DataFrame
    new_df = dataframe[colunas_relevantes]
    
    return new_df

def disciplinas(dataframe):
    # Identificar as disciplinas disponíveis no DataFrame
    available_columns = dataframe.columns.tolist()    
    dis = []
    for col in available_columns:
        if col[1] in ['M', 'F', 'AC','TF', 'FRE(%)', 'FT AN.', 'FRE.AN(%)']:
            dis.append(col[0])    
    disciplinas_unicas = list(set(dis))  
    return disciplinas_unicas

if __name__ == '__main__':
    df = carregar_planilha('/home/ubuand/Documentos/mapao_nominal_2/mapao_3D.xlsx')
    df = limpar_colunas(df)
    print(df.head())




