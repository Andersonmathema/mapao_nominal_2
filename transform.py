import pandas as pd
import re
import json

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
        if col in ['ALUNO', 'SITUAÇÃO', 'TOTAL FT An', 'TOTAL Fre An(%)'] or 'M' in col[-1]:
            colunas_relevantes.append(col)            
     
    # Selecionar as colunas específicas para o novo DataFrame
    new_df = dataframe[colunas_relevantes]

    # Remove linhas no final que não são alunos
    new_df = new_df.dropna(subset=['TOTAL FT An', 'TOTAL Fre An(%)'], how='all')
    
    return new_df

def disciplinas(dataframe):
    # Identificar as disciplinas disponíveis no DataFrame
    available_columns = dataframe.columns.tolist()    
    dis = []
    for col in available_columns:
        if 'M' in col[-1]:
            dis.append(col)    
    disciplinas_unicas = list(dis)  
    return disciplinas_unicas


def mapao_json(df: pd.DataFrame, ano: int, bimestre: int) -> dict:
    registros = []
    cols = df.columns.tolist()
    cols.pop(0)
    cols.pop(0)
    
    for i, row in df.iterrows():
        situacao = row['SITUAÇÃO'].strip()
        if situacao != "Ativo":
            continue

        medias = {}
        for col in cols:
            val = row[col]
            medias[col] = val

        nome = str(row['ALUNO']).strip()
            
        registros.append({
                "ano": ano,
                "bimestre": bimestre,
                "nome": nome,
                "situacao_mapao": "Ativo",
                "ft_anual": row['TOTAL FT An'],
                "freq_anual_pct": row['TOTAL Fre An(%)'],
                "medias": medias,
        })

    return {"source": "MAPAO", "registros": registros}


if __name__ == '__main__':
    df = carregar_planilha('/home/anderson/Documentos/mapao_nominal_2/MAPAO_3A_4bi.xlsx')  
    df_limpo = limpar_colunas(df)
    df_new = new_dataframe(df_limpo)
    print(disciplinas(df_new))
#     mp = mapao_json(df_new, 2025, 4)

#     output_path = "mapao_novo_3A_4bi_2025.json"

#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(
#             mp,
#             f,
#             ensure_ascii=False,
#             indent=2
#         )

#     print(f"JSON gerado com sucesso: {output_path}")
#     print(f"Total de registros: {len(mp['registros'])}")



