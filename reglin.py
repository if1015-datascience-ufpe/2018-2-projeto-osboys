import pandas as pd
import statsmodels.formula.api as smf

#DataFrame de pedidos de atendimento
adf = pd.read_csv('data/156cco2018.csv', sep = ';', encoding = 'latin1')

date_cols = ['DATA_DEMANDA', 'DATA_ULT_SITUACAO']

adf[date_cols] =\
    pd.DataFrame([pd.to_datetime(adf[col], format = '%Y-%m-%d') for col in date_cols]).T

adf = adf[adf['SITUACAO'] == 'ATENDIDA']

#DataFrame de dados dos bairros
bdf = pd.read_csv('dados_corrigidos.csv')

cols = ['nome_bairro', 'rend_medio', 'populacao', 'area_hectare']

bdf = bdf[cols]

#DataFrame de tempo entre demanda e execução
tdf = adf['DATA_ULT_SITUACAO'] - adf['DATA_DEMANDA']
tdf = pd.concat([tdf, adf['BAIRRO']], axis = 1)
tdf.columns = ['DEMORA', 'BAIRRO']
tdf = tdf.groupby('BAIRRO')
tdf = tdf.sum() / tdf.count()
