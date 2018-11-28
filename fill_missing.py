import pandas as pd

df = pd.read_csv('dados_preliminares.csv')

def fill_missing(df, col_name, bairro, new_val):
    df.loc[df['nome_bairro'] == bairro, col_name] = new_val

#Correção de áreas em hectares:
h_bs = ['Casa Amarela',
        'Poço da Panela',
        'Santana',
        'Sítio dos Pintos',
        'Mustardinha',
        'Pau-Ferro']

h_vs = [188, 81, 47, 180, 63, 44]

for i, bairro in enumerate(h_bs):
    fill_missing(df, 'area_hectare', bairro, h_vs[i])

#Erro no bairro do Jordão:
fill_missing(df, 'taxa_m_cresc', 'Jordão', .49)

final_df = df

pd.DataFrame.to_csv(final_df, 'dados_corrigidos.csv')
